'''

Build TeX tables of various process yields for the H2Tau analysis.

Yields + uncertainties are taken from the data card.  Requires a single .txt
card with all channels.  You can build it in the correct format with:

    combine_cards_with_names.sh MY-LIMIT/cmb/125/*txt > megacard.txt

where MY-LIMIT is the output directory of setup-htt.py

And then create the tables with

    python h2tau_tables.py

which will create

    em_yields_table.tex
    et_yields_table.tex
    mm_yields_table.tex
    mt_yields_table.tex

Author: Evan K. Friis, UW Madison
'''

import math
from HiggsAnalysis.HiggsToTauTau.DataCard import DataCard
from HiggsAnalysis.HiggsToTauTau.sigfigs import sigfigs

dc = DataCard('megacard.txt')

def quad(*xs):
    return math.sqrt(sum(x*x for x in xs))

def render(x):
    ''' Render x (an uncertainties object) with correct sig figs '''
    if isinstance(x, int):
        return '%i' % x
    else:
        #return r'$%s \pm %s$' % (int(x.nominal_value), int(x.std_dev()))
        # Never round greater than unity.  Always include at least 1 sig digit.
        return r'$%s \pm %s$' % (sigfigs(x.nominal_value, x.std_dev(), 1, max_sig_fig=0))

def render_values(table):
    # Convert all objects to strings
    output = {}
    for field in table.keys():
        output[field] = render(table[field])
    return output

def add_up_backgrounds(table, bkgs=('ZTT', 'QCD', 'Wjets', 'ZJ', 'TT', 'VV')):
    ''' Add up the total bkg contribution '''
    for category in ['inc', 'boost', 'vbf']:
        result = sum(table[category + x] for x in bkgs)
        table[category + 'Total'] = result


tables = {}

###### MT Channel

et_mt_template = r'''
Process & \textit{{0-Jet}} & Boosted & VBF \\
\hline
Z$\to\tau\tau$ & {incZTT} & {boostZTT} & {vbfZTT} \\
\hline
QCD & {incQCD} & {boostQCD} & {vbfQCD} \\
\hline
W+jets & {incWjets} & {boostWjets} & {vbfWjets} \\
\hline
Z+jets (l/jet faking $\tau$) & {incZJ} & {boostZJ} & {vbfZJ} \\
\hline
$\ttbar$ & {incTT} & {boostTT} & {vbfTT} \\
\hline
Dibosons & {incVV} & {boostVV} & {vbfVV} \\
\hline
\hline
Total Background & {incTotal} & {boostTotal} & {vbfTotal} \\
\hline
H$\to\tau\tau$ & {incHTT} & {boostHTT} & {vbfHTT} \\
\hline
Data & {incData} & {boostData} & {vbfData} \\
'''

# Define which sets of bins corresponds to table categories
mt_0jet_bins = ['htt_mt_0_*', 'htt_mt_1_*']
mt_boost_bins = ['htt_mt_2_*', 'htt_mt_3_*']
mt_vbf_bins = ['htt_mt_5_*']

