import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Matplotlib settings
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# Load shapefile
shp_path = r"D:\Desktop\Atlanta\13121Export_Output_2.shp"
gdf = gpd.read_file(shp_path)

# Ensure GEOID is string
gdf["GEOID"] = gdf["GEOID"].astype(str)

# Define CSV files and color mapping
csv_files = {
    "White": (r"D:\Desktop\Fig3d_Atlanta_data\White.csv", "#33bfeb"),
    "Hispanic": (r"D:\Desktop\Fig3d_Atlanta_data\Hispanic.csv", "#ff7f0e"),
    "Black": (r"D:\Desktop\Fig3d_Atlanta_data\Black.csv", "#d62728"),
}

# Load dataframes
dfs = {}
for group, (file, color) in csv_files.items():
    df = pd.read_csv(file)
    df["GIDBG"] = df["GIDBG"].astype(str)
    df["color"] = color
    dfs[group] = df

# Merge all groups into one DataFrame
df_all = pd.concat(dfs.values(), ignore_index=True)
merged = gdf.merge(df_all, left_on="GEOID", right_on="GIDBG", how="right")
merged = merged.to_crs(epsg=4326)

# Replace geometries with centroids
merged["geometry"] = merged["geometry"].centroid

# Define size mapping function
def map_size(value):
    if 0.03 <= value < 0.15:
        return 10
    elif 0.15 <= value < 0.27:
        return 200
    elif 0.27 <= value < 0.39:
        return 400
    elif 0.39 <= value < 0.50:
        return 600
    elif 0.50 <= value < 0.62:
        return 800
    elif 0.62 <= value < 0.74:
        return 1000
    else:
        return 50

# Apply size mapping
merged["size"] = merged["Variance"].apply(map_size)

# Plotting
fig, ax = plt.subplots(figsize=(12.5, 12.5))
gdf.plot(ax=ax, color="lightgrey", edgecolor="white")

# Plot scatter points for each group
for group, (_, color) in csv_files.items():
    subset = merged[merged["color"] == color]
    ax.scatter(
        subset.geometry.x,
        subset.geometry.y,
        s=subset["size"],
        color=color,
        label=group,
        alpha=0.8,
        edgecolors="black",
        linewidth=0.7
    )

# Add scale bar
scale_length_m = 5000
latitude_atlanta = 33.75
conversion_factor = 111320 * np.cos(np.radians(latitude_atlanta))
scale_length_deg = scale_length_m / conversion_factor

scale_start_x = gdf.bounds.minx.min()
scale_start_y = gdf.bounds.miny.min()

ax.plot(
    [scale_start_x, scale_start_x + scale_length_deg],
    [scale_start_y, scale_start_y],
    color='black',
    linewidth=2
)
ax.text(
    scale_start_x + scale_length_deg / 2,
    scale_start_y + 0.001,
    f'{scale_length_m} m',
    fontsize=12,
    ha='center'
)

# Title and labels
ax.set_title("Atlanta Phase Angle Variance by CBG", fontsize=20)
ax.set_xlabel("Longitude", fontsize=16)
ax.set_ylabel("Latitude", fontsize=16)
ax.grid(False)

# Tick parameters
ax.tick_params(axis="x", which="major", bottom=True, labelsize=14)
ax.tick_params(axis="y", which="major", left=True, labelsize=14)

# Legend
handles = [
    plt.scatter([], [], s=200, color=color, label=group, edgecolors="black", linewidth=0.7)
    for group, (_, color) in csv_files.items()
]
ax.legend(handles=handles, loc='lower right', fontsize=14, frameon=False)

# Save and show the figure
output_path = r"D:\Desktop\Fig3d_Atlanta_variance_map.svg"
plt.savefig(output_path, format="svg", bbox_inches="tight")
plt.show()
