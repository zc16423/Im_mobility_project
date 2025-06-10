import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import datetime
import os

# Font and Theme Setup
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# Define Paths and Settings
folder_path = r"D:\Desktop\Fig3c_three_races_time_distribution"
files = {
    "Black": "Black.csv",
    "White": "White.csv",
    "Hispanic": "Hispanic.csv"
}
colors = {
    "Black": "#d62728",
    "White": "#33bfeb",
    "Hispanic": "#ff7f0e"
}

# Time Conversion Function
def time_to_angle(time_str):
    base_time = datetime.datetime.strptime("11:00", "%H:%M")
    max_time = datetime.datetime.strptime("16:00", "%H:%M")
    current_time = datetime.datetime.strptime(time_str, "%H:%M")
    total_minutes = (max_time - base_time).total_seconds() / 60
    elapsed_minutes = (current_time - base_time).total_seconds() / 60
    return (elapsed_minutes / total_minutes) * 90

# Processing Each Group
for group, filename in files.items():
    file_path = os.path.join(folder_path, filename)
    if not os.path.exists(file_path):
        print(f"文件 {filename} 不存在，跳过。")
        continue

    # Load Data
    df = pd.read_csv(file_path)

    # Calculate Angle
    df["Angle"] = df["Time2"].apply(time_to_angle)
    mean_angle = np.radians(df["Angle"].mean())  # Mean in radians

    # Sample Data
    df_sampled = df.sample(n=min(10000, len(df)), random_state=42)

    # Plot Polar Scatter
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(5, 5))

    # Polar Settings
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1)
    ax.set_thetamin(0)
    ax.set_thetamax(90)

    # Draw Wedge Background
    wedge = patches.Wedge((0, 0), 1, 0, 90, color='white', alpha=0, linewidth=1.5)
    ax.add_patch(wedge)

    # Generate Scatter Points
    radii = np.random.uniform(0.15, 1, len(df_sampled))
    angles = np.radians(df_sampled["Angle"])

    ax.scatter(angles, radii,
               color=colors[group],
               s=5, alpha=0.5, edgecolors='none')

    # Mean Line
    ax.plot([mean_angle, mean_angle], [0, 1],
            color='black', linestyle='--', linewidth=1.5,
            label=r"Mean valley of time ($\phi$)")

    # Customize Ticks
    tick_labels = ["11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
    tick_angles = np.radians(np.linspace(0, 90, len(tick_labels)))
    ax.set_xticks(tick_angles)
    ax.set_xticklabels(tick_labels, fontsize=16)
    ax.set_yticks([])

    # Grid and Borders
    ax.grid(True, linewidth=1.5)
    ax.spines['polar'].set_linewidth(1.5)

    # Title and Legend
    ax.set_title(group, fontsize=20, pad=5)
    ax.legend(loc="upper right", fontsize=16, frameon=False)
    
    # Save Figure
    output_path = os.path.join(folder_path, f"PolarScatter_{group}.svg")
    plt.savefig(output_path, format='svg', bbox_inches='tight')
    plt.show()
