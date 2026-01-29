#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %% initial imports
import pandas as pd
import numpy as np
import os
import glob

import matplotlib as mpl
import matplotlib.figure as figure
import matplotlib.colors as colors
from matplotlib.ticker import AutoMinorLocator

from IPython.display import display

mpl.rc('text', usetex=True)
mpl.rc('font', family='serif')
mpl.rc('font', size=8)


# %% some fixed parameters, data loading and initial calculations
# name of the resulting file and the experiment name
#exp_desc = 'roaming-patches-l32-even'

local_exp_desc = 'roaming-random-local-l64'
global_exp_desc = 'roaming-random-patches-l64-even'

local_exp_files = glob.glob(os.path.join('data/' , local_exp_desc + "*.csv"))
global_exp_files = glob.glob(os.path.join('data/' , global_exp_desc + "*.csv"))


# data loading

# variables usd in the plots
local_v = ["neighborhood-type", "roaming-agents", "synergy-factor", "mean-cooperators1k"]
global_v = ["random-patches-number", "roaming-agents", "synergy-factor", "mean-cooperators1k"]

# file with data from the experiment
# Note: header=6 is for NetLogo data
local_data = pd.concat([pd.read_csv(f, header=6) for f in local_exp_files], ignore_index=True)
global_data = pd.concat([pd.read_csv(f, header=6) for f in global_exp_files], ignore_index=True)

# data = pd.read_csv('data/' + exp_desc + '.csv', header=6)


# %% local version

# data from used for plots
local_df = pd.DataFrame(columns=local_v)

# we choose only data for no roamin agents in the population
var0s = local_data[local_v[0]].unique()
var1s = [0,0.1,0.4] # NOTE: v1 is always 0 for the verion without the romaing
var2s = local_data[local_v[2]].unique()

# preprocess
for v0 in var0s:
    for v1 in var1s:
        for v2 in var2s: 
          local_df.loc[len(local_df.index)] = [
                v0,
                v1,
                v2,
                local_data[(local_data[local_v[0]] == v0) & (local_data[local_v[1]] == v1) & (local_data[local_v[2]] == v2)]['mean-cooperators1k'].mean()
            ]


# %% global version

# data from used for plots
global_df = pd.DataFrame(columns=global_v)

var0s = global_data[global_v[0]].unique()
var1s = [0, 0.1, 0.4] # NOTE: v1 is always 0 for the verion without the romaing
var2s = global_data[global_v[2]].unique()


# %% preprocess
for v0 in var0s:
    for v1 in var1s:
        for v2 in var2s: 
          global_df.loc[len(global_df.index)] = [
                v0,
                v1,
                v2,
                global_data[(global_data[global_v[0]] == v0) & (global_data[global_v[1]] == v1) & (global_data[global_v[2]] == v2)]['mean-cooperators1k'].mean()
            ]

#%% plot 
var0s = ["random von Neumann", "random Moore", 6, 8 ]


plot_data0 = dict()
plot_data1 = dict()
plot_data2 = dict()

fig = figure.Figure(figsize=(6,5))

for i, v in enumerate(var0s):
    axs = fig.add_subplot(221+i)
    if i <=1:
        plot_data0[v] = local_df[ (local_df[local_v[0]] == v) & (local_df[local_v[1]] == var1s[0]) ][[local_v[2], local_v[3]]].to_numpy()
        plot_data1[v] = local_df[ (local_df[local_v[0]] == v) & (local_df[local_v[1]] == var1s[1]) ][[local_v[2], local_v[3]]].to_numpy()
        plot_data2[v] = local_df[ (local_df[local_v[0]] == v) & (local_df[local_v[1]] == var1s[2]) ][[local_v[2], local_v[3]]].to_numpy()
    else:
        plot_data0[v] = global_df[ (global_df[global_v[0]] == v) & (global_df[global_v[1]] == var1s[0]) ][[global_v[2], global_v[3]]].to_numpy()
        plot_data1[v] = global_df[ (global_df[global_v[0]] == v) & (global_df[global_v[1]] == var1s[1])  ][[global_v[2], global_v[3]]].to_numpy()
        plot_data2[v] = global_df[ (global_df[global_v[0]] == v) & (global_df[global_v[1]] == var1s[2])  ][[global_v[2], global_v[3]]].to_numpy()
        
    axs.plot(plot_data0[v].T[0],plot_data0[v].T[1], ":", color='black', linewidth="1.25")
    axs.plot(plot_data1[v].T[0],plot_data1[v].T[1], "--s", color='green', linewidth="1.25", markerfacecolor="None",  ms='5')
    axs.plot(plot_data2[v].T[0],plot_data2[v].T[1], ":x", color='red',  linewidth=".5",  ms='5')
    
    axs.set_xticks([3,3.5,4,4.5,5,5.5,6])
    axs.set_xlim([2.9,6.1])
    axs.grid(True, which='major',linestyle='-.', linewidth=0.25, c='k', alpha=0.75)
    
    if i in [0,2]:
      axs.set_ylabel(r'fraction of cooperators')
    else:
      axs.set_ylabel('')  
    
    if type(v) == int:
        axs.set_title(r"global romaing, $K="+str(v)+"$", size=8)
    else:
        axs.set_title(str(v), size=8)
      
    if i in [2,3]:
      axs.set_xlabel(r'synergy factor $r$')
    else:
      axs.set_xlabel('')
      
    axs.text(2.4, 1.15, chr(ord('a')+i)+")", ha='center', va='center', size=10)
        
  

fig.tight_layout()
display(fig)

# %% saving
fName = "plots/plot_" + "roaming-vs-static" + ".pdf"
print("[INFO] Saving " + fName)
fig.savefig(fName, format="pdf", bbox_inches='tight')
