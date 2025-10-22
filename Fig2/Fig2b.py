"""
This code generates a two-panel figure of swimming efficiency against normalized cell body length (b/L).

Input files:
    - Fig2b.csv: Efficiency data for various configurations
        * b: Cell body major axis length
        * Efficiency(b/a_1.2): Efficiency with cell body aspect ratio b/a = 1.2 
        * Efficiency(HIs): Efficiency with natural aspect ratio (b/a = 1.53) and full HIs 
        * Efficiency(b/a_2.5): Efficiency with cell body aspect ratio b/a = 2.5
        * Efficiency(noffHIs): Efficiency with only body-flagella HIs
        * Efficiency(noHIs): Efficiency without HIs

Output:
    - Fig2b.png
        * Left panel: Efficiency for aspect ratios b/a = 1.2, 1.53, 2.5
        * Right panel: Efficiency under different HI treatments at b/a = 1.53
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fontsize = 24
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
    "legend.fontsize": fontsize - 6,
    "lines.linewidth": 2.5,
    "axes.linewidth": 1.5,
    "xtick.major.width": 1.5,
    "ytick.major.width": 1.5,
})
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

def plot_figure(df):
    L = 14
    b_normalized = df['b'].values / L
    fig = plt.figure(figsize=(8, 5))
    gs = gridspec.GridSpec(1, 2, left=0.1, right=0.95, bottom=0.15, top=0.85, wspace=0.03)

    ax1 = fig.add_subplot(gs[0, 0])
    e_1 = df['Efficiency(b/a_1.2)'] * 100
    e_2 = df['Efficiency(HIs)'] * 100
    e_3 = df['Efficiency(b/a_2.5)'] * 100
    ax1.axvline(x=5.95/14, color='black', linestyle='--', linewidth=1.5)
    ax1.plot(b_normalized, e_1, marker='^', markersize=8,
             markerfacecolor='#228B22', markeredgecolor='black', markeredgewidth=1,
             color='#228B22', linestyle='-', linewidth=2.5)
    ax1.plot(b_normalized, e_2, marker='o', markersize=8,
             markerfacecolor='red', markeredgecolor='black', markeredgewidth=1,
             color='red', linestyle='-', linewidth=2.5)
    ax1.plot(b_normalized, e_3, marker='s', markersize=8,
             markerfacecolor='#FFD700', markeredgecolor='black', markeredgewidth=1,
             color='#FFD700', linestyle='-', linewidth=2.5)
    ax1.set_ylim(0,0.75)
    ax1.set_yticks([0, 0.2, 0.4, 0.6], ['', '0.2', '', '0.6'])
    ax1.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], ['0', '', '0.2', '', '0.4', ''])
    ax1.set_ylabel(r'$\eta\ (\%)$', labelpad=8)
    y_min, y_max = ax1.get_ylim()
    b_min, b_max = 0.3, 0.46
    n_segments = 100
    for i in range(n_segments):
        y_start = y_max - i * (y_max - y_min) / n_segments
        y_end = y_max - (i + 1) * (y_max - y_min) / n_segments
        alpha = 0.05 + 0.4 * (i / n_segments)
        ax1.add_patch(plt.Rectangle((b_min, y_end), b_max - b_min, y_start - y_end,
                                    facecolor='gray', alpha=alpha, edgecolor='none',
                                    linewidth=0, zorder=0))
    ax2 = fig.add_subplot(gs[0, 1])
    e_HIs = df['Efficiency(HIs)'].values * 100
    e_noffHIs = df['Efficiency(noffHIs)'].values * 100
    e_noHIs = df['Efficiency(noHIs)'].values * 100
    ax2.plot(b_normalized, e_HIs, marker='o', markersize=8,
             markerfacecolor='red', markeredgecolor='black', markeredgewidth=1,
             color='red', linestyle='-')
    ax2.plot(b_normalized, e_noffHIs, marker='o', markersize=8,
             markerfacecolor='none', markeredgecolor='red', markeredgewidth=2,
             color='red', linestyle='-')
    ax2.plot(b_normalized, e_noHIs, marker='o', markersize=8,
             markerfacecolor='none', markeredgecolor='black', markeredgewidth=2,
             color='black', linestyle='--')
    ax2.set_ylim(0,0.75)
    ax2.set_yticks([0, 0.2, 0.4, 0.6], ['', '', '', ''])
    ax2.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], ['0', '', '0.2', '', '0.4', ''])
    fig.text(0.525, 0.02, r'$b/L$', ha='center', fontsize=fontsize+2)
    return fig

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, 'Fig2b.csv')
    output_file = os.path.join(current_dir, 'Fig2b.png')
    df = pd.read_csv(data_file)
    fig = plot_figure(df)
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    main()
