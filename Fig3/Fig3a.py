"""
This code plots the instantaneous swimming speed Ub(t) over one beating cycle.

Input files:
    - Fig3a.csv: Time-series data 
        * t/T: Normalized time 
        * Ub(with_HIs): Swimming speed with hydrodynamic interactions 
        * Ub(no_HIs): Swimming speed without hydrodynamic interactions
        * delta_Ub: Velocity difference

Output:
    - Fig3a.png 
        * Main plot: Ub(t)/U0 vs t/T 
        * Inset plot: ΔUb/U0 vs t/T
"""
import pandas as pd
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
data_file = os.path.join(current_dir, 'Fig3a.csv')
output_file = os.path.join(current_dir, 'Fig3a.png')

df = pd.read_csv(data_file)
t = df['t/T'].values
v_with = df['Ub(with_HIs)'].values
v_without = df['Ub(no_HIs)'].values
v_diff = df['delta_Ub'].values

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_position([0.15, 0.15, 0.75, 0.75])

ax.axhline(0, color='gray', linestyle=':', linewidth=2, alpha=0.7)
ax.plot(t, v_with, color='red', linestyle='-', marker='o', markerfacecolor='red',
         markeredgecolor='black', markeredgewidth=1, markersize=13, label='with HIs')
ax.plot(t, v_without, color='black', linestyle='--', marker='o', markerfacecolor='none',
         markeredgecolor='black', markeredgewidth=2, markersize=13, label='no HIs')

ax.axvspan(0, 14/27, color='#E74C3C', alpha=0.2)
ax.axvspan(14/27, 1, color='#3498DB', alpha=0.2)

ax.text(0.25, 0.91, r'\textbf{power stroke}', fontsize=fontsize-6.5,
         ha='center', va='center')
ax.text(0.75, 0.91, r'\textbf{recovery stroke}', fontsize=fontsize-6.5,
         ha='center', va='center')

ax.set_xlim(0, 1)
ax.set_ylim(-0.7, 0.99)
ax.set_xticks([0, 0.5, 1],['0', '0.5', '1'])
ax.set_yticks([-0.5, 0, 0.5],['-0.5', '0', '0.5'])
ax.set_xlabel(r'$t/T$', fontsize=fontsize)
ax.set_ylabel(r'$U_{\mathrm{b}}(t)/U_{0}$', fontsize=fontsize, labelpad=8)
ax.legend(loc='lower left', frameon=True, edgecolor='darkgray',
           facecolor='white', framealpha=1, borderpad=0.18)

ax_inset = fig.add_axes([0.68, 0.65, 0.28, 0.21])
ax_inset.plot(t, v_diff, color='blue', linewidth=2.5)
ax_inset.axhline(0, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax_inset.axvspan(0, 14/27, color='#E74C3C', alpha=0.2)
ax_inset.axvspan(14/27, 1, color='#3498DB', alpha=0.2)
ax_inset.set_xlim(0, 1)
ax_inset.set_ylim(-0.025, 0.145)
ax_inset.set_xticks([0, 0.5, 1],['0', '0.5', '1'])
ax_inset.set_yticks([0, 0.1],['0', '0.1'])
ax_inset.set_xlabel(r'$t/T$', fontsize=20, labelpad=2)
ax_inset.set_ylabel(r'$\Delta U_{\mathrm{b}}/U_{0}$', fontsize=20, labelpad=5)
ax_inset.tick_params(labelsize=18)

plt.tight_layout(pad=0)
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()