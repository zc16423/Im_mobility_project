# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 20:21:48 2025

@author: 22956
"""


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

# Global plot settings
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# Define groups and their corresponding filenames
groups = {
    "White": ["White 2019.csv", "White 2020.csv"],
    "Hispanic": ["Hispanic 2019.csv", "Hispanic 2020.csv"],
    "Black": ["Black 2019.csv", "Black 2020.csv"]
}

# Automatically get all CSV file paths in the directory
file_paths = glob.glob(r"D:\Desktop\Figure4_Data_2019_2020\*.csv")

# Function to load and process the data
def load_and_process_data(file_paths, groups):
    data_frames = []
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        for group, files in groups.items():
            if file_name in files:
                # Read only the 'Time1' column
                df = pd.read_csv(file_path, usecols=['Time1'])
                df = df.melt(var_name='Device', value_name='Time1')
                df['Group'] = group
                df['Date'] = '20190313-20191231' if '2019' in file_name else '20200313-20201231'
                data_frames.append(df)
    # Combine all data into a single DataFrame
    combined_data = pd.concat(data_frames, ignore_index=True)
    # Define group order for consistent plotting
    combined_data['Group'] = pd.Categorical(combined_data['Group'],
                                            categories=["White", "Hispanic", "Black"],
                                            ordered=True)
    return combined_data

# Function to convert decimal time to 'HH:MM' format
def convert_time_to_hm(time_val):
    hours = int(time_val)
    minutes = int(round((time_val - hours) * 60))
    return f"{hours:02}:{minutes:02}"

# Function to plot the violin plot
def plot_violin(data, output_path):
    sns.set_style("white")
    sns.set_palette("muted")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.violinplot(
        data=data, x="Group", y="Time1", hue="Date",
        split=True, inner="quart", fill=True,
        palette={
            "20190313-20191231": "skyblue",
            "20200313-20201231": "salmon"
        },
        ax=ax
    )
    
    # Set y-axis limits and custom tick labels
    ax.set_ylim(10.5, 16.5)
    tick_positions = np.linspace(10.5, 16.5, num=7)
    tick_labels = [convert_time_to_hm(t) for t in tick_positions]
    ax.set_yticks(tick_positions)
    ax.set_yticklabels(tick_labels)
    
    # Axis labels and title
    ax.set_title("Phase Angle", fontsize=14)
    ax.set_xlabel("Race", fontsize=14)
    ax.set_ylabel(r"Time of valley ($\phi$)", fontsize=14)
    
    # Customize legend
    ax.legend(title="Date", loc='lower right', fontsize=12, frameon=False)
    ax.grid(False)
    
    # Customize axis spines
    for spine_location, spine in ax.spines.items():
        if spine_location in ['left', 'bottom']:
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
    
    # Save the figure
    plt.subplots_adjust(left=0.10, right=0.97, top=0.94, bottom=0.10)
    plt.savefig(output_path, format='svg')
    plt.show()

# Load and plot the data
data = load_and_process_data(file_paths, groups)
output_path = r"D:\Desktop\Fig4f_phase_angle_2019_2020.svg"
plot_violin(data, output_path)
