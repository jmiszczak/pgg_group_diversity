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
mpl.rc('font', size=9)

# %% data loading

# name of the resulting file
plot_name = 'roaming-random-local'

# experiements used for the plots
exps = [
  'roaming-random-local-l64',
  'roaming-random-local-l64-async',
  'roaming-random-local-differences-l64'
  ]


# variables usd in the plots
v = ["neighborhood-type", "roaming-agents", "synergy-factor", "mean-cooperators1k"]

# raw data and preprocessed data
data = dict()
df = dict()

# data preprocessing
for exp_desc in exps:

  # file with data from the experiment
  # Note: header=6 is for NetLogo data
  
  
# exp_files = [exp_desc, exp_desc + '-batch2',  exp_desc + '-batch3' ]
  print ('data/' + exp_desc + '.csv')
  data[exp_desc] = pd.read_csv('data/' + exp_desc + '.csv', header=6)
  
  # data fram used for plots
  df[exp_desc] = pd.DataFrame(columns=v)
  var0s = data[exp_desc][v[0]].unique()
  var1s = data[exp_desc][v[1]].unique()
  var2s = data[exp_desc][v[2]].unique()
  
  for v0 in var0s:
      for v1 in var1s:
          for v2 in var2s: 
            df[exp_desc].loc[len(df[exp_desc].index)] = [
                  v0,
                  v1,
                  v2,
                  data[exp_desc][(data[exp_desc][v[0]] == v0) & (data[exp_desc][v[1]] == v1) & (data[exp_desc][v[2]] == v2)]['mean-cooperators1k'].mean()
              ]

#%% plot

# levels and colors for the contour plots
levels = [0, 0.001, 0.2, 0.5, 0.75, 0.9, 0.95, 0.98, 1]
plotColors = ['yellow', 'orange',  'red', 'tomato',
              'olive', 'palegreen', 'lightblue', 'white']
cmap, norm = colors.from_levels_and_colors(levels, plotColors)

for j, exp_desc in enumerate(exps):
  plot_data = dict()

  # one figure for all cases of v0
  fig = figure.Figure(figsize=(5, 2), dpi=150)
  for i, v0 in enumerate(var0s):
    # Note: 1*2 is the number of cases for var0s 
    axs = fig.add_subplot(121+i);
 
    plot_data[v0] = df[exp_desc][df[exp_desc][v[0]] == v0][[v[1], v[2], v[3]]].to_numpy()
    
    # add contour
    axs.contour(
      plot_data[v0].T[0].reshape((len(var1s),len(var2s))),
      plot_data[v0].T[1].reshape((len(var1s),len(var2s))),
      plot_data[v0].T[2].reshape((len(var1s),len(var2s))),
      levels=levels[1::],
      linestyles='dashed',
      linewidths=.5,
      colors = ['black']
      )
  
    # fill the contours
    im = axs.contourf(
      plot_data[v0].T[0].reshape((len(var1s),len(var2s))),
      plot_data[v0].T[1].reshape((len(var1s),len(var2s))),
      plot_data[v0].T[2].reshape((len(var1s),len(var2s))),
      levels=levels,
      cmap = cmap,
      norm = norm,
      interpolation=None
      )
  
    # make nice major and minor ticks
    axs.set_yticks([2.5,3,3.5,4,4.5,5,5.5,6])
    axs.set_xticks([0.0,.2,.4,.6,.8,1.0])
    axs.yaxis.set_minor_locator(AutoMinorLocator(n=5))
    axs.xaxis.set_minor_locator(AutoMinorLocator(n=4))
  
    # take car of the labels
    if i in [0,2,4]:
      axs.set_ylabel(r'synergy factor $r$')
    
    axs.set_xlabel(r'roaming agents fraction $\delta$')
        
    if i not in [0,2,4]:
        axs.set_yticklabels([])
    
    # final touches
    axs.set_title(str(v0), size=8)
    axs.grid(True, which='major',linestyle='-.', linewidth=0.25, c='k', alpha=0.75) 
  
  # attach the title and the color bar to the first plot
  if j == 0:
    
    cbar_ax = fig.add_axes([0.125, 1.05, 0.8, 0.04])
    cbar = fig.colorbar(im, cax=cbar_ax, orientation="horizontal")
    cbar.set_ticklabels([str(l) for l in levels])
      
  # displaying
  fig.tight_layout()
  display(fig)
  
  # saving
  fName = "plots/plot_" + exp_desc + ".pdf"
  print("[INFO] Saving " + fName)
  fig.savefig(fName, format="pdf", bbox_inches='tight')

# #%% min delta
# data_md = dict()
# data_max1 = dict()
# data_max2 = dict()
# thr1 = 0.95
# thr2 = 0.99

# for k in var0s:
#     data_md[k] = df[df[v[0]] == k][[v[1], v[2], v[3]]]
                              
# for k in var0s:
#     data_max1[k] = data_md[k][data_md[k]['mean-cooperators1k'] >= thr1 ]
#     data_max2[k] = data_md[k][data_md[k]['mean-cooperators1k'] >= thr2 ]
  
# #min_delta1 = [min(data_max1[x]['roaming-agents']) for x in var0s]
# #min_delta2 = [min(data_max2[x]['roaming-agents']) for x in var0s]

# min_delta1 = [min(data_max1[x][data_max1[x]['synergy-factor'] == min(data_max1[x]['synergy-factor'])]['roaming-agents'])  for x in var0s]
# min_delta2 = [min(data_max2[x][data_max1[x]['synergy-factor'] == min(data_max2[x]['synergy-factor'])]['roaming-agents'])  for x in var0s]

# print(min_delta1)

# print(min_delta2)

