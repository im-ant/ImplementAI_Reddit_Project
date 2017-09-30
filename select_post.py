#!/usr/local/bin/python3
import json
import pandas as pd
import re
import sys

## select posts relevant to the company and save in dictionary form. company per list of post.
fp = sys.argv[1] # input file path
fout = sys.argv[2] #output file path

df = pd.read_csv('/data/ImplementReddit/companies/constituents.csv')
symb_name = {}
for line in df[['Symbol', 'Name']].values:
    name = line[1].lower()
    name_ = re.sub(r'(\scorp.{2}|\sinc.*|\scos.*|\&\sco.*|\sco.*|ltd.|the\s)',"",name) # strip off the Inc/Corp stuff
    symb_name[line[0].lower()] = name_
symbs = set(symb_name.keys())
names =  set(symb_name.values())
print("Total %s companies to consider"%(len(symbs)))

count = 0
data_company = {} # {company_name: [post1, post2...]}
data = []
with open(fp) as f:
    for line in f:
        d = json.loads(line) 
        title = d["title"].lower()
        if set(title.split()).intersection(names):
            comps = set(title.split()).intersection(names)
            # print(comps)
            count += 1
            for comp in comps:
                if not data_company.get(comp):
                    data_company[comp] = [d]
                else:
                    data_company[comp].append(d)
print(" Selected %s posts from %s"%(count, fp))

json.dump(data_company, open(fout,"w"))
