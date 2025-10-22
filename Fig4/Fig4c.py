"""
This code calculates and plots the average of the normalized drag forces

Input files:
    - Fig4c.csv: Drag force components along y-direction
        
Data structure:
    - Power stroke phase (14 data points)
    - Recovery stroke phase (remaining data points)

Output:
    - Fig4c.png 
        * Left group: Forces on body from flagella 
        * Right group: Forces on flagella from body
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

fontsize = 35.5
plt.rcParams.update({
    "text.usetex": True,
    "font.family": 'serif',
    "xtick.labelcolor": "black",
    "xtick.labelsize": fontsize,
})
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(current_dir, 'Fig4c.csv')
output_file = os.path.join(current_dir, 'Fig4c.png')

df = pd.read_csv(data_file)

Fb = df['Fb(y)'].abs()
Ff = df['Ff(y)'].abs()

mean_power1 = Fb[:14].mean()
mean_recover1 = Fb[14:].mean()
mean_power2 = Ff[:14].mean()
mean_recover2 = Ff[14:].mean()

fig, ax = plt.subplots(figsize=(7.6, 5)) 
ax.set_position([0.15, 0.15, 0.75, 0.75])

for spine in ax.spines.values():
    spine.set_visible(False)

group_spacing = 1.2
bar_spacing = 0.9
x_left = np.array([-group_spacing - bar_spacing/2, -group_spacing + bar_spacing/2])
x_right = np.array([group_spacing - bar_spacing/2, group_spacing + bar_spacing/2])
width = 0.4

ax.bar(x_left[0], mean_power1, width, color='red', alpha=0.7, edgecolor='#000000', linewidth=1.5)
ax.bar(x_left[1], mean_recover1, width, color='blue', alpha=0.7, edgecolor='#000000', linewidth=1.5)
ax.bar(x_right[0], mean_power2, width, color='red', alpha=0.7, edgecolor='#000000', linewidth=1.5)
ax.bar(x_right[1], mean_recover2, width, color='blue', alpha=0.7, edgecolor='#000000', linewidth=1.5)

ax.set_xticks(np.concatenate([x_left, x_right]))
ax.tick_params(axis='x', length=0) 
ax.set_xticklabels([r'$\mathrm{power}$', r'$\mathrm{recovery}$', 
                     r'$\mathrm{power}$', r'$\mathrm{recovery}$'],
                    ha='center', va='top', fontsize=fontsize-5)

y_max = max([mean_power1, mean_recover1, mean_power2, mean_recover2]) * 1.2
ax.set_ylim([0, y_max])
ax.set_xlim([-2.5, 2.5])
ax.set_yticks([])

ax.axhline(y=0, color='black', linewidth=1.5, zorder=1)
ax.plot([0, 0], [0, y_max * 1.05], 'k-', linewidth=1.2, zorder=1)

y_ticks = np.arange(0, y_max, 0.5)
y_ticks = y_ticks[y_ticks <= y_max]

for y in y_ticks:
    if y > 0:
        ax.plot([0, 0.06], [y, y], 'k-', linewidth=1.0, zorder=2)
        ax.text(-0.08, y, f'{y:.1f}', ha='right', va='center', fontsize=fontsize-1)

label_y = y_max * 0.95

ax.text(-group_spacing, label_y, 
        r'$\langle \boldsymbol{F}_{i\to \mathrm{b}} \boldsymbol{\cdot} \hat{\boldsymbol{y}} / \boldsymbol{F}_\mathrm{b}^0 \boldsymbol{\cdot} \hat{\boldsymbol{y}} \rangle$',
        ha='center', va='center', fontsize=fontsize-5, weight='bold')

ax.text(group_spacing, label_y, 
        r'$\langle \boldsymbol{F}_{\mathrm{b} \to i} \boldsymbol{\cdot} \hat{\boldsymbol{y}} / \boldsymbol{F}_i^0 \boldsymbol{\cdot} \hat{\boldsymbol{y}} \rangle$', 
        ha='center', va='center', fontsize=fontsize-5, weight='bold')

plt.tight_layout(pad=0)
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()