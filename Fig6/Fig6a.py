"""
This code generates a dual-axis plot of velocity and efficiency
    
Input files:
    - Dataset2_withHIs.csv
    - Dataset2_noHIs.csv

Output:
    - Fig6a.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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

class CombinedLineHandler:
    """Handler for legend entries combining velocity (triangle) and efficiency (circle) markers."""
    
    def __init__(self, line1_color, line1_style, marker1_style, 
                 line2_color, line2_style, marker2_style):
        self.line1_color = line1_color
        self.line1_style = line1_style
        self.marker1_style = marker1_style
        self.line2_color = line2_color
        self.line2_style = line2_style
        self.marker2_style = marker2_style
    
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        """Create custom legend entry with both velocity and efficiency symbols."""
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        y_center = y0 + height / 2
        
        # Velocity symbols (red triangles)
        x1_start, x1_end, x1_marker = x0 + width * 0.05, x0 + width * 0.35, x0 + width * 0.25
        line1 = plt.Line2D([x1_start, x1_end], [y_center, y_center], 
                          color=self.line1_color, linestyle=self.line1_style, linewidth=2.5)
        handlebox.add_artist(line1)
        marker1 = plt.Line2D([x1_marker], [y_center], marker='^', markersize=10, 
                           color=self.line1_color, linestyle='None', **self.marker1_style)
        handlebox.add_artist(marker1)
        
        # Efficiency symbols (black circles)
        x2_start, x2_end, x2_marker = x0 + width * 0.5, x0 + width * 0.8, x0 + width * 0.7
        line2 = plt.Line2D([x2_start, x2_end], [y_center, y_center], 
                          color=self.line2_color, linestyle=self.line2_style, linewidth=2.5)
        handlebox.add_artist(line2)
        marker2 = plt.Line2D([x2_marker], [y_center], marker='o', markersize=10, 
                           color=self.line2_color, linestyle='None', **self.marker2_style)
        handlebox.add_artist(marker2)
        
        return line1

# Plot Style Definitions
# Velocity styles (red triangles, left y-axis)
uy_with_HIs = {'marker': '^', 'markersize': 14, 'markerfacecolor': 'red', 
               'markeredgecolor': 'red', 'markeredgewidth': 0.8, 
               'color': 'red', 'linestyle': '-'}

uy_no_HIs = {'marker': '^', 'markerfacecolor': 'none', 'markeredgecolor': 'red', 
             'markeredgewidth': 2, 'markersize': 14, 
             'color': 'red', 'linestyle': '--'}

# Efficiency styles (black circles, right y-axis)
eta_with_HIs = {'marker': 'o', 'markersize': 14, 'markerfacecolor': 'black', 
                'markeredgecolor': 'black', 'markeredgewidth': 1, 
                'color': 'black', 'linestyle': '-'}

eta_no_HIs = {'marker': 'o', 'markerfacecolor': 'none', 'markeredgecolor': 'black', 
              'markeredgewidth': 2, 'markersize': 14, 
              'color': 'black', 'linestyle': '--'}

def main():
    L = 10.82  # Characteristic length scale

    # Get current directory and define file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_with_HIs = os.path.join(current_dir, 'Dataset2_withHIs.csv')
    file_no_HIs = os.path.join(current_dir, 'Dataset2_noHIs.csv')
    output_file = os.path.join(current_dir, 'Fig6a.png')
    
    # Load data
    df_HIs = pd.read_csv(file_with_HIs)
    b_HIs = df_HIs['b'].values   
    Uy_HIs = df_HIs['Average_Uy'].values  
    eta_HIs = df_HIs['Efficiency(%)'].values  
    
    df_noHIs = pd.read_csv(file_no_HIs) 
    b_noHIs = df_noHIs['b'].values  
    Uy_noHIs = df_noHIs['Average_Uy'].values
    eta_noHIs = df_noHIs['Efficiency(%)'].values
    
    # Create figure and dual axes
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)  # Primary axis: velocity
    ax2 = ax1.twinx()           # Secondary axis: efficiency
    
    # Add reference line
    ax1.axvline(x = 4.61/L, color='black', linestyle='--', linewidth=1.5)
    
    # Plot data
    ax1.plot(b_HIs/L, Uy_HIs, **uy_with_HIs)
    ax1.plot(b_noHIs/L, Uy_noHIs, **uy_no_HIs)
    ax2.plot(b_HIs/L, eta_HIs, **eta_with_HIs)
    ax2.plot(b_noHIs/L, eta_noHIs, **eta_no_HIs)
    
    # Configure axes labels
    ax1.set_xlabel(r'$b/L$', labelpad=8)
    ax1.set_ylabel(r'$\langle{U_\mathrm{b}}\rangle / U_0$', labelpad=8, color='red')
    ax2.set_ylabel(r'$\eta\ (\%)$', labelpad=8, color='black')
    
    # Set limits and ticks
    ax1.set_ylim([0, 0.097])
    ax2.set_ylim([-0.01, 0.5])
    ax1.set_xticks([0, 0.2, 0.4, 0.6])
    ax1.set_xticklabels(['0', '0.2', '0.4', '0.6'])
    ax1.set_yticks([0.05])
    ax1.set_yticklabels(['0.05'])
    ax2.set_yticks([0.2, 0.4])
    
    # Configure tick colors
    ax1.tick_params(axis='y', colors='red')
    ax2.tick_params(axis='y', color='0.3', labelcolor='black')
    
    # Configure spines
    ax1.spines['left'].set_color('red')
    ax1.spines['left'].set_linewidth(1.5)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_color('0.3')
    ax1.spines['bottom'].set_color('0.3')
    
    ax2.spines['right'].set_color('0.3')
    ax2.spines['right'].set_linewidth(1.5)
    ax2.spines['left'].set_visible(False)
    ax2.spines['top'].set_color('0.3')
    ax2.spines['bottom'].set_color('0.3')
    
    ax1.set_box_aspect(1)
    
    # Create custom legend
    legend_elements = [
        Line2D([0], [0], marker='', color='none', label='with HIs'),
        Line2D([0], [0], marker='', color='none', label='no HIs')
    ]
    
    handler_map = {
        legend_elements[0]: CombinedLineHandler(
            'red', '-', 
            {'markerfacecolor': 'red', 'markeredgecolor': 'red', 'markeredgewidth': 0.8},
            'black', '-', 
            {'markerfacecolor': 'black', 'markeredgecolor': 'black', 'markeredgewidth': 1}
        ),
        legend_elements[1]: CombinedLineHandler(
            'red', '--', 
            {'markerfacecolor': 'none', 'markeredgecolor': 'red', 'markeredgewidth': 2},
            'black', '--', 
            {'markerfacecolor': 'none', 'markeredgecolor': 'black', 'markeredgewidth': 2}
        )
    }
    
    ax1.legend(legend_elements, ['with HIs', 'no HIs'], 
               handler_map=handler_map,
               loc='upper right', 
               frameon=True,
               bbox_to_anchor=(1.025, 1.025),
               edgecolor='darkgray',
               fontsize=fontsize-8,
               facecolor='white',
               framealpha=1,
               title_fontsize=fontsize-20,
               handletextpad=0.01,
               labelspacing=0.3, 
               handlelength=2.5,  
               borderpad=0.1)
    
    # Save and display
    plt.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    main()