"""
Average flow field around a swimming cell
Input files: Fig1b.npz
Output: Fig1b.png
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import os

fontsize = 32

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
    "axes.linewidth": 1.5,
    "xtick.major.width": 1.5,
    "ytick.major.width": 1.5
})
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

def load_data(data_path):
    """Load flow field data from npz file."""
    return dict(np.load(data_path, allow_pickle=True))

def calculate_speed(U, V):
    """Calculate flow speed magnitude."""
    return np.sqrt(U**2 + V**2)

def plot_flow_field(data, output_path, a, b, axis_range, axis_ticks):
    """Plot flow field with velocity contour and streamlines."""
    X, Y = data['X_plot'], data['Y_plot']
    U, V = data['U_plot'], data['V_plot']
    speed = calculate_speed(U, V)

    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    contour = ax.contourf(X, Y, speed, levels=200, cmap='jet', alpha=1.0, zorder=1)
    ax.streamplot(X, Y, U, V, 
                  color="darkgray",
                  linewidth=1.8,
                  density=[0.4, 0.38],
                  arrowsize=3,
                  arrowstyle='->',
                  minlength=0.1,
                  maxlength=5.8,
                  broken_streamlines=False)

    ellipse = Ellipse((0, 0), width=2*a, height=2*b, edgecolor='black', facecolor='lightgray', linewidth=5, zorder=10)
    ax.add_patch(ellipse)

    ax.set_xlim(axis_range)
    ax.set_ylim(axis_range)
    ax.set_xticks(axis_ticks)
    ax.set_yticks(axis_ticks)
    ax.set_xlabel(r'$x/L$')
    ax.set_ylabel(r'$y/L$')
    ax.set_aspect('equal')

    cbar = plt.colorbar(contour, shrink=0.6, aspect=15, ticks=[0, 0.02, 0.04])
    cbar.ax.tick_params(labelsize=30)
    cbar.ax.text(0.85, 1.02, r'$U/U_0$', transform=cbar.ax.transAxes,
                  fontsize=30, ha='center', va='bottom')

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    # Get script directory to ensure correct save path
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Data and output paths
    data_file = os.path.join(current_dir, 'Fig1b.npz')
    output_file = os.path.join(current_dir, 'Fig1b.png')

    # Geometric parameters
    adim = 3.89
    bdim = 5.95
    Ldim = 14
    a = adim / Ldim
    b = bdim / Ldim

    # Plot settings
    axis_range = (-2, 2)
    axis_ticks = [-1.5, 0, 1.5]

    data = load_data(data_file)
    plot_flow_field(data, output_file, a, b, axis_range, axis_ticks)