tables['mt'] = {
    'incZTT' : dc.get_rate(mt_0jet_bins, 'ZTT'),
    'boostZTT' : dc.get_rate(mt_boost_bins, 'ZTT'),
    'vbfZTT' : dc.get_rate(mt_vbf_bins, 'ZTT'),

    'incQCD' : dc.get_rate(mt_0jet_bins, 'QCD'),
    'boostQCD' : dc.get_rate(mt_boost_bins, 'QCD'),
    'vbfQCD' : dc.get_rate(mt_vbf_bins, 'QCD'),

    'incWjets' : dc.get_rate(mt_0jet_bins, 'W'),
    'boostWjets' : dc.get_rate(mt_boost_bins, 'W'),
    'vbfWjets' : dc.get_rate(mt_vbf_bins, 'W'),

    'incZJ' : dc.get_rate(mt_0jet_bins, 'ZJ') + dc.get_rate(mt_0jet_bins, 'ZL'),
    'boostZJ' : dc.get_rate(mt_boost_bins, 'ZJ') + dc.get_rate(mt_boost_bins, 'ZL'),
    'vbfZJ' : dc.get_rate(mt_vbf_bins, 'ZLL'),

    'incTT' : dc.get_rate(mt_0jet_bins, 'TT'),
    'boostTT' : dc.get_rate(mt_boost_bins, 'TT'),
    'vbfTT' : dc.get_rate(mt_vbf_bins, 'TT'),

    'incVV' : dc.get_rate(mt_0jet_bins, 'VV'),
    'boostVV' : dc.get_rate(mt_boost_bins, 'VV'),
    'vbfVV' : dc.get_rate(mt_vbf_bins, 'VV'),

    'incHTT' : dc.get_rate(mt_0jet_bins, 'ggH') + dc.get_rate(mt_0jet_bins, 'qqH') + dc.get_rate(mt_0jet_bins, 'VH'),
    'boostHTT' : dc.get_rate(mt_boost_bins, 'ggH') + dc.get_rate(mt_boost_bins, 'qqH') + dc.get_rate(mt_boost_bins, 'VH'),
    'vbfHTT' : dc.get_rate(mt_vbf_bins, 'ggH') + dc.get_rate(mt_vbf_bins, 'qqH') + dc.get_rate(mt_vbf_bins, 'VH'),

    'incData' : dc.get_obs(mt_0jet_bins),
    'boostData' : dc.get_obs(mt_boost_bins),
    'vbfData' : dc.get_obs(mt_vbf_bins),
}
add_up_backgrounds(tables['mt'])

dc.print_systematics(mt_0jet_bins, 'QCD'),

with open('mt_yields_table.tex', 'w') as file:
    file.write(et_mt_template.format(**render_values(tables['mt'])))

###### ET Channel

et_0jet_bins = ['htt_et_0_*', 'htt_et_1_*']
et_boost_bins = ['htt_et_2_*', 'htt_et_3_*']
et_vbf_bins = ['htt_et_5_*']

tables['et'] = {
    'incZTT' : dc.get_rate(et_0jet_bins, 'ZTT'),
    'boostZTT' : dc.get_rate(et_boost_bins, 'ZTT'),
    'vbfZTT' : dc.get_rate(et_vbf_bins, 'ZTT'),

    'incQCD' : dc.get_rate(et_0jet_bins, 'QCD'),
    'boostQCD' : dc.get_rate(et_boost_bins, 'QCD'),
    'vbfQCD' : dc.get_rate(et_vbf_bins, 'QCD'),

    'incWjets' : dc.get_rate(et_0jet_bins, 'W'),
    'boostWjets' : dc.get_rate(et_boost_bins, 'W'),
    'vbfWjets' : dc.get_rate(et_vbf_bins, 'W'),

    'incZJ' : dc.get_rate(et_0jet_bins, 'ZJ') + dc.get_rate(et_0jet_bins, 'ZL'),
    'boostZJ' : dc.get_rate(et_boost_bins, 'ZJ') + dc.get_rate(et_boost_bins, 'ZL'),
    'vbfZJ' : dc.get_rate(et_vbf_bins, 'ZLL'),

    'incTT' : dc.get_rate(et_0jet_bins, 'TT'),
    'boostTT' : dc.get_rate(et_boost_bins, 'TT'),
    'vbfTT' : dc.get_rate(et_vbf_bins, 'TT'),

    'incVV' : dc.get_rate(et_0jet_bins, 'VV'),
    'boostVV' : dc.get_rate(et_boost_bins, 'VV'),
    'vbfVV' : dc.get_rate(et_vbf_bins, 'VV'),

    'incHTT' : dc.get_rate(et_0jet_bins, 'ggH') + dc.get_rate(et_0jet_bins, 'qqH') + dc.get_rate(et_0jet_bins, 'VH'),
    'boostHTT' : dc.get_rate(et_boost_bins, 'ggH') + dc.get_rate(et_boost_bins, 'qqH') + dc.get_rate(et_boost_bins, 'VH'),
    'vbfHTT' : dc.get_rate(et_vbf_bins, 'ggH') + dc.get_rate(et_vbf_bins, 'qqH') + dc.get_rate(et_vbf_bins, 'VH'),

    'incData' : dc.get_obs(et_0jet_bins),
    'boostData' : dc.get_obs(et_boost_bins),
    'vbfData' : dc.get_obs(et_vbf_bins),
}
add_up_backgrounds(tables['et'])

