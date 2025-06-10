import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os
import matplotlib.collections as collections
import matplotlib.colors as mcolors

# Set global font style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
sns.set_theme(style="whitegrid")

# Define folder path
path = r"D:\Desktop\Fig2b_range_data"

# Load all CSV files from the folder and concatenate them
all_files = glob.glob(os.path.join(path, "*.csv"))
file_names = [os.path.splitext(os.path.basename(f))[0] for f in all_files]
combined_df = pd.concat(
    [pd.read_csv(f)[['Range']] for f in all_files],
    axis=1
)
combined_df.columns = file_names

# Arrange columns in the desired order
expected_columns = ['White', 'Hispanic', 'Black']
combined_df = combined_df[[col for col in expected_columns if col in combined_df.columns]]

# Plot violin plot
plt.figure(figsize=(6, 5))
ax = sns.violinplot(
    data=combined_df,
    bw_adjust=0.5,
    cut=1,
    linewidth=1.5,
    palette=['#71b7ed', '#f57c6e', '#f2b56f'],
    inner="box"
)

# Set x-axis labels
violin_centers = ax.get_xticks()
plt.xticks(
    violin_centers,
    combined_df.columns,
    rotation=0,
    ha='center',
    fontsize=20
)

# Set y-axis limits and ticks
plt.ylim(0.11, 0.42)
plt.yticks([i / 100 for i in range(11, 43, 5)], fontsize=18)
plt.ylabel(r'$2A$', fontsize=20)
plt.title('Range', fontsize=28, color='#333333')

# Customize violin fill color and edge
palette = ['#71b7ed', '#f57c6e', '#f2b56f']
for idx, violin in enumerate(ax.collections):
    if isinstance(violin, collections.PolyCollection):
        violin.set_edgecolor('black')
        violin.set_linewidth(1.0)
        rgba_color = mcolors.to_rgba(palette[idx % len(palette)], alpha=0.7)
        violin.set_facecolor(rgba_color)

plt.grid(False)

# Customize axis spines
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
    color='black'
)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Save figure
plt.subplots_adjust(left=0.12, right=0.98, top=0.90, bottom=0.10)
output_path = r"D:\Desktop\Fig2b_range.svg"
plt.savefig(output_path, dpi=300)
plt.show()
