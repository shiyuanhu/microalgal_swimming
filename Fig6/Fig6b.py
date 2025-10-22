"""
This code generates a dual-axis plot of velocity and efficiency
    
Input files:
    - Dataset3_withHIs.csv
    - Dataset3_noHIs.csv

Output:
    - Fig6b.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Global plot style configuration
fontsize = 34
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
    "lines.linewidth": 2.5,
    "axes.linewidth": 1.5,
    "xtick.major.width": 1.5,
    "ytick.major.width": 1.5,
})

# Characteristic length scale
L = 13.03

def load_data(file_with, file_without):
    df_HIs = pd.read_csv(file_with)
    df_noHIs = pd.read_csv(file_without)
    return df_HIs, df_noHIs


def plot_figure(df_HIs, df_noHIs, output_file):
    b_HIs = df_HIs['b'].values
    Uy_HIs = df_HIs['Average_Uy'].values
    eta_HIs = df_HIs['Efficiency(%)'].values

    b_noHIs = df_noHIs['b'].values
    Uy_noHIs = df_noHIs['Average_Uy'].values
    eta_noHIs = df_noHIs['Efficiency(%)'].values

    # Styles
    uy_with_interaction_style = {
        'marker': '^', 'markersize': 14, 'markerfacecolor': 'red',
        'markeredgecolor': 'red', 'markeredgewidth': 0.8, 'color': 'red', 'linestyle': '-'
    }
    uy_without_interaction_style = {
        'marker': '^', 'markerfacecolor': 'none', 'markeredgecolor': 'red',
        'markeredgewidth': 2, 'markersize': 14, 'color': 'red', 'linestyle': '--'
    }
    eta_with_interaction_style = {
        'marker': 'o', 'markersize': 14, 'markerfacecolor': 'black',
        'markeredgecolor': 'black', 'markeredgewidth': 1, 'color': 'black', 'linestyle': '-'
    }
    eta_without_interaction_style = {
        'marker': 'o', 'markerfacecolor': 'none', 'markeredgecolor': 'black',
        'markeredgewidth': 2, 'markersize': 14, 'color': 'black', 'linestyle': '--'
    }

    # Figure
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax1.set_box_aspect(1)
    ax1.axvline(x = 4.44/L, color='black', linestyle='--', linewidth=1.5)

    ax1.plot(b_HIs / L, Uy_HIs, **uy_with_interaction_style)
    ax1.plot(b_noHIs / L, Uy_noHIs, **uy_without_interaction_style)
    ax2.plot(b_HIs / L, eta_HIs, **eta_with_interaction_style)
    ax2.plot(b_noHIs / L, eta_noHIs, **eta_without_interaction_style)

    ax1.set_xlabel(r'$b/L$', labelpad=8)
    ax1.set_ylabel(r'$\langle{U_\mathrm{b}}\rangle / U_0$', labelpad=8, color='red')
    ax2.set_ylabel(r'$\eta\ (\%)$', labelpad=8, color='black')

    # Configure tick colors
    ax1.tick_params(axis='y', colors='red')
    ax2.tick_params(axis='y', color='0.3', labelcolor='black')
    
    # Set Y-axis spine colors
    ax1.spines['left'].set_color('red')
    ax1.spines['left'].set_linewidth(1.5)
    ax2.spines['right'].set_color('0.3')
    ax2.spines['right'].set_linewidth(1.5)

    # Ensure other spines maintain original colors
    ax1.spines['top'].set_color('0.3')
    ax1.spines['bottom'].set_color('0.3') 
    ax1.spines['right'].set_visible(False)
    ax2.spines['top'].set_color('0.3')
    ax2.spines['bottom'].set_color('0.3')
    ax2.spines['left'].set_visible(False) 

    ax1.set_ylim([0, 0.097])
    ax2.set_ylim([-0.01, 0.5])
    ax2.set_yticks([0.2, 0.4])
    ax1.set_yticks([0.05])
    ax1.set_xticks([0, 0.2, 0.4, 0.6])

    plt.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close(fig)

def main():
    # File paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_with_HIs = os.path.join(current_dir, 'Dataset3_withHIs.csv')
    file_no_HIs = os.path.join(current_dir, 'Dataset3_noHIs.csv')
    output_file = os.path.join(current_dir, 'Fig6b.png')

    df_HIs, df_noHIs = load_data(file_with_HIs, file_no_HIs)
    plot_figure(df_HIs, df_noHIs, output_file)

if __name__ == "__main__":
    main()
