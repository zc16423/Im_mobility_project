
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import glob

# Global plot style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# Define race groups and corresponding filenames
groups = {
    "White": ["White 2019.csv", "White 2020.csv"],
    "Hispanic": ["Hispanic 2019.csv", "Hispanic 2020.csv"],
    "Black": ["Black 2019.csv", "Black 2020.csv"]
}

# Automatically find all CSV files in the specified directory
file_paths = glob.glob(r"D:\Desktop\Figure4_Data_2019_2020\*.csv")

# Function to load and process data
def load_and_process_data(file_paths, groups):
    data = pd.DataFrame()

    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        for group, files in groups.items():
            if file_name in files:
                df = pd.read_csv(file_path, usecols=['Baseline'])
                # Melt so that Baseline column becomes a single column (redundant here but okay)
                df = df.melt(var_name='Device', value_name='Baseline')
                df['Group'] = group
                df['Date'] = '20190313-20191231' if '2019' in file_name else '20200313-20201231'
                data = pd.concat([data, df], ignore_index=True)

    # Ensure Group order in violin plot
    data['Group'] = pd.Categorical(data['Group'], categories=["White", "Hispanic", "Black"], ordered=True)
    return data

# Load and process data
data = load_and_process_data(file_paths, groups)

# Define violin plot function
def plot_violin(data, output_path):
    sns.set_style("white")
    sns.set_palette("muted")

    fig, ax = plt.subplots(figsize=(8, 5))

    # Draw violin plot
    sns.violinplot(
        data=data, 
        x="Group", 
        y="Baseline", 
        hue="Date",
        split=True, 
        inner="quart", 
        fill=True,
        palette={"20190313-20191231": "skyblue", "20200313-20201231": "salmon"},
        ax=ax
    )

    # Title and labels
    ax.set_title("Baseline", fontsize=14)
    ax.set_xlabel("Race", fontsize=14)
    ax.set_ylabel(r"$B$", fontsize=14)

    # Format y-axis tick labels
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))
    
    # Legend
    ax.legend(title="Date", loc='upper right', fontsize=12, frameon=False)
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
    ax.tick_params(
        axis='both', 
        which='both',
        direction='out', 
        length=7, 
        width=1.5,
        color='black', 
        labelsize=12
    )
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # Save the figure
    plt.subplots_adjust(left=0.10, right=0.97, top=0.94, bottom=0.10)
    plt.savefig(output_path, format='svg')
    plt.show()

# Output path
output_path = r"D:\Desktop\Fig4h_baseline_2019_2020.svg"
plot_violin(data, output_path)
