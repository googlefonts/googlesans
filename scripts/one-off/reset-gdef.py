# flake8: noqa
# Copyright 2022 Google Sans Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

from ufoLib2 import Font


ALL_GLYPHS = set(
    """combiningAnusvara-malayalam
candrabindu-malayalam
anusvara-malayalam
visarga-malayalam
vedicanusvara-malayalam
a-malayalam
aa-malayalam
i-malayalam
ii-malayalam
u-malayalam
uu-malayalam
rVocalic-malayalam
lVocalic-malayalam
e-malayalam
ee-malayalam
ai-malayalam
o-malayalam
oo-malayalam
au-malayalam
ka-malayalam
kha-malayalam
ga-malayalam
gha-malayalam
nga-malayalam
ca-malayalam
cha-malayalam
ja-malayalam
jha-malayalam
nya-malayalam
tta-malayalam
ttha-malayalam
dda-malayalam
ddha-malayalam
nna-malayalam
ta-malayalam
tha-malayalam
da-malayalam
dha-malayalam
na-malayalam
nnna-malayalam
pa-malayalam
pha-malayalam
ba-malayalam
bha-malayalam
ma-malayalam
ya-malayalam
ra-malayalam
rra-malayalam
la-malayalam
lla-malayalam
llla-malayalam
va-malayalam
sha-malayalam
ssa-malayalam
sa-malayalam
ha-malayalam
ttta-malayalam
verticalBarVirama-malayalam
circularVirama-malayalam
avagraha-malayalam
aaMatra-malayalam
iMatra-malayalam
iiMatra-malayalam
uMatra-malayalam
uuMatra-malayalam
rVocalicMatra-malayalam
rrVocalicMatra-malayalam
eMatra-malayalam
eeMatra-malayalam
aiMatra-malayalam
oMatra-malayalam
ooMatra-malayalam
auMatra-malayalam
halant-malayalam
dotreph-malayalam
para-malayalam
mChillu-malayalam
yChillu-malayalam
lllChillu-malayalam
aulengthmark-malayalam
onehundredsixtieth-malayalam
onefortieth-malayalam
threeeights-malayalam
onetwentieth-malayalam
onetenth-malayalam
onetwentieths-malayalam
onefifth-malayalam
archaicii-malayalam
rrVocalic-malayalam
llVocalic-malayalam
lVocalicMatra-malayalam
llVocalicMatra-malayalam
zero-malayalam
one-malayalam
two-malayalam
three-malayalam
four-malayalam
five-malayalam
six-malayalam
seven-malayalam
eight-malayalam
nine-malayalam
ten-malayalam
onehundred-malayalam
onethousand-malayalam
onequarter-malayalam
onehalf-malayalam
threequarters-malayalam
onesixteenth-malayalam
oneeighth-malayalam
threesixteenths-malayalam
datemark-malayalam
nnChillu-malayalam
nChillu-malayalam
rrChillu-malayalam
lChillu-malayalam
llChillu-malayalam
kChillu-malayalam
ya-malayalam.post
va-malayalam.post
ra-malayalam.pres
ka-malayalam.half
kha-malayalam.half
ga-malayalam.half
gha-malayalam.half
nga-malayalam.half
ca-malayalam.half
cha-malayalam.half
ja-malayalam.half
jha-malayalam.half
nya-malayalam.half
tta-malayalam.half
ttha-malayalam.half
dda-malayalam.half
ddha-malayalam.half
nna-malayalam.half
ta-malayalam.half
tha-malayalam.half
da-malayalam.half
dha-malayalam.half
na-malayalam.half
pa-malayalam.half
pha-malayalam.half
ba-malayalam.half
bha-malayalam.half
ma-malayalam.half
ya-malayalam.half
ra-malayalam.half
rra-malayalam.half
la-malayalam.half
lla-malayalam.half
llla-malayalam.half
va-malayalam.half
sha-malayalam.half
ssa-malayalam.half
sa-malayalam.half
ha-malayalam.half
k_ssa-malayalam.half
k_ka-malayalam
k_ta-malayalam
k_tta-malayalam
k_la-malayalam
k_ssa-malayalam
g_ga-malayalam
g_da-malayalam
g_ma-malayalam
g_na-malayalam
g_la-malayalam
ng_ka-malayalam
ng_k_la-malayalam
ng_nga-malayalam
c_ca-malayalam
c_cha-malayalam
j_ja-malayalam
j_nya-malayalam
ny_ca-malayalam
ny_cha-malayalam
ny_ja-malayalam
ny_nya-malayalam
tt_tta-malayalam
dd_dda-malayalam
dd_ddha-malayalam
nn_dda-malayalam
nn_ddha-malayalam
nn_ma-malayalam
nn_nna-malayalam
nn_tta-malayalam
t_na-malayalam
t_bha-malayalam
t_ma-malayalam
t_sa-malayalam
t_ta-malayalam
t_tha-malayalam
t_la-malayalam
d_da-malayalam
d_dha-malayalam
n_da-malayalam
n_dha-malayalam
n_na-malayalam
n_ma-malayalam
n_rra-malayalam
n_ta-malayalam
n_tha-malayalam
p_ta-malayalam
p_pa-malayalam
p_la-malayalam
ph_la-malayalam
b_ba-malayalam
b_da-malayalam
b_dha-malayalam
b_la-malayalam
m_ma-malayalam
m_pa-malayalam
m_p_la-malayalam
m_la-malayalam
y_ya-malayalam
rr_rra-malayalam
l_pa-malayalam
l_la-malayalam
ll_lla-malayalam
v_la-malayalam
v_va-malayalam
sh_ca-malayalam
sh_cha-malayalam
sh_sha-malayalam
sh_la-malayalam
ss_tta-malayalam
s_sa-malayalam
s_tha-malayalam
s_rr_rra-malayalam
s_la-malayalam
h_ma-malayalam
h_na-malayalam
h_la-malayalam
ja_lVocalicMatra-malayalam
tta_lVocalicMatra-malayalam
ttha_lVocalicMatra-malayalam
da_lVocalicMatra-malayalam
bha_lVocalicMatra-malayalam
ma_lVocalicMatra-malayalam
ra_lVocalicMatra-malayalam
rra_lVocalicMatra-malayalam
llla_lVocalicMatra-malayalam
ja_llVocalicMatra-malayalam
tta_llVocalicMatra-malayalam
ttha_llVocalicMatra-malayalam
da_llVocalicMatra-malayalam
bha_llVocalicMatra-malayalam
ma_llVocalicMatra-malayalam
ra_llVocalicMatra-malayalam
rra_llVocalicMatra-malayalam
llla_llVocalicMatra-malayalam
danda-deva.loclMALM
dbldanda-deva.loclMALM
period.loclMALM
comma.loclMALM
colon.loclMALM
semicolon.loclMALM
ellipsis.loclMALM
exclam.loclMALM
question.loclMALM
asterisk.loclMALM
parenleft.loclMALM
parenright.loclMALM
braceleft.loclMALM
braceright.loclMALM
bracketleft.loclMALM
bracketright.loclMALM
quotedblleft.loclMALM
quotedblright.loclMALM
quoteleft.loclMALM
quoteright.loclMALM""".split()
)

