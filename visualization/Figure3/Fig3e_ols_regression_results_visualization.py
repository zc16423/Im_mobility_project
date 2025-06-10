import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib.colors import TwoSlopeNorm

# Global plot style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
sns.set(style='white')

# Input and output directories
file_dir = r"D:\Desktop\Fig3e_regression_data"
output_dir = r"D:\Desktop\Fig3e_OLS_Heatmaps"

# Iterate through each CSV file in the directory
for file in os.listdir(file_dir):
    if file.endswith(".csv"):
        file_path = os.path.join(file_dir, file)
        data = pd.read_csv(file_path)

        # Keep only 'Variable' and 'Coefficient' columns
        data = data[['Variable', 'Coefficient']]

        # Reshape data for heatmap
        heatmap_data = pd.DataFrame(
            data['Coefficient'].values.reshape(-1, 1),
            index=data['Variable'],
            columns=['']
        )

        # Calculate figure height dynamically
        fig_height = len(data) * 1.15
        fig, ax = plt.subplots(figsize=(4, fig_height))

        # Normalize colorbar center at 0
        norm = TwoSlopeNorm(vmin=-0.63, vcenter=0, vmax=1.61)

        # Remove axis spines
        sns.despine(left=True, bottom=True)

        # Plot the heatmap
        sns.heatmap(
            heatmap_data,
            cmap='PiYG_r',
            norm=norm,
            cbar=True,
            fmt=".2f",
            linewidths=2,
            linecolor='white',
            square=True,
            ax=ax,
            cbar_kws={'orientation': 'vertical', 'shrink': 0.8, 'pad': 0.05},
            annot=True,
            annot_kws={"size": 16, "color": "black", "weight": "normal"}
        )

        # Customize colorbar ticks
        colorbar = ax.collections[0].colorbar
        colorbar.ax.tick_params(labelsize=14)
        colorbar.set_ticks([-0.6, -0.4, -0.2, 0, 0.5, 1.0, 1.5])

        # Set axis labels and titles
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        ax.set_title(file_name, fontsize=16)
        ax.set_ylabel('Coefficient', fontsize=16)
        ax.set_xticklabels([]) 
        ax.tick_params(axis='x', labelsize=16)
        ax.tick_params(axis='y', labelsize=16, labelrotation=0)

        # Save the figure
        output_file = os.path.join(output_dir, f"{file_name}.svg")
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()