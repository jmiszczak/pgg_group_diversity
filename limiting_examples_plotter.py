#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 12:46:02 2026

@author: jam
"""

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
mpl.rc('font', size=10)

# %% data loading

# name of the resulting file
plot_sync = 'example-times-series-sync'
plot_async = 'example-times-series-async'

# file with data from the experiment
# Note: Netolog data are fixed before loading
sync_file = os.path.join('data/' , "pgg_group_diversity_limiting_sync_fixed.csv")
async_file = os.path.join('data/' , "pgg_group_diversity_limiting_async_fixed.csv")

# use only selected columns
local_v = ["x0", "y0", "y1"]
sync_data = pd.read_csv(sync_file, usecols = local_v) 
async_data = pd.read_csv(async_file, usecols = local_v) 

#%%


fig1 = figure.Figure(figsize=(4,3))
axs1 = fig1.add_subplot(1,1,1)
axs1.plot(async_data['x0'][1025:-1:128], async_data['y0'][1025:-1:128], ":", color='green',  linewidth="1",  ms='5')
axs1.plot(async_data['x0'][1025:-1:128], async_data['y1'][1025:-1:128],  "-", color='blue',  linewidth="1.5",  ms='5')

axs1.grid(True, which='major',linestyle='-.', linewidth=0.25, c='k', alpha=0.75)
axs1.set_xticks([1024] + [4096*i for i in range(17)])
axs1.set_xlim([1024-256,32768+256])
axs1.set_ylim([0,1.05])
axs1.set_ylabel(r'fraction of cooperators')
axs1.set_xlabel(r'step')
axs1.set_title("asynchronouse mode")

fig1.tight_layout()
display(fig1)

fName = "plots/plot_" + plot_async + ".pdf"
print("[INFO] Saving " + fName)
fig1.savefig(fName, format="pdf", bbox_inches='tight')

#%%
fig2 = figure.Figure(figsize=(4,3))
axs2 = fig2.add_subplot(1,1,1)
axs2.plot(sync_data['x0'][1025:-1:128], sync_data['y0'][1025:-1:128], ":", color='green',  linewidth="1",  ms='5')
axs2.plot(sync_data['x0'][1025:-1:128], sync_data['y1'][1025:-1:128],  "-", color='blue',  linewidth="1.5",  ms='5')

axs2.grid(True, which='major',linestyle='-.', linewidth=0.25, c='k', alpha=0.75)
axs2.set_xticks([1024] + [4096*i for i in range(17)])
axs2.set_xlim([1024-256,32768+256])
axs2.set_ylim([0,1.05])
axs2.set_ylabel(r'fraction of cooperators')
axs2.set_xlabel(r'step')
axs2.set_title("synchronouse mode")

fig2.tight_layout()
display(fig2)

fName = "plots/plot_" + plot_sync + ".pdf"
print("[INFO] Saving " + fName)
fig2.savefig(fName, format="pdf", bbox_inches='tight')