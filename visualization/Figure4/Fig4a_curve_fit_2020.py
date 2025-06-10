import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set global font style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# Read CSV files
file_path_before = r"D:\Desktop\Fig4a_fit_data\USA_2020_before.csv"
file_path_during = r"D:\Desktop\Fig4a_fit_dat\USA_2020_during.csv"
data_before = pd.read_csv(file_path_before)
data_during = pd.read_csv(file_path_during)

# Extract amplitude, phase angle, and baseline columns
amplitudes_before = data_before['Amplitude']
phase_angles_before = data_before['Phase Angle']
baselines_before = data_before['Baseline']

amplitudes_during = data_during['Amplitude']
phase_angles_during = data_during['Phase Angle']
baselines_during = data_during['Baseline']

# Define x range
x = np.linspace(0, 2 * np.pi, 1000)

# Create figure and axis
fig, ax = plt.subplots(figsize=(7, 5))
gray_color = '#D3D3D3'

# Plot individual curves for 'before' data
for a, b, c in zip(amplitudes_before, phase_angles_before, baselines_before):
    y = a * np.sin(x + b) + c
    ax.plot(x, y, color=gray_color, linewidth=0.5)

# Plot individual curves for 'during' data
for a, b, c in zip(amplitudes_during, phase_angles_during, baselines_during):
    y = a * np.sin(x + b) + c
    ax.plot(x, y, color='#B0B0B0', linewidth=0.5)

# Plot mean fitted curve after National Emergency
amplitude_red = 0.0859
phase_angle_red = 1.0571
baseline_red = 0.4740
y_red = amplitude_red * np.sin(x + phase_angle_red) + baseline_red
ax.plot(x, y_red, color='#ee6666', linewidth=3, label='After National Emergency (Mean)')

# Plot mean fitted curve before National Emergency
amplitude_blue = 0.1553
phase_angle_blue = 1.2278
baseline_blue = 0.4295
y_blue = amplitude_blue * np.sin(x + phase_angle_blue) + baseline_blue
ax.plot(x, y_blue, color='#1f77b4', linewidth=3, label='Before National Emergency (Mean)')

# Add legend
ax.legend(loc='lower left', fontsize=12, frameon=False)

# Axis labels
ax.set_xlabel(r'$x_t$', fontsize=14)
ax.set_ylabel(r'$R(t)$', fontsize=14)
ax.grid(False)

# Customize axis spines
for spine_location, spine in ax.spines.items():
    if spine_location in ['left', 'bottom']:
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1.5)
    else:
        spine.set_visible(False)

# Customize tick appearance
ax.tick_params(axis='both', which='both',
               direction='out', length=7, width=1.5,
               color='black', labelsize=12)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Save figure
plt.subplots_adjust(left=0.1, right=0.99, top=0.99, bottom=0.11)
output_path = r"D:/Desktop/Fig4a_USA_2020.svg"
plt.savefig(output_path, format='svg')
plt.show()