with open('et_yields_table.tex', 'w') as file:
    file.write(et_mt_template.format(**render_values(tables['et'])))

###### EM Channel

em_template = r'''
Process & \textit{{0-Jet}} & Boosted & VBF \\
\hline
Z$\to\tau\tau$ & {incZTT} & {boostZTT} & {vbfZTT} \\
\hline
QCD & {incQCD} & {boostQCD} & {vbfQCD} \\
\hline
$\ttbar$ & {incTT} & {boostTT} & {vbfTT} \\
\hline
Dibosons & {incVV} & {boostVV} & {vbfVV} \\
\hline
\hline
Total Background & {incTotal} & {boostTotal} & {vbfTotal} \\
\hline
H$\to\tau\tau$ & {incHTT} & {boostHTT} & {vbfHTT} \\
\hline
Data & {incData} & {boostData} & {vbfData} \\
'''

em_0jet_bins = ['htt_em_0_*', 'htt_em_1_*']
em_boost_bins = ['htt_em_2_*', 'htt_em_3_*']
em_vbf_bins = ['htt_em_5_*']

tables['em'] = {
    'incZTT' : dc.get_rate(em_0jet_bins, 'Ztt'),
    'boostZTT' : dc.get_rate(em_boost_bins, 'Ztt'),
    'vbfZTT' : dc.get_rate(em_vbf_bins, 'Ztt'),

    'incQCD' : dc.get_rate(em_0jet_bins, 'Fakes'),
    'boostQCD' : dc.get_rate(em_boost_bins, 'Fakes'),
    'vbfQCD' : dc.get_rate(em_vbf_bins, 'Fakes'),

    'incTT' : dc.get_rate(em_0jet_bins, 'ttbar'),
    'boostTT' : dc.get_rate(em_boost_bins, 'ttbar'),
    'vbfTT' : dc.get_rate(em_vbf_bins, 'ttbar'),

    'incVV' : dc.get_rate(em_0jet_bins, 'EWK'),
    'boostVV' : dc.get_rate(em_boost_bins, 'EWK'),
    'vbfVV' : dc.get_rate(em_vbf_bins, 'EWK'),

    'incHTT' : dc.get_rate(em_0jet_bins, 'ggH') + dc.get_rate(em_0jet_bins, 'qqH') + dc.get_rate(em_0jet_bins, 'VH'),
    'boostHTT' : dc.get_rate(em_boost_bins, 'ggH') + dc.get_rate(em_boost_bins, 'qqH') + dc.get_rate(em_boost_bins, 'VH'),
    'vbfHTT' : dc.get_rate(em_vbf_bins, 'ggH') + dc.get_rate(em_vbf_bins, 'qqH') + dc.get_rate(em_vbf_bins, 'VH'),

    'incData' : dc.get_obs(em_0jet_bins),
    'boostData' : dc.get_obs(em_boost_bins),
    'vbfData' : dc.get_obs(em_vbf_bins),
}
add_up_backgrounds(tables['em'], bkgs=('ZTT', 'QCD', 'TT', 'VV'))

with open('em_yields_table.tex', 'w') as file:
    file.write(em_template.format(**render_values(tables['em'])))

###### MM Channel

