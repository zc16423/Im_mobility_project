import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set global font style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# Load CSV file
file_path = r"D:\Desktop\Fig1e_fitting_data_2019.csv"
data = pd.read_csv(file_path)

# Extract columns: Amplitude, Phase Angle, Baseline
amplitudes = data['Amplitude']
phase_angles = data['Phase Angle']
baselines = data['Baseline']

# Define x-axis range from 0 to 2π
x = np.linspace(0, 2 * np.pi, 1000)

# Create the plot
fig, ax = plt.subplots(figsize=(12, 7.5))
gray_color = '#D3D3D3'

# Plot each row's sine curve
for a, b, c in zip(amplitudes, phase_angles, baselines):
    y = a * np.sin(x + b) + c
    ax.plot(x, y, color=gray_color, linewidth=0.5)

# Plot the mean curve in red
mean_amplitude = 0.1315
mean_phase_angle = 1.1238
mean_baseline = 0.4475
y_mean = mean_amplitude * np.sin(x + mean_phase_angle) + mean_baseline
ax.plot(x, y_mean, color='#ee6666', linewidth=3, label='USA 2019 (Mean)')

# Add legend
ax.legend(loc='lower left', fontsize=28, frameon=False)

# Set labels and title
ax.set_xlabel(r'$x_t$', fontsize=28)
ax.set_ylabel(r'$R(t)$', fontsize=28)
ax.grid(False)

# Customize axis spines
for spine_location, spine in ax.spines.items():
    if spine_location in ['left', 'bottom']:
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(2)
    else:
        spine.set_visible(False)

# Customize tick parameters
ax.tick_params(axis='both', which='both',
               direction='out', length=10, width=2,
               color='black', labelsize=28)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Save the figure
plt.subplots_adjust(left=0.1, right=0.99, top=0.99, bottom=0.11)
output_path = r"D:\Desktop\Fig1e.svg"
plt.savefig(output_path, format='svg')
plt.show()
