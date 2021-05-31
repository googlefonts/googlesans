# Copyright 2021 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import defaultdict
from types import SimpleNamespace
from typing import Any, Callable, DefaultDict, Dict, List, Optional, Sequence, Tuple

import fontTools
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.otlLib.builder import buildPairPosClassesSubtable
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables.otBase import ValueRecord
from fontTools.ttLib.ttFont import TTFont
from sklearn import cluster
from ufo2ft.featureWriters import ast
from ufo2ft.featureWriters.kernFeatureWriter import KernFeatureWriter


def compact(ttf: TTFont, mode: str, clustering_kwargs: Dict[str, Any] = {}) -> TTFont:
    # print("Compacting GPOS...")
    config = {"mode": mode, "clustering_kwargs": clustering_kwargs}
    # Plan:
    #  1. Find lookups of Lookup Type 2: Pair Adjustment Positioning Subtable
    #     https://docs.microsoft.com/en-us/typography/opentype/spec/gpos#lookup-type-2-pair-adjustment-positioning-subtable
    #  2. Extract glyph-glyph kerning and class-kerning from all present subtables
    #  3. Regroup into different subtable arrangements
    #  4. Put back into the lookup
    gpos = ttf["GPOS"]
    for lookup in gpos.table.LookupList.Lookup:
        if lookup.LookupType == 2:
            compact_lookup(ttf, config, lookup)
        elif lookup.LookupType == 9 and lookup.SubTable[0].ExtensionLookupType == 2:
            compact_ext_lookup(ttf, config, lookup)
    return ttf


def compact_lookup(
    ttf: TTFont, config: Dict[str, Any], lookup: fontTools.ttLib.tables.otTables.Lookup
) -> None:
    new_subtables = []
    for subtable in lookup.SubTable:
        if subtable.Format == 1:
            new_subtables.extend(compact_glyph_pairs(ttf, config, lookup, subtable))
        elif subtable.Format == 2:
            new_subtables.extend(compact_class_pairs(ttf, config, lookup, subtable))
    lookup.SubTable = new_subtables
    lookup.SubTableCount = len(new_subtables)


def compact_ext_lookup(
    ttf: TTFont, config: Dict[str, Any], lookup: fontTools.ttLib.tables.otTables.Lookup
) -> None:
    new_ext_subtables = []
    for ext_subtable in lookup.SubTable:
        subtable = ext_subtable.ExtSubTable
        if subtable.Format == 1:
            new_subtables = compact_glyph_pairs(ttf, config, lookup, subtable)
        elif subtable.Format == 2:
            new_subtables = compact_class_pairs(ttf, config, lookup, subtable)
        for subtable in new_subtables:
            ext_subtable = otTables.ExtensionPos()
            ext_subtable.Format = 1
            ext_subtable.ExtSubTable = subtable
            new_ext_subtables.append(ext_subtable)
    lookup.SubTable = new_ext_subtables
    lookup.SubTableCount = len(new_ext_subtables)


def compact_glyph_pairs(
    ttf: TTFont,
    config: Dict[str, Any],
    lookup: fontTools.ttLib.tables.otTables.Lookup,
    subtable: fontTools.ttLib.tables.otTables.PairPos,
) -> List[fontTools.ttLib.tables.otTables.PairPos]:
    return [subtable]


def compact_class_pairs(
    ttf: TTFont,
    config: Dict[str, Any],
    lookup: fontTools.ttLib.tables.otTables.Lookup,
    subtable: fontTools.ttLib.tables.otTables.PairPos,
) -> List[fontTools.ttLib.tables.otTables.PairPos]:
    subtables = []
    classes1: DefaultDict[int, List[str]] = defaultdict(list)
    for g in subtable.Coverage.glyphs:
        classes1[subtable.ClassDef1.classDefs.get(g, 0)].append(g)
    classes2: DefaultDict[int, List[str]] = defaultdict(list)
    for g, i in subtable.ClassDef2.classDefs.items():
        classes2[i].append(g)
    all_pairs = {}
    for i, class1 in enumerate(subtable.Class1Record):
        for j, class2 in enumerate(class1.Class2Record):
            if is_really_zero(class2.Value1) and is_really_zero(class2.Value2):
                continue
            all_pairs[(tuple(classes1[i]), tuple(classes2[j]))] = (
                class2.Value1,
                class2.Value2,
            )

    if config["mode"] == "one":
        subtables.append(
            buildPairPosClassesSubtable(all_pairs, ttf.getReverseGlyphMap())
        )
    elif config["mode"] == "max":
        groups: Dict[Any, Any] = defaultdict(dict)
        for pair, values in all_pairs.items():
            groups[pair[0]][pair] = values
        for pairs in groups.values():
            subtables.append(
                buildPairPosClassesSubtable(pairs, ttf.getReverseGlyphMap())
            )
    elif config["mode"] == "auto":
        grouped_pairs = cluster_pairs_by_class2_coverage(
            all_pairs, config["clustering_kwargs"]
        )
        for pairs in grouped_pairs:
            subtables.append(
                buildPairPosClassesSubtable(pairs, ttf.getReverseGlyphMap())
            )
    else:
        raise ValueError(f"Bad config {config}")
    return subtables


