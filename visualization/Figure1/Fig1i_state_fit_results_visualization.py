import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem, t

# Set global font and style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# Input and output folders
input_folder = r"D:\Desktop\Fig1i_USA_state_data"
output_folder = r"D:\Desktop\Fig1i_USA_state"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all CSV files
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# Process each pair of raw data and fit result
for file_name in csv_files:
    if file_name.endswith('_fit.csv'):
        continue

    # Look for corresponding '_fit.csv' file
    file_name_fit = file_name.replace('.csv', '_fit.csv')
    if file_name_fit not in csv_files:
        continue  

    # Read raw data
    file_path_1 = os.path.join(input_folder, file_name)
    data_1 = pd.read_csv(file_path_1)

    # Read fit data
    file_path_2 = os.path.join(input_folder, file_name_fit)
    data_2 = pd.read_csv(file_path_2)

    # Calculate mean and 95% confidence interval for each hour
    hours = np.arange(24)
    means = data_1.mean(axis=0).to_numpy()
    stderr = data_1.sem(axis=0).to_numpy()
    confidence_level = 0.95
    confidence_interval = stderr * t.ppf((1 + confidence_level) / 2., len(data_1) - 1)

    # Ensure wrap-around for polar plot
    means = np.append(means, means[0])
    confidence_interval = np.append(confidence_interval, confidence_interval[0])

    # Map hours to angles in radians
    angles = np.deg2rad(np.linspace(0, 360, 25, endpoint=True))

    # Extract model parameters
    amplitudes = data_2['Amplitude']
    phase_angles = data_2['Phase Angle']
    baselines = data_2['Baseline']

    # Prepare x values for model plot
    x = np.linspace(0, 2 * np.pi, 1000)

    # Plot polar figure
    fig = plt.figure(figsize=(4.3, 4.6))
    ax = fig.add_subplot(projection='polar')

    # Plot empirical mean
    ax.plot(angles, means, color='#4b6aa8', linewidth=4.5, label='Empirical')

    # Plot 95% confidence interval
    ax.fill_between(
        angles,
        means - confidence_interval,
        means + confidence_interval,
        color='#4b6aa8',
        alpha=0.5,
        linewidth=0,
        label='95% CI'
    )

    # Plot model predictions
    for amp, phase, base in zip(amplitudes, phase_angles, baselines):
        y_model = amp * np.sin(x + phase) + base
        ax.plot(x, y_model, color='#ee6666', linestyle='--', linewidth=4.5, label='Model')

    # Plot customization
    title = ''.join([c for c in file_name if not c.isdigit()]).replace('.csv', '')
    ax.set_title(
        title,
        va='bottom',
        fontsize=52,
        weight='bold',
        pad=0,
        backgroundcolor='#f0a02f',
        color='white'
    )

    ax.set_theta_direction(-1)  # Clockwise
    ax.set_theta_offset(np.pi / 2)  # 0:00 at top

    # Hide labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Grid lines and style
    ax.grid(True, linestyle='--', color='gray', linewidth=2, alpha=1.0)
    ax.set_facecolor('white')
    ax.tick_params(labelsize=24)

    # Polar axis style
    ax.spines['polar'].set_linewidth(2.5)
    ax.spines['polar'].set_color('black')
    ax.set_rticks([0.3, 0.6])
    ax.set_rlabel_position(-225)

    # Save figure
    output_path = os.path.join(output_folder, file_name.replace('.csv', '.svg'))
    plt.subplots_adjust(left=0, right=1, top=0.79, bottom=0)
    plt.savefig(output_path, format='svg')
    plt.close(fig)
