
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Set global font style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# Load the dataset
file_path = r"D:\Desktop\Fig2e_state_phase_angle.csv"
df = pd.read_csv(file_path)
df = df[::-1]  

# Color mapping
colors = {
    "White": '#71b7ed',
    "Hispanic": '#f2b56f',
    "Black": '#f57c6e'
}

def transform_time(value):
    """
    Convert time string (HH:MM) to decimal hours.
    """
    try:
        if pd.isna(value):
            return None
        time_obj = pd.to_datetime(value, format='%H:%M')
        return time_obj.hour + time_obj.minute / 60
    except ValueError:
        return None

# Create figure and axis
fig, ax = plt.subplots(figsize=(7, 12))

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Add vertical grid lines
ax.xaxis.grid(True, linestyle="--", alpha=1)
ax.yaxis.grid(False)

# Plot dumbbell plots
for _, row in df.iterrows():
    x_values = {
        "White": transform_time(row['White']),
        "Hispanic": transform_time(row['Hispanic']),
        "Black": transform_time(row['Black'])
    }
    
    # Filter out None values
    valid_values = {k: v for k, v in x_values.items() if v is not None}
    
    # Always plot scatter points
    for group, x_value in valid_values.items():
        ax.scatter(
            x_value,
            row['name'],
            color=colors[group],
            s=150,
            edgecolors='black',
            linewidth=1,
            alpha=1.0
        )
    
    # Plot connecting line if more than one data point exists
    if len(valid_values) >= 2:
        sorted_x = sorted(valid_values.values())
        ax.plot(
            sorted_x,
            [row['name']] * len(sorted_x),
            color='black',
            lw=1.5
        )

# Configure x-axis
ax.set_xlim(12, 15)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x)}:00"))

# Create custom legend
handles = [
    plt.Line2D(
        [0], [0],
        marker='o',
        color='w',
        markerfacecolor=colors[k],
        markersize=10,
        markeredgecolor='black',
        label=k
    ) for k in colors
]
ax.legend(
    handles=handles,
    loc='upper right',
    fontsize=14,
    frameon=False
)

# Axis labels and tick labels
ax.set_xlabel(r"Time of valley ($\phi$)", fontsize=20)
ax.set_ylabel("State", fontsize=20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Customize left/bottom spines
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
output_path = r"D:\Desktop\Fig2e_state_phase_angle.svg"
plt.subplots_adjust(left=0.15, right=0.96, top=0.99, bottom=0.06)
plt.savefig(output_path, format='svg')
plt.show()