mm_template = r'''
Process & \textit{{0-Jet}} & Boosted & VBF \\
\hline
Z$\to\tau\tau$ & {incZTT} & {boostZTT} & {vbfZTT} \\
\hline
QCD & {incQCD} & {boostQCD} & {vbfQCD} \\
\hline
W+jets & {incWjets} & {boostWjets} & {vbfWjets} \\
\hline
Z$\to\mu\mu$ & {incZJ} & {boostZJ} & {vbfZJ} \\
\hline
$\ttbar$ & {incTT} & {boostTT} & {vbfTT} \\
\hline
Dibosons & {incVV} & {boostVV} & {vbfVV} \\
\hline
\hline
Total Background & {incTotal} & {boostTotal} & {vbfTotal} \\
\hline
H$\to\tau\tau$ & {incHTT} & {boostHTT} & {vbfHTT} \\
\hline
Data & {incData} & {boostData} & {vbfData} \\
'''

mm_0jet_bins = ['htt_mm_0_*', 'htt_mm_1_*']
mm_boost_bins = ['htt_mm_2_*', 'htt_mm_3_*']
mm_vbf_bins = ['htt_mm_5_*']

tables['mm'] = {
    'incZTT' : dc.get_rate(mm_0jet_bins, 'ZTT'),
    'boostZTT' : dc.get_rate(mm_boost_bins, 'ZTT'),
    'vbfZTT' : dc.get_rate(mm_vbf_bins, 'ZTT'),

    'incQCD' : dc.get_rate(mm_0jet_bins, 'QCD'),
    'boostQCD' : dc.get_rate(mm_boost_bins, 'QCD'),
    'vbfQCD' : dc.get_rate(mm_vbf_bins, 'QCD'),

    'incWjets' : dc.get_rate(mm_0jet_bins, 'WJets'),
    'boostWjets' : dc.get_rate(mm_boost_bins, 'WJets'),
    'vbfWjets' : dc.get_rate(mm_vbf_bins, 'WJets'),

    'incZJ' : dc.get_rate(mm_0jet_bins, 'ZMM'),
    'boostZJ' : dc.get_rate(mm_boost_bins, 'ZMM'),
    'vbfZJ' : dc.get_rate(mm_vbf_bins, 'ZMM'),

    'incTT' : dc.get_rate(mm_0jet_bins, 'TTJ'),
    'boostTT' : dc.get_rate(mm_boost_bins, 'TTJ'),
    'vbfTT' : dc.get_rate(mm_vbf_bins, 'TTJ'),

    'incVV' : dc.get_rate(mm_0jet_bins, 'Dibosons'),
    'boostVV' : dc.get_rate(mm_boost_bins, 'Dibosons'),
    'vbfVV' : dc.get_rate(mm_vbf_bins, 'Dibosons'),

    'incHTT' : dc.get_rate(mm_0jet_bins, 'ggH') + dc.get_rate(mm_0jet_bins, 'qqH') + dc.get_rate(mm_0jet_bins, 'VH'),
    'boostHTT' : dc.get_rate(mm_boost_bins, 'ggH') + dc.get_rate(mm_boost_bins, 'qqH') + dc.get_rate(mm_boost_bins, 'VH'),
    'vbfHTT' : dc.get_rate(mm_vbf_bins, 'ggH') + dc.get_rate(mm_vbf_bins, 'qqH') + dc.get_rate(mm_vbf_bins, 'VH'),

    'incData' : dc.get_obs(mm_0jet_bins),
    'boostData' : dc.get_obs(mm_boost_bins),
    'vbfData' : dc.get_obs(mm_vbf_bins),
}
add_up_backgrounds(tables['mm'])

with open('mm_yields_table.tex', 'w') as file:
    file.write(mm_template.format(**render_values(tables['mm'])))