BASES = set(
    "dottedCircle a-malayalam aa-malayalam i-malayalam u-malayalam rVocalic-malayalam lVocalic-malayalam e-malayalam ee-malayalam o-malayalam ka-malayalam kha-malayalam ga-malayalam gha-malayalam nga-malayalam ca-malayalam cha-malayalam ja-malayalam jha-malayalam nya-malayalam tta-malayalam ttha-malayalam dda-malayalam ddha-malayalam nna-malayalam ta-malayalam tha-malayalam da-malayalam dha-malayalam na-malayalam nnna-malayalam pa-malayalam pha-malayalam ba-malayalam bha-malayalam ma-malayalam ya-malayalam ra-malayalam rra-malayalam la-malayalam lla-malayalam llla-malayalam va-malayalam sha-malayalam ssa-malayalam sa-malayalam ha-malayalam ttta-malayalam mChillu-malayalam yChillu-malayalam lllChillu-malayalam rrVocalic-malayalam llVocalic-malayalam nnChillu-malayalam nChillu-malayalam rrChillu-malayalam lChillu-malayalam llChillu-malayalam kChillu-malayalam k_ka-malayalam k_ta-malayalam k_tta-malayalam k_la-malayalam k_ssa-malayalam g_ga-malayalam g_da-malayalam g_ma-malayalam g_na-malayalam g_la-malayalam ng_ka-malayalam ng_k_la-malayalam ng_nga-malayalam c_ca-malayalam c_cha-malayalam j_ja-malayalam j_nya-malayalam ny_ca-malayalam ny_cha-malayalam ny_ja-malayalam ny_nya-malayalam tt_tta-malayalam dd_dda-malayalam dd_ddha-malayalam nn_dda-malayalam nn_ddha-malayalam nn_ma-malayalam nn_nna-malayalam nn_tta-malayalam t_na-malayalam t_bha-malayalam t_ma-malayalam t_sa-malayalam t_ta-malayalam t_tha-malayalam t_la-malayalam d_da-malayalam d_dha-malayalam n_da-malayalam n_dha-malayalam n_na-malayalam n_ma-malayalam n_rra-malayalam n_ta-malayalam n_tha-malayalam p_la-malayalam ph_la-malayalam b_ba-malayalam b_da-malayalam b_dha-malayalam b_la-malayalam m_ma-malayalam m_pa-malayalam m_p_la-malayalam m_la-malayalam y_ya-malayalam l_la-malayalam ll_lla-malayalam v_la-malayalam v_va-malayalam sh_ca-malayalam sh_cha-malayalam sh_sha-malayalam sh_la-malayalam ss_tta-malayalam s_tha-malayalam s_rr_rra-malayalam s_la-malayalam h_ma-malayalam h_na-malayalam h_la-malayalam tta_lVocalicMatra-malayalam da_lVocalicMatra-malayalam bha_lVocalicMatra-malayalam ra_lVocalicMatra-malayalam rra_lVocalicMatra-malayalam llla_lVocalicMatra-malayalam da_llVocalicMatra-malayalam ra_llVocalicMatra-malayalam rra_llVocalicMatra-malayalam".split()
)

MARKS = set(
    "combiningAnusvara-malayalam candrabindu-malayalam verticalBarVirama-malayalam circularVirama-malayalam halant-malayalam lVocalicMatra-malayalam llVocalicMatra-malayalam".split()
)

for path in Path("source/GoogleSans/").glob("*.ufo"):
    ufo = Font.open(path)
    otc = ufo.lib["public.openTypeCategories"]

    for name in ALL_GLYPHS:
        if name in otc:
            del otc[name]
    otc.update({k: "base" for k in BASES})
    otc.update({k: "mark" for k in MARKS})

    ufo.save()
