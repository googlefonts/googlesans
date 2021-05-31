# Kerning optimization

## How to run

From the top-level:
1. make sure you have a venv with `requirements-dev.txt`, e.g. by running `make setup`
2. activate the venv
3. run the python module `scripts.measure_kerning_optimizations`

```bash
make setup
source .venv/bin/activate
python3 -m scripts.measure_kerning_optimizations
```

## Extract AOSP app strings

The script downloads a few Android apps from Google's Git repositories, finds
`strings.xml` resource files and extracts text runs from these. The results are
written to the JSON file `scripts/measure_kerning_optimizations/aosp.json`.

In the JSON file, keys are strings and values contain information about the
origin of the string (apps and languages).

```bash
python scripts/measure_kerning_optimizations/extract_aosp_strings/extract_strings.py
```
