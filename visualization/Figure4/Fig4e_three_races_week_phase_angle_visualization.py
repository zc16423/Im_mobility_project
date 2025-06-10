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

# Helper function to convert time values to HH:MM format
def convert_time_to_hm(time_val):
    hours = int(time_val)
    minutes = int((time_val - hours) * 60)
    return f"{hours:02d}:{minutes:02d}"

# Set y-axis ticks and labels
ax.set_ylim(12, 15)
yticks = np.linspace(12, 15, num=7)
ytick_labels = [convert_time_to_hm(t) for t in yticks]
ax.set_yticks(yticks)
ax.set_yticklabels(ytick_labels)

# Load data and plot
for label, color in zip(labels, colors):
    data = pd.read_csv(folder_path / f"{label}.csv")
    sns.lineplot(x="Week", y="Time1", data=data, label=label,
                 color=color, linewidth=3, ax=ax)

# Title and axis labels
ax.set_title("Phase Angle", fontsize=14)
ax.set_xlabel("Week (2020)", fontsize=14)
ax.set_ylabel(r"Time of Valley ($\phi$)", fontsize=14)
ax.set_xticks(np.arange(1, 54, step=3))

# Add vertical line and annotation
week_of_emergency = 11
ax.axvline(week_of_emergency, linestyle='--', linewidth=0.8, color='#333333')
ax.text(week_of_emergency, ax.get_ylim()[1] * 0.99,
        'National Emergency (2020-03-13)',
        color='black', ha='left', va='top', fontsize=12)

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
plt.subplots_adjust(left=0.10, right=0.97, top=0.94, bottom=0.10)
plt.savefig(r"D:\Desktop\Fig4e_week_phase_angle.svg", format='svg')
plt.show()
