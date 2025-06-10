import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem, t

# Set global font style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# Define input and output folders
input_folder = r"D:\Desktop\Fig2a_race_fit_data"
output_folder = r"D:\Desktop\Fig2a_three_race_figure"
os.makedirs(output_folder, exist_ok=True)

# List all CSV files in the input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# Process only files with corresponding '_fit.csv'
for file_name in csv_files:
    if not file_name.endswith('_fit.csv'):
        fit_file_name = file_name.replace('.csv', '_fit.csv')
        if fit_file_name in csv_files:
            file_path_data = os.path.join(input_folder, file_name)
            file_path_fit = os.path.join(input_folder, fit_file_name)
            
            # Load CSV data
            data_empirical = pd.read_csv(file_path_data)
            data_fit = pd.read_csv(file_path_fit)
            
            # Calculate mean and standard error for each hour
            hours = np.arange(24)
            means = data_empirical.mean(axis=0)
            stderr = data_empirical.sem(axis=0)
            
            # Calculate 95% confidence intervals
            confidence_level = 0.95
            ci = stderr * t.ppf((1 + confidence_level) / 2., len(data_empirical) - 1)
            means = np.concatenate([means, [means[0]]])  # Close the circle
            ci = np.concatenate([ci, [ci[0]]])
            
            # Map hours to angles
            angles = np.deg2rad(np.linspace(0, 360, 25, endpoint=True))
            
            # Extract amplitude, phase angle, and baseline from fit data
            amplitudes = data_fit['Amplitude']
            phase_angles = data_fit['Phase Angle']
            baselines = data_fit['Baseline']
            
            # Define x range for model curves (0 to 2π)
            x = np.linspace(0, 2 * np.pi, 1000)
            
            # Create polar plot
            fig = plt.figure(figsize=(5.5, 5.5))
            ax = fig.add_subplot(projection='polar')
            
            # Plot empirical means
            ax.plot(angles, means, color='#4b6aa8', linewidth=4, label='Empirical')
            
            # Plot confidence intervals
            ax.fill_between(
                angles,
                means - ci,
                means + ci,
                color='#4b6aa8',
                linewidth=0,
                alpha=0.5,
                label=r'95% CI'
            )
            
            # Plot model fit curves
            for a, b, c in zip(amplitudes, phase_angles, baselines):
                y = a * np.sin(x + b) + c
                ax.plot(x, y, color='#ee6666', linestyle='--', linewidth=4, label='Model')
            
            # Set plot title
            plot_title = file_name.replace('.csv', '')
            ax.set_title(
                plot_title,
                va='bottom',
                fontsize=32,
                weight='bold',
                pad=20,
                backgroundcolor='#f0a02f',
                color='white'
            )
            
            # Configure polar plot
            ax.set_theta_direction(-1)
            ax.set_theta_offset(np.pi / 2.0)
            
            # Set angle labels
            ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2])
            ax.set_xticklabels(['00:00', '06:00', '12:00', '18:00'], fontsize=24)
            
            # Grid and axis styles
            ax.grid(True, linestyle='--', color='gray', linewidth=1.5, alpha=0.5)
            ax.set_facecolor('white')
            ax.tick_params(labelsize=24)
            
            # Customize polar spine
            ax.spines['polar'].set_linewidth(1.5)
            ax.spines['polar'].set_color('black')
            
            # Configure radial ticks
            ax.set_rticks([0.2, 0.4, 0.6], minor=False)
            ax.set_rlabel_position(-225)
            
            # Save figure
            output_path = os.path.join(output_folder, f"{plot_title}_polar_plot.svg")
            plt.legend(loc='upper right', fontsize=28, frameon=False)
            plt.subplots_adjust(left=0.1, right=0.9, top=0.84, bottom=0.06)
            plt.savefig(output_path, format='svg')
            plt.close(fig)