def is_really_zero(value: Optional[ValueRecord]) -> bool:
    if value is None:
        return True
    return not bool(value.getEffectiveFormat())


Pairs = Dict[Tuple[Tuple[str, ...], Tuple[str, ...]], Any]


def cluster_pairs_by_class2_coverage(
    pairs: Pairs, clustering_kwargs: Dict[str, Any]
) -> List[Pairs]:
    # Idea:
    #   1. group pairs by Class1 = get lines from the matrix
    #   2. cluster together lines that have non-zero values in the same Class2
    #   3. make 1 subtable per cluster
    # That way, we hope to have fewer subtables than in the "max" strategy,
    # but that each subtable will have high occupancy/low sparsity thanks to
    # the clustering.
    all_class1 = list(set(pair[0] for pair in pairs))
    all_class2 = list(set(pair[1] for pair in pairs))
    vectors = [
        [1 if (class1, class2) in pairs else 0 for class2 in all_class2]
        for class1 in all_class1
    ]
    # Make matrix lines
    lines: Dict[Sequence[str], Pairs] = defaultdict(dict)
    for pair, values in pairs.items():
        lines[pair[0]][pair] = values
    # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
    # Default values determined by running:
    # python -m scripts.measure_kerning_optimizations.find_best_clustering
    kwargs = {**clustering_kwargs}  # Shallow copy to edit defaults
    if "lines_per_cluster" in kwargs:
        lines_per_cluster = kwargs.pop("lines_per_cluster")
        kwargs["n_clusters"] = min(
            max(int(len(lines) / lines_per_cluster), 1), len(lines)
        )
        # print(len(lines), kwargs["n_clusters"])
        kwargs["distance_threshold"] = None
    else:
        kwargs.setdefault("n_clusters", None)
        kwargs.setdefault("linkage", "ward")
        kwargs.setdefault("distance_threshold", 5.5)
    labels = cluster.AgglomerativeClustering(**kwargs).fit_predict(vectors)
    # Group matrix lines according to clustering
    grouped_lines: Dict[int, Pairs] = defaultdict(dict)
    ungrouped_lines = []
    for class1, label in zip(all_class1, labels):
        if label == -1:
            ungrouped_lines.append(lines[class1])
        else:
            grouped_lines[label].update(lines[class1])
    return [*grouped_lines.values(), *ungrouped_lines]


# ============================

# NOTE:(jany) I also tried adding the subtable breaks using a custom feature
# writer but it didn't seem to work so I gave up


def add_to_lib(designspace: DesignSpaceDocument, config: Any) -> DesignSpaceDocument:
    for source in designspace.sources:
        for writer in source.font.lib["com.github.googlei18n.ufo2ft.featureWriters"]:
            if writer["class"] == "KernFeatureWriter":
                writer[
                    "module"
                ] = "scripts.measure_kerning_optimizations.compact_kern_feature_writer"
                writer["class"] = "CompactKernFeatureWriter"
                writer["options"]["config"] = config
    return designspace


class CompactKernFeatureWriter(KernFeatureWriter):
    options: SimpleNamespace = {  # type: ignore
        "config": None,
        **KernFeatureWriter.options,
    }

    # Override this method to organize the lookup into subtables that hopefully
    # take less space.
    def _makeKerningLookup(
        self,
        name: str,
        pairs: List[Any],
        exclude: Optional[Callable[[Any], bool]] = None,
        rtl: bool = False,
        ignoreMarks: bool = True,
    ) -> ast.LookupBlock:
        print("Using the custom feature writer!")
        assert pairs
        kept_pairs = []
        for pair in pairs:
            if exclude is not None and exclude(pair):
                self.log.debug("pair excluded from '%s' lookup: %r", name, pair)
                continue
            kept_pairs.append(pair)

        subtables = []
        if self.options.config == "one":
            subtables.append(kept_pairs)
        elif self.options.config == "max":
            # Group pairs by left-hand side then make one subtable per group
            groups = defaultdict(list)
            for pair in kept_pairs:
                groups[pair.side1].append(pair)
            subtables.extend(groups.values())
        elif self.options.config == "auto":
            # TODO: somewhere in the middle
            subtables.append(kept_pairs)

        rules = []
        for i, subtable in enumerate(subtables):
            if i > 0:
                rules.append(ast.SubtableStatement())
            for pair in subtable:
                rules.append(self._makePairPosRule(pair, rtl=rtl))
        if rules:
            lookup = ast.LookupBlock(name)
            if ignoreMarks and self.options.ignoreMarks:
                lookup.statements.append(ast.makeLookupFlag("IgnoreMarks"))
            lookup.statements.extend(rules)
            return lookup
