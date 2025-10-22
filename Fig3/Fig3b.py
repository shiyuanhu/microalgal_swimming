"""
This script plots the displacement yb(t) over multiple beating cycles.

Input files:
    - Fig3b.csv: Time-series data for body displacement
        * t/T: Normalized time 
        * y(with_HIs): Body displacement with hydrodynamic interactions 
        * y(no_HIs): Body displacement without hydrodynamic interactions
        * delta_y: Displacement difference 

Output:
    - Fig3b.png
        * Main plot: yb(t)/L vs t/T over 4 beating cycles
        * Inset plot : Δyb/L vs t/T for one cycle
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

fontsize = 33
plt.rcParams.update({
    "text.usetex": True,
    "font.family": 'serif',
    "xtick.direction": 'in',
    "ytick.direction": 'in',
    "axes.edgecolor": '0.3',
    "xtick.color": "0.3",
    "ytick.color": "0.3",
    "xtick.labelcolor": "black",
    "ytick.labelcolor": "black",
    "xtick.labelsize": fontsize,
    "ytick.labelsize": fontsize,
    "axes.labelsize": fontsize,
    "axes.titlesize": fontsize + 2,
    "legend.fontsize": fontsize - 10,
    "lines.linewidth": 2.5,
    "axes.linewidth": 1.5,
})
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(current_dir, 'Fig3b.csv')
output_file = os.path.join(current_dir, 'Fig3b.png')

df = pd.read_csv(data_file)
t = df['t/T'].values
x_with = df['y(with_HIs)'].values
x_without = df['y(no_HIs)'].values
x_diff = df['delta_y'].values

num_cycles = 4
n = len(t)
t_ext = np.concatenate([t + i for i in range(num_cycles)])
x_with_ext = np.concatenate([x_with + x_with[-1] * i for i in range(num_cycles)])
x_without_ext = np.concatenate([x_without + x_without[-1] * i for i in range(num_cycles)])

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_position([0.15, 0.15, 0.75, 0.75])

ax.plot(t_ext, x_with_ext, label='with HIs', color='red', linestyle='-')
ax.plot(t_ext, x_without_ext, label='no HIs', color='black', linestyle='--')
ax.axvspan(3, 3 + 14/27, color='#E74C3C', alpha=0.2)
ax.axvspan(3 + 14/27, 4, color='#3498DB', alpha=0.2)
ax.set_xlim(-1/15, 4)
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_yticks([0, 0.2, 0.4])
ax.set_xlabel(r'$t/T$', fontsize=fontsize)
ax.set_ylabel(r'${y_{\mathrm{b}}(t)/L}$', fontsize=fontsize, labelpad=8)
ax.grid(True)
ax.legend(loc='lower right', frameon=True, edgecolor='darkgray', 
          facecolor='white', framealpha=1, borderpad=0.18)

ax_inset = fig.add_axes([0.22, 0.71, 0.28, 0.21])
ax_inset.plot(t, x_diff, color='blue', linewidth=2.5)
ax_inset.axhline(0, color='gray', linewidth=1.5)
ax_inset.axvspan(0, 14/27, color='#E74C3C', alpha=0.2)
ax_inset.axvspan(14/27, 1, color='#3498DB', alpha=0.2)

for spine in ax_inset.spines.values():
    spine.set_edgecolor('0.3')
    spine.set_linewidth(1.5)

ax_inset.set_xlim(0, 1)
ax_inset.set_ylim(0, 0.05)
ax_inset.set_xticks([0, 0.5, 1],['0', '0.5', '1'])
ax_inset.set_yticks([0, 0.05])
ax_inset.set_yticklabels(['0', '5'])
ax_inset.set_xlabel(r'$t/T$', fontsize=20, labelpad=2)
ax_inset.set_ylabel(r'$\Delta y_{\mathrm{b}}/L$', fontsize=20, labelpad=5)
ax_inset.text(0.1, 1, r'$10^{-2}$', transform=ax_inset.transAxes, 
              fontsize=18, ha='center', va='bottom')
ax_inset.tick_params(axis='both', labelsize=18)

plt.tight_layout(pad=0)
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()