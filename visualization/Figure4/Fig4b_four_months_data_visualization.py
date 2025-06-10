import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import numpy as np

# Set global font and style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# File paths
file_path = r"D:\Desktop\Fig4b_USA_four_months.csv"
output_path = r"D:\Desktop\Fig4b_USA_ratio.svg"

# Load data
data = pd.read_csv(file_path)

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day

# Filter data for weekdays (Mon-Fri) in 2020
data_2020 = data[(data['Year'] == 2020) & (data['Date'].dt.dayofweek < 5)]

# Create a 3x4 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(15, 12.5))
fig.subplots_adjust(wspace=0.01)
fig.tight_layout(pad=1)
sns.set(style='white')

# Shared colorbar axis
cbar_ax = fig.add_axes([0.3, 0.04, 0.5, 0.025])

# Loop through each month and plot the heatmap
for month in range(1, 13):
    ax = axes[(month - 1) // 4, (month - 1) % 4]
    month_data = data_2020[data_2020['Month'] == month].copy()
    month_data.set_index('Date', inplace=True)

    # Create a full calendar for the month with NaNs as default
    cal_data = pd.DataFrame(
        index=pd.date_range(
            start=f'2020-{month:02d}-01',
            end=f'2020-{month:02d}-{calendar.monthrange(2020, month)[1]}'
        )
    )
    cal_data['Average'] = np.nan
    cal_data.update(month_data['Average'])

    # Calculate week number within the month (1-based)
    cal_data['Week'] = cal_data.index.to_series().apply(lambda x: (x.day - 1) // 7 + 1)
    cal_data['Day'] = cal_data.index.weekday

    # Pivot data to create a heatmap: Week (rows) x Day of week (columns)
    cal_pivot = cal_data.pivot('Week', 'Day', 'Average')
    cal_pivot = cal_pivot.iloc[:, :5]

    # Draw heatmap
    sns.heatmap(
        cal_pivot,
        ax=ax,
        cmap='PiYG_r',
        cbar=True,
        cbar_kws={'orientation': 'horizontal'},
        vmin=0.385,
        vmax=0.575,
        cbar_ax=cbar_ax,
        linewidths=1,
        linecolor='white'
    )

    # Formatting
    ax.set_title(calendar.month_abbr[month], fontsize=16)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.tick_params(axis='x', length=0)
    ax.spines['top'].set_visible(False)
    ax.set_xticklabels(['M', 'T', 'W', 'T', 'F'], fontsize=12)
    ax.set_yticklabels([f'Week {i}' for i in range(1, len(cal_pivot.index) + 1)], fontsize=10)

# Colorbar label
cbar_ax.text(0, 0, 'National Emergency (2020-03-13)', ha='center', va='center', fontsize=12)

# Overall figure title
fig.suptitle(r'24-hours Mean $R(t)$', fontsize=14, y=0.02)

# Save figure
plt.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.08)
plt.savefig(output_path, dpi=300, format='svg')
plt.close()
