import pandas as pd
import os,sys
sys.path.append(os.getenv('FTBASE')+'/babymaking/batch')
import samples
from list_of_samples_forAN import used_mc

def latex_table(filename):
    pd.set_option('max_colwidth', -1)

    # read in
    f = open(filename,"r")
    lines = f.readlines()
    f.close()

    # gets info of all samples
    all_samples = []
    for row in lines[3:]:
        entry = row.split()
        # cleans up entries
        if len(entry) == 7:
            entry = entry[:-1]
        all_samples.append(entry)

    used_names = {2016:[],2017:[],2018:[]}
    s_mc = {2016:samples.mc_2016_94x, 2017:samples.mc_2017, 2018:samples.mc_2018}

    # matches mc name to sample name
    for year in [2016,2017,2018]:
        for mc in used_mc[year]:
            for s in s_mc[year]:
                if mc == s[1] and s[0] not in used_names[year]:
                    used_names[year].append(s[0])
                    break

    # matches sample name to sample info, write out tables
    used_samples = {2016:[],2017:[],2018:[]}
    cols = ["sample", "neventstotal", "xsec", "lumi"]

    for year in [2016,2017,2018]:
        for name in used_names[year]:
            for s in all_samples:
                if name == s[0]:
                    used_samples[year].append(s)
                    break
        used_samples[year] = [[entry[0].split("/")[1], entry[2], entry[4], str('%.2g' % (float(entry[5])**-1))] for entry in used_samples[year]]
        df = pd.DataFrame(used_samples[year], columns=cols)
        out = open("table_{year}.tex".format(year=year), "w")
        out.write(df.to_latex(index=False))
        out.close()

if __name__ == "__main__":
    latex_table(os.getenv('FTBASE')+'/common/CORE/Tools/datasetinfo/scale1fbs.txt')
