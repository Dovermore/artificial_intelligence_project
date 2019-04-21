import pandas as pd
import matplotlib.pyplot as plt
import re

map_length = 16
token = ':'
comment = '#'
name = 'name'
path = "/Users/chuan/Project/artificial_intelligence_project/outputs/"

#%% Read in data
data = list()
with open(path + 'analysis.txt') as f:
    while True:
        # reached end of the line
        line = f.readline()
        if not line:
            break
        # store information
        map_info = dict()
        # read in the map
        diagram = list()
        for i in range(map_length):
            diagram.append(line)
            line = f.readline()
        map_info['diagram'] = ''.join(diagram)
        # skip everything else
        while line[0] == comment:
            line = f.readline()
        # read in the important information
        for i in range(3):
            key, value = line[:-1].split(token)
            if key == 'name':
                a = re.match(r".*sample(\d*).json", value)
                value = a.group(1)
            map_info[key] = value
            line = f.readline()
        while line and line[0] != comment:
            line = f.readline()
        # store
        data.append(map_info)

#%% Clean
types = {'n_nodes' : int, 'n_steps' : int, 'name' : str, 'diagram' : str}
df = pd.DataFrame(data)
print(df.columns)
df = df.astype(types, copy=True)

#%% Analysis
df.plot.scatter(x='n_steps', y='n_nodes')
# add annotations one by one with a loop
for i in df.index:
     plt.annotate(df.loc[i, 'name'], (df.loc[i, 'n_steps']+0.2, df.loc[i, 'n_nodes']))
plt.savefig(path + 'n_nodes vs n_steps')

#%% print row
def print_row(s):
    print("*****"*10)
    print(s.diagram)
    print('n_nodes', s.n_nodes)
    print('n_steps', s.n_steps)


#%%
outliers = [19, 21, 12]
for n in outliers:
    row  = df.loc[n-1, :]
    print_row(row)


#%%test
test = ' ../tests/part_a/sample1.json'
a = re.match(r".*sample(\d*).json", test)
print(a.group(1))