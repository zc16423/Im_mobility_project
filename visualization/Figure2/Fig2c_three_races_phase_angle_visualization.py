import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os
import numpy as np
import matplotlib.collections as collections
import matplotlib.colors as mcolors

# Set global font style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
sns.set_theme(style="whitegrid")

# Define folder path
path = r"D:\Desktop\Fig2c_phase_angle_data"

# Load all CSV files and concatenate them
all_files = glob.glob(os.path.join(path, "*.csv"))
file_names = [os.path.splitext(os.path.basename(f))[0] for f in all_files]
combined_df = pd.concat(
    [pd.read_csv(f)[['Time1']] for f in all_files],
    axis=1
)
combined_df.columns = file_names

# Arrange columns in the desired order
expected_columns = ['White', 'Hispanic', 'Black']
combined_df = combined_df[[col for col in expected_columns if col in combined_df.columns]]

# Helper function: Convert decimal time to HH:MM format
def convert_time_to_hm(time_val):
    if isinstance(time_val, (int, float)):
        hours = int(time_val)
        minutes = int(round((time_val - hours) * 60))
        return f"{hours:02}:{minutes:02}"
    return str(time_val)

# Get all unique time values (flatten and remove NaNs)
time_values = combined_df.values.flatten()
time_values = time_values[~np.isnan(time_values)]
time_values_sorted = sorted(set(time_values))

# Generate y-axis ticks
tick_count = 10
filtered_ticks = np.linspace(
    min(time_values_sorted),
    max(time_values_sorted),
    num=tick_count
)
filtered_ticks = np.round(filtered_ticks, 2)
filtered_labels = [convert_time_to_hm(t) for t in filtered_ticks]

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
    fontsize=18
)

# Set y-axis ticks and labels
ax.set_yticks(filtered_ticks)
ax.set_yticklabels(filtered_labels, fontsize=18)

# Axis labels
plt.xlabel('Race', fontsize=20)
plt.ylabel(r"Time of Valley ($\phi$)", fontsize=20)
plt.title('Phase Angle', fontsize=28, color='#333333')

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
for spine_loc, spine in ax.spines.items():
    if spine_loc in ['left', 'bottom']:
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
plt.subplots_adjust(left=0.13, right=0.99, top=0.90, bottom=0.10)
output_path = r"D:\Desktop\Fig2c_phase_angle.svg"
plt.savefig(output_path, dpi=300)
plt.show()
