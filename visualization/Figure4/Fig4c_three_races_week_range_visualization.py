import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Plot settings
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
sns.set_theme(style="whitegrid")

# File paths and settings
folder_path = Path(r"D:\Desktop\Fig4_weekly_fit_means")
labels = ['White', 'Hispanic', 'Black']
colors = ['#33bfeb', '#ff7f0e', '#d62728']

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 5))

# Load data and plot
for label, color in zip(labels, colors):
    data = pd.read_csv(folder_path / f"{label}.csv")
    sns.lineplot(x="Week", y="Range", data=data, label=label,
                 color=color, linewidth=3, ax=ax)

# Add vertical line and annotation
week_of_emergency = 11
ax.axvline(week_of_emergency, linestyle='--', linewidth=0.8, color='#333333')
ax.text(week_of_emergency, ax.get_ylim()[1] * 0.95,
        'National Emergency (2020-03-13)',
        color='black', ha='left', va='top', fontsize=12)

# Title and axis labels
ax.set_title("Range", fontsize=14)
ax.set_xlabel("Week (2020)", fontsize=14)
ax.set_ylabel(r"$2A$", fontsize=14)
ax.set_xticks(np.arange(1, 54, step=3))

# Legend
ax.legend(loc='upper right', fontsize=12, frameon=False)
ax.grid(False)

# Customize axes spines
for spine_name, spine in ax.spines.items():
    if spine_name in ['left', 'bottom']:
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1.5)
    else:
        spine.set_visible(False)

# Customize tick parameters
ax.tick_params(axis='both', which='both',
               direction='out', length=7, width=1.5,
               color='black', labelsize=12)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Save figure
plt.subplots_adjust(left=0.1, right=0.99, top=0.99, bottom=0.11)
plt.savefig(r"D:\Desktop\Fig4c_week_range.svg", format='svg')
plt.show()
