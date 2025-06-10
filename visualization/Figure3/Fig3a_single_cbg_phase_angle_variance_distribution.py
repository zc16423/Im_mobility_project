import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Global font configuration
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
sns.set(style='white')

# Define data file paths
file_paths = {
    'White': r"D:\Desktop\Fig3a_single_cbg_variance\White.csv",
    'Hispanic': r"D:\Desktop\Fig3a_single_cbg_variance\Hispanic.csv",
    'Black': r"D:\Desktop\Fig3a_single_cbg_variance\Black.csv"
}

# Define colors
colors = {
    'White': '#33bfeb',
    'Hispanic': '#ff7f0e',
    'Black': '#d62728'
}

# Merge data from all groups
data = pd.DataFrame()
for group, file_path in file_paths.items():
    df = pd.read_csv(file_path)
    df['Group'] = group
    data = pd.concat([data, df], ignore_index=True)

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 5))

# Plot KDEs for each group
for group, color in colors.items():
    sns.kdeplot(
        data=data[data['Group'] == group],
        x='Variance',
        ax=ax,
        color=color,
        label=group,
        fill=True,
        alpha=0.6,
        linewidth=2
    )

# Configure axis labels
ax.set_xlabel(r'Variance ($\phi$)', fontsize=16)
ax.set_ylabel('Density', fontsize=16)

# Remove background grid
ax.grid(False)

# Customize spines
for spine_location, spine in ax.spines.items():
    if spine_location in ['left', 'bottom']:
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1.5)
    else:
        spine.set_visible(False)

# Customize tick parameters
ax.tick_params(
    axis='both',
    which='both',
    direction='out',
    length=7,
    width=1.5,
    color='black',
    labelsize=16
)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Add legend
ax.legend(title=None, loc='upper right', fontsize=16, frameon=False)

# Save figure
plt.subplots_adjust(left=0.12, right=0.95, top=0.98, bottom=0.12)
output_path = r"D:\Desktop\Fig3a_variance_distribution.svg"
plt.savefig(output_path, format='svg')
plt.show()
