"""
This script plots an elliptical cell body with attached flagella beating over time
Input files: Fig1a.csv
Output: Fig1a.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import pandas as pd

plt.rcParams.update({
    "text.usetex": True,
    "font.family": 'serif',
    "xtick.direction": 'in',
    "ytick.direction": 'in',
    "lines.linewidth": 2.5,
    "axes.linewidth": 1.5
})
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

def load_data(file_path, t):
    """Load x,y flagella coordinates at time step t from CSV."""
    df = pd.read_csv(file_path)
    df_t = df[df["time"] == t]
    if df_t.empty:
        raise ValueError(f"No data found at time {t}")
    x = df_t.iloc[:, 2].values
    y = df_t.iloc[:, 3].values
    return x, y

def draw_cell_body(ax, a, b, y_offset):
    """Draw elliptical cell body."""
    theta = np.linspace(0, 2*np.pi, 200)
    ax.fill(a*np.cos(theta), b*np.sin(theta) + y_offset, 'lightgray',
            edgecolor='black', linewidth=3)

def draw_flagella(ax, file_path, time_steps):
    """Draw flagella trajectories for all time steps."""
    colors = plt.cm.rainbow(np.linspace(1, 0, len(time_steps)))
    for t, color in zip(time_steps, colors):
        x, y = load_data(file_path, t)
        rx = a * np.cos(phi)
        ry = b * np.sin(phi) + y_offset
        lx = -a * np.cos(phi)
        ly = b * np.sin(phi) + y_offset
        ax.plot(x + rx, y + ry, color=color, linewidth=3)
        ax.plot(-x + lx, y + ly, color=color, linewidth=3)

def add_colorbar(fig, time_steps):
    """Add time colorbar to the figure."""
    cbar_ax = fig.add_axes([0.35, 0.88, 0.3, 0.03])
    norm = plt.Normalize(min(time_steps), max(time_steps))
    sm = plt.cm.ScalarMappable(cmap='rainbow_r', norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
    cbar.set_ticks([])
    cbar.set_label(r"$t$", fontsize=14)

def plot_cell_with_flagella(file_path, output_name, a, b, phi, y_offset, num_time_steps):
    """Main plotting routine for cell body and flagella."""
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_axis_off()
    draw_cell_body(ax, a, b, y_offset)
    time_steps = range(num_time_steps)
    draw_flagella(ax, file_path, time_steps)
    add_colorbar(fig, time_steps)
    plt.savefig(output_name, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    # Get script directory to ensure correct save path
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Data and output paths
    csv_file = os.path.join(current_dir, "Fig1a.csv")
    output_name = os.path.join(current_dir, "Fig1a.png")
    
    # Geometric parameters (dimensionless)
    adim = 3.89
    bdim = 5.95
    ldim = 14
    a = adim / ldim
    b = bdim / ldim
    phi = 0.45 * np.pi
    y_offset = -0.17
    num_time_steps = 28

    plot_cell_with_flagella(csv_file, output_name, a, b, phi, y_offset, num_time_steps)