# Some debugging for Colin
with open('debug_tables_boost.txt', 'w') as debug_file:
    debug_file.write("Problem: Boosted QCD should be > 10% (SS/OS ratio)\n")
    debug_file.write("ETau boosted QCD\n")
    dc.print_systematics(et_boost_bins, 'QCD', stream=debug_file)

    debug_file.write("\nHypothesis: effect due to fact that SS/OS is uncorrelated between all channels\n")
    debug_file.write("Effect in each category:\n")

    debug_file.write("\nETau boosted QCD 8TeV only\n")
    dc.print_systematics(['htt_et_2_8TeV', 'htt_et_3_8TeV'], 'QCD', stream=debug_file)

    debug_file.write("\nETau boosted QCD 8TeV, high pt only\n")
    dc.print_systematics(['htt_et_2_8TeV'], 'QCD', stream=debug_file)

    debug_file.write("\nETau boosted QCD 8TeV, low pt only\n")
    dc.print_systematics(['htt_et_3_8TeV'], 'QCD', stream=debug_file)

    debug_file.write("\nETau boosted QCD 7TeV, high pt only\n")
    dc.print_systematics(['htt_et_2_7TeV'], 'QCD', stream=debug_file)

    debug_file.write("\nETau boosted QCD 8TeV, low pt only\n")
    dc.print_systematics(['htt_et_3_7TeV'], 'QCD', stream=debug_file)

    debug_file.write("\nIgnorning effect of correlated b systematics, add in quad:\n")
    qcd_uncertainties = [25, 22, 9.8, 8.9, 4.27]
    debug_file.write(" ++ ".join(str(x) for x in qcd_uncertainties) + " = %0.1f\n" % quad(*qcd_uncertainties))
    debug_file.write("Summed error is less than 10% (36/460 total) due to uncorrelation\n")

with open('debug_tables_vbf.txt', 'w') as debug_file:
    debug_file.write("\n\nProblem: VBF QCD should be as for Boosted (SS/OS ratio), now is much larger\n")
    debug_file.write("ETau VBF QCD\n")
    dc.print_systematics(et_vbf_bins, 'QCD', stream=debug_file)

    debug_file.write("\nETau VBF QCD 8TeV only\n")
    dc.print_systematics(['htt_et_5_8TeV'], 'QCD', stream=debug_file)
    debug_file.write("\n\nToo me looks as though the uncertainty is 30\%, gets knocked down to do quadrature sum effects\n")

with open('debug_tables_zll.txt', 'w') as debug_file:
    debug_file.write("Problem: Z+jets (l->tau) should be > 30% for all categories\n")
    debug_file.write("NB that we add (l->tau) and (jet->tau) together for these tables...\n")
    debug_file.write("\n\n")
    debug_file.write("ETau 0jet ZL (SEPARATE from ZJ)\n")
    dc.print_systematics(et_0jet_bins, 'ZL', stream=debug_file)

    debug_file.write("ETau 0jet ZL 8TeV only (SEPARATE from ZJ)\n")
    dc.print_systematics([x + '8TeV' for x in et_0jet_bins], 'ZL', stream=debug_file)

    debug_file.write("\nETau 0jet ZJ (SEPARATE from ZL)\n")
    dc.print_systematics(et_0jet_bins, 'ZJ', stream=debug_file)

    debug_file.write("\n\n")
    debug_file.write("ETau boost ZL (SEPARATE from ZJ)\n")
    dc.print_systematics(et_boost_bins, 'ZL', stream=debug_file)
    debug_file.write("\nETau boost ZJ (SEPARATE from ZL)\n")
    dc.print_systematics(et_boost_bins, 'ZJ', stream=debug_file)

    debug_file.write("\n\n")
    debug_file.write("ETau VBF ZLL (ZL + ZJ together)\n")
    dc.print_systematics(et_vbf_bins, 'ZLL', stream=debug_file)

    debug_file.write("\n\n")
    debug_file.write("ETau VBF ZLL (ZL + ZJ together) 8TeV\n")
    dc.print_systematics([x + '8TeV' for x in et_vbf_bins], 'ZLL', stream=debug_file)


    debug_file.write("\n\n")
    debug_file.write("MTau VBF ZLL (ZL + ZJ togmther)\n")
    dc.print_systematics(mt_vbf_bins, 'ZLL', stream=debug_file)

    debug_file.write("\n\n")
    debug_file.write("MTau VBF ZLL (ZL + ZJ togmther) 8TeV\n")
    dc.print_systematics([x + '8TeV' for x in mt_vbf_bins], 'ZLL', stream=debug_file)

