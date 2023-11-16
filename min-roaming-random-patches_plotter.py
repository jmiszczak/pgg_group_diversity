#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %% initial imports
import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.figure as figure
# import matplotlib.colors as colors
# from matplotlib.ticker import AutoMinorLocator

from IPython.display import display

mpl.rc('text', usetex=True)
mpl.rc('font', family='serif')
mpl.rc('font', size=8)

# %% data loading and initial calculations
plot_name = 'min-roaming-random-patches'
# experiemetns used for the plots
exps = ['roaming-random-patches-l16','roaming-random-patches-l32-even', 'roaming-random-patches-l64-even']
exps_var0s = {
  'roaming-random-patches-l16' : range(4,11),
  'roaming-random-patches-l32-even': [4,6,8,10],
  'roaming-random-patches-l64-even' : [4,6,8,10,12]
  }

exps_world_size = {
  'roaming-random-patches-l16' : 16,
  'roaming-random-patches-l32-even': 32,
  'roaming-random-patches-l64-even' : 64
  }

# raw and preprocessed data
data = dict()
df = dict()

for exp_desc in exps:

  # variables usd in the plots
  v = ["random-patches-number", "roaming-agents", "synergy-factor", "mean-cooperators1k"]

  # file with data from the experiment
  # Note: header=6 is for NetLogo data  
  data[exp_desc] = pd.read_csv('data/' + exp_desc + '.csv', header=6)
  
  # data from used for plots
  df[exp_desc] = pd.DataFrame(columns=v)
  #var0s = data[exp_desc][v[0]].unique()
  var1s = data[exp_desc][v[1]].unique()
  var2s = data[exp_desc][v[2]].unique()
  
  # range of parameters depends on the experiment
  var0s = exps_var0s[exp_desc]
  
  # preprocess
  for v0 in var0s:
      for v1 in var1s:
          for v2 in var2s: 
            df[exp_desc].loc[len(df[exp_desc].index)] = [
                  v0,
                  v1,
                  v2,
                  data[exp_desc][(data[exp_desc][v[0]] == v0) & (data[exp_desc][v[1]] == v1) & (data[exp_desc][v[2]] == v2)]['mean-cooperators1k'].mean()
              ]
  
  
  
  
#%% min delta
thr1 = 0.90
thr2 = 0.98

exps_world_size = {
  'roaming-random-patches-l16' : 16,
  'roaming-random-patches-l32-even': 32,
  'roaming-random-patches-l64-even' : 64
  }

fig = figure.Figure(figsize=(6.5,2.5),dpi=200)

for i, exp_desc in enumerate(exps):
  axs = fig.add_subplot(131+i)
  axs.set_ylim(-0.01,0.5)
  var0s = np.array([4,6,8,10])
  
  data_md = dict()
  data_max1 = dict()
  data_max2 = dict()
  pm = lambda x : '-' if x < a else '+'
  
  
  for k in var0s:
      data_md[k] = df[exp_desc][df[exp_desc][v[0]] == k][[v[1], v[2], v[3]]]
                                  
  for k in var0s:
      data_max1[k] = data_md[k][data_md[k]['mean-cooperators1k'] >= thr1 ]
      data_max2[k] = data_md[k][data_md[k]['mean-cooperators1k'] >= thr2 ]
      
  
  min_delta1 = [min(data_max1[x][data_max1[x]['synergy-factor'] == min(data_max1[x]['synergy-factor'])]['roaming-agents'])  for x in var0s]
  min_delta2 = [min(data_max2[x][data_max1[x]['synergy-factor'] == min(data_max2[x]['synergy-factor'])]['roaming-agents'])  for x in var0s]
 
  
  # thr1
  axs.plot(var0s, min_delta1, 'x', color='steelblue', label=r'$\geq$ {}\%'.format(100*thr1))
  a, b = np.polyfit(var0s, min_delta1, 1)

  
  axs.plot(var0s, a*var0s+b, '--', color='steelblue', lw=0.75)
  
  loc = np.array((4.3,a*5))
  axs.text(*loc, r'$f_{}(K) = {:4.3f}K {} {:4.3f}$ '.format('{'+str(thr1)+'}',a,pm(b),abs(b)),
            rotation=np.rad2deg(np.arctan(a)), rotation_mode='anchor',
                transform_rotates_text=True)
  
  # thr2
  axs.plot(var0s, min_delta2, 'ro', fillstyle='none', label=r'$\geq$ {}\%'.format(100*thr2))
  a, b = np.polyfit(var0s, min_delta2, 1)
  
  axs.plot(var0s, a*var0s+b,'r--', lw=0.75)
  
  loc = np.array((4.3,a*5+b+0.07))
  axs.text(*loc, r'$f_{}(K) = {:4.3f}K {} {:4.3f}$ '.format('{'+str(thr2)+'}',a,pm(b),abs(b)),
           rotation=np.rad2deg(np.arctan(a)), rotation_mode='anchor',
                transform_rotates_text=True)

  axs.grid(True, linestyle=':', linewidth=0.5, c='k')
  axs.set_xlabel(r'$K$')
  
  axs.set_title(r"$L="+ str(exps_world_size[exp_desc]) + "$")
  
  if i == 0:
    axs.set_ylabel(r'optimal $\delta$')
  if i != 0:
    axs.set_yticklabels([])
  
fig.tight_layout()
display(fig)
plot_name = 'min-roaming-random-patches'
fName = "plots/plot_" + plot_name + "-min_delta.pdf"
print("[INFO] Saving " + fName)
fig.savefig(fName, format="pdf", bbox_inches='tight')