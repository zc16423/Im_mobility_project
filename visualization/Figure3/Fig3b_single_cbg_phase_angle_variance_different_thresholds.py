import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

# Font and Theme Setup
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
sns.set_theme(style="white")

# Load Data
white_data = pd.read_csv(r"D:\Desktop\Fig3b_threshold_Phase_angle_variance\White.csv")
hispanic_data = pd.read_csv(r"D:\Desktop\Fig3b_threshold_Phase_angle_variance\Hispanic.csv")
black_data = pd.read_csv(r"D:\Desktop\Fig3b_threshold_Phase_angle_variance\Black.csv")

# Add group labels
white_data['Group'] = 'White'
hispanic_data['Group'] = 'Hispanic'
black_data['Group'] = 'Black'

# Combine datasets
combined_data = pd.concat([white_data, hispanic_data, black_data], ignore_index=True)

# Color and Marker Settings
color_map = {
    'White': '#33bfeb',
    'Hispanic': '#ff7f0e',
    'Black': '#d62728'
}
marker_map = {
    'White': 'o',
    'Hispanic': 's',
    'Black': 'D'
}

# Plotting
fig, ax = plt.subplots(figsize=(9, 5))

for group in ['White', 'Hispanic', 'Black']:
    group_data = combined_data[combined_data['Group'] == group]
    
    prev_collections = len(ax.collections)
    
    sns.regplot(
        data=group_data,
        x='Threshold',
        y='Mean_Variance',
        ax=ax,
        label=group,
        color=color_map[group],
        marker=marker_map[group],
        scatter_kws={'s': 40},
        ci=95,
        robust=True
    )
    
    new_collections = ax.collections[prev_collections:]
    for coll in new_collections:
        if isinstance(coll, PolyCollection):
            coll.set_alpha(0.4)
            
# Axis Labels and Formatting
ax.set_xlabel("Percentage (%)", fontsize=16)
ax.set_ylabel(r"Variance ($\phi$)", fontsize=16)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))
ax.grid(False)

# Border and Ticks
for spine_location, spine in ax.spines.items():
    if spine_location in ['left', 'bottom']:
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1.5)
    else:
        spine.set_visible(False)

ax.tick_params(
    axis='both',
    which='both',
    direction='out',
    length=7,
    width=1.5,
    color='black',
    labelsize=14
)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Legend
ax.legend(title=None, loc='upper left', fontsize=14, frameon=False)

# Save Figure
plt.subplots_adjust(left=0.12, right=0.95, top=0.98, bottom=0.12)
output_path = r"D:\Desktop\Fig3b_variance_threshold.svg"
plt.savefig(output_path, format='svg')
plt.show()
