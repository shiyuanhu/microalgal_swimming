"""
This code plots velocity time-series computed using the Boundary Element 
Method and a nonlocal slender body theory, with an inset schematic of the model.

Input files:
    - U_bem.csv: Velocity data from Boundary Element Method
        * time: Normalized time t/τ 
        * U0: Velocity magnitude U(t) 

    - U_nonlocal.csv: Velocity data from nonlocal slender body theory
        * time: Normalized time t/τ
        * U0: Velocity magnitude U(t)

Output:
    - Fig5.png
        * Main plot: U(t) vs t/τ 
        * Inset diagram: Hinged arm structure
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Set global plotting parameters
fontsize = 34
plt.rcParams.update({
    "font.family": 'serif', 
    "text.usetex": True,
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

def read_csv_files(file1, file2):
    """Read two CSV files"""
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    return df1['time'].values, df1['U0'].values, df2['time'].values, df2['U0'].values

def plot_comparison(t1, u1, t2, u2, label1='BEM/regularized Stokeslet', label2='nonlocal slender body'):
    """Plot velocity comparison between two datasets"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot two curves
    ax.plot(t1, u1, '-', color='black', label=label1, linewidth=3)
    ax.plot(t2, u2, '--', color='red', label=label2, linewidth=3)
    ax.axhline(0, color='gray', linestyle=':', linewidth=2, alpha=0.7)
    
    # Set axes
    ax.set_xlabel(r'$t/\tau$')
    ax.set_ylabel(r'$U(t)$')
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0], ['0', '0.2', '0.4', '0.6', '0.8', '1.0'])

    ax.legend(loc='upper center', bbox_to_anchor=(0.53, 1.0), frameon=True, edgecolor='darkgray', 
              facecolor='white', framealpha=1, fontsize=fontsize-10, 
              borderpad=0.18, handlelength=1.8, handletextpad=0.1, labelspacing=0.2)
    ax.grid(False)
    
    return fig, ax

def add_inset_diagram(ax):
    """Add mechanical structure diagram as inset"""
    # Create inset axes
    axins = inset_axes(ax, width="90%", height="90%", loc='lower right',
                      bbox_to_anchor=(0.38, -0.15, 0.83, 0.83), bbox_transform=ax.transAxes)
    axins.set_aspect('equal')
    axins.axis('off')
    
    # Structure parameters
    theta = 0.6
    L = 3
    delta = 0.12
    offset = 5 * delta
    
    # Hinge positions
    P_upper = (offset, offset)
    P_lower = (offset, -offset)
    A = (L * np.cos(theta) + offset, L * np.sin(theta) + offset)
    B = (L * np.cos(theta) + offset, -L * np.sin(theta) - offset)
    
    # Draw arms and hinges
    axins.plot([P_upper[0], A[0]], [P_upper[1], A[1]], 'k-', linewidth=2)
    axins.plot([P_lower[0], B[0]], [P_lower[1], B[1]], 'k-', linewidth=2)
    axins.plot(P_upper[0], P_upper[1], 'ko', markersize=8)
    axins.plot(P_lower[0], P_lower[1], 'ko', markersize=8)
    axins.axhline(0, color='k', linestyle='--', linewidth=1.5)
    
    # Offset distance annotation
    x_arrow = P_upper[0] - 0.3
    arrow = FancyArrowPatch((x_arrow, 0), (x_arrow, P_upper[1]),
                           arrowstyle='<->', mutation_scale=12, color='black',
                           linewidth=1.5, shrinkA=0, shrinkB=0)
    axins.add_patch(arrow)
    axins.text(x_arrow-0.65, P_upper[1]/2+0.05, r'$5r_0$', fontsize=fontsize-12, ha='center', va='center')
    
    # Angle annotation
    radius = 1.5
    start_pt = (P_upper[0] + radius, P_upper[1])
    end_pt = (P_upper[0] + radius * np.cos(theta), P_upper[1] + radius * np.sin(theta))
    arc_arrow = FancyArrowPatch(start_pt, end_pt,
                               connectionstyle=f"arc3,rad={theta/5}",
                               arrowstyle='<->', mutation_scale=16, color='black',
                               linewidth=1.5, shrinkA=0, shrinkB=0)
    axins.add_patch(arc_arrow)
    
    label_x = P_upper[0] + 2.3 * np.cos(theta/4)
    label_y = P_upper[1] + 2.3 * np.sin(theta/4)
    axins.text(label_x, label_y, r'$\theta(t)$', fontsize=fontsize-10, ha='center')
    
    # Coordinate system indicator
    coords_ax = ax.figure.add_axes([0.73, 0.22, 1/24, 1/18], frameon=False)
    coords_ax.arrow(0.08, 0.08, 0.15, 0, head_width=0.03, head_length=0.03,
                   linewidth=1.5, fc='k', ec='k')
    coords_ax.arrow(0.08, 0.08, 0, 0.15, head_width=0.03, head_length=0.03,
                   linewidth=1.5, fc='k', ec='k')
    coords_ax.text(0.35, 0.04, '$x$', color='k', ha='center', fontsize=fontsize-14)
    coords_ax.text(0.08, 0.35, '$y$', color='k', ha='center', fontsize=fontsize-14)
    coords_ax.axis('off')
    
    # Set limits
    margin = 0.5
    axins.set_xlim(-margin, L + offset + margin)
    axins.set_ylim(-L - offset - margin, L + offset + margin)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file1 = os.path.join(current_dir, 'U_bem.csv')
    file2 = os.path.join(current_dir, 'U_nonlocal.csv')
    output_file = os.path.join(current_dir, 'Fig5.png')
    
    t1, u1, t2, u2 = read_csv_files(file1, file2)

    fig, ax = plot_comparison(t1, u1, t2, u2)
    
    add_inset_diagram(ax)
    
    plt.tight_layout()

    fig.savefig(output_file, format='png', dpi=300, bbox_inches='tight')    
    plt.show()

if __name__ == "__main__":
    main()