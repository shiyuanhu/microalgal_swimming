"""
Input files:
    - Fig4b.csv: Data for different HI components
        * h: Normalized separation distance  
        * B_to_F_static: Body-to-flagellum static HI 
        * B_to_F_dynamic: Body-to-flagellum dynamic HI 
        * B_to_F: Total body-to-flagellum HI 
        * F_to_B: Flagellum-to-body HI 
        * noHIs: Body speed without hydrodynamic interactions 

Output:
    - Fig4b.png 
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

fontsize = 35.5
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
    "legend.fontsize": fontsize - 11,  
    "lines.linewidth": 2.5,  
    "axes.linewidth": 1.5,  
    "xtick.major.width": 1.5,  
    "ytick.major.width": 1.5,  
})

current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(current_dir, 'Fig4b.csv')
output_file = os.path.join(current_dir, 'Fig4b.png')

df = pd.read_csv(data_file)

fig, ax = plt.subplots(figsize=(7.6,5.225)) 
ax.set_position([0.15, 0.15, 0.75, 0.75])

ax.plot(df['h'], df['B_to_F_static'], color='#F18F01', label=r"$\mathrm{B\textrm{-} to \textrm{-} F\ static}$", linestyle=':', linewidth=3.2)
ax.plot(df['h'], df['B_to_F_dynamic'], color='#F18F01', label=r"$\mathrm{B\textrm{-} to \textrm{-} F\ dynamic}$", linestyle='--', linewidth=3.2)
ax.plot(df['h'], df['B_to_F'], color='#F18F01', label=r"$\mathrm{B\textrm{-} to \textrm{-} F}$", linestyle='-', linewidth=3.2)
ax.plot(df['h'], df['F_to_B'], color='#0177F1', label=r"$\mathrm{F\textrm{-} to \textrm{-} B}$", linestyle='-', linewidth=3.2)
ax.plot(df['h'], df['noHIs'], color='dimgray', label=r"$\mathrm{no\ HIs}$", linestyle='-', linewidth=3.2)

ax.set_xlim([-0.01, 2.0])
ax.set_ylim([0, 0.157])

ax.set_xticks([0, 1.0, 2.0])

ax.set_yticks([0, 0.05, 0.1, 0.15])
ax.set_yticklabels([r"$0$", r"$0.05$", r"$0.1$", r"$0.15$"])

ax.set_xlabel(r"$h/r_{\mathrm{b}}$")
ax.set_ylabel(r"$U_\mathrm{b}/U_{0}$", labelpad=8)

plt.legend(loc='lower right', frameon=True, bbox_to_anchor=(1.015, -0.02), edgecolor='darkgray', facecolor='white', 
           framealpha=1, handletextpad=0.2, labelspacing=0.15, handlelength=1.5, borderpad=0.18)

plt.tight_layout(pad=0)
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()