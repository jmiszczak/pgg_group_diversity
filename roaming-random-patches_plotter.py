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

exp_desc = 'roaming-patches-l32-even'

exp_files = glob.glob(os.path.join('data/' , exp_desc + "*.csv"))

# exp_files = [exp_desc, exp_desc + '-batch2',  exp_desc + '-batch3' ]


# data loading

# variables usd in the plots
v = ["random-patches-number", "roaming-agents", "synergy-factor", "mean-cooperators1k"]

# file with data from the experiment
# Note: header=6 is for NetLogo data
data = pd.concat([pd.read_csv(f, header=6) for f in exp_files], ignore_index=True)

# data = pd.read_csv('data/' + exp_desc + '.csv', header=6)

# data from used for plots
df = pd.DataFrame(columns=v)
var0s = data[v[0]].unique()
var1s = data[v[1]].unique()
var2s = data[v[2]].unique()

# %% preprocess
for v0 in var0s:
    for v1 in var1s:
        for v2 in var2s: 
          df.loc[len(df.index)] = [
                v0,
                v1,
                v2,
                data[(data[v[0]] == v0) & (data[v[1]] == v1) & (data[v[2]] == v2)]['mean-cooperators1k'].mean()
            ]


#%% plot 
var0s = np.array([4,6,8,10])
levels = [0, 0.1, 0.5, 0.75, 0.9, 0.95, 0.98, 1]

plotColors = ['orange', 'red', 
              'tomato', 'yellow', 
              'palegreen', 'lightblue', 
              'white']
cmap, norm = colors.from_levels_and_colors(levels, plotColors)

# contained for plotted data
plot_data = dict()

# one figure for all cases of v0
fig = figure.Figure(figsize=(6,5))

# Note: this dependes on the desired results
k_vals = [4,6]

for i, v0 in enumerate(k_vals):
  # Note: 3*2 is the number of cases for var0s 
  axs = fig.add_subplot(221+i)
 
  plot_data[v0] = df[df[v[0]] == v0][[v[1], v[2], v[3]]].to_numpy()

  axs.contour(
    plot_data[v0].T[0].reshape((len(var1s),len(var2s))),
    plot_data[v0].T[1].reshape((len(var1s),len(var2s))),
    plot_data[v0].T[2].reshape((len(var1s),len(var2s))),
    levels=levels[1::],
    linestyles='dashed',
    linewidths=.75,
    colors = ['black']
    )

  im = axs.contourf(
    plot_data[v0].T[0].reshape((len(var1s),len(var2s))),
    plot_data[v0].T[1].reshape((len(var1s),len(var2s))),
    plot_data[v0].T[2].reshape((len(var1s),len(var2s))),
    levels=levels,
    cmap = cmap,
    norm = norm
    )

  axs.set_yticks([3,4,5,6,7,8])
  axs.set_xticks([0,.1,.2,.3,.4])

  if i in [0,2]:
    axs.set_ylabel(r'synergy factor $r$')

  if i not in [0,2]:
    axs.set_yticklabels([])

  
  if i in [len(k_vals)-1,len(k_vals)-2]:
    axs.set_xlabel(r'roaming agents participation $\delta$')

  if i not in [2,3,4,5,6]:  
    axs.set_xticklabels([])
  
  axs.yaxis.set_minor_locator(AutoMinorLocator(n=5))
  axs.xaxis.set_minor_locator(AutoMinorLocator(n=4))
  axs.set_title(r'$K$='+str(v0))

  axs.grid(True, which='major',linestyle='-.', linewidth=0.25, c='k', alpha=0.75)

cbar_ax = fig.add_axes([0.12, 1.025, 0.8, 0.02])
cbar = fig.colorbar(im, cax=cbar_ax, orientation="horizontal")
cbar.set_ticklabels([str(l) for l in levels])

fig.tight_layout()
display(fig)

# %% saving
fName = "final_plots/plot_" + exp_desc + ".pdf"
print("[INFO] Saving " + fName)
fig.savefig(fName, format="pdf", bbox_inches='tight')
