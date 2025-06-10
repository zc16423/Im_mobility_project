import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrow  

# Set global font style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# Load shapefile
shp_path = r"D:\Desktop\St. Louis\29510Export_Output_2.shp"
gdf = gpd.read_file(shp_path)

# Ensure GEOID is a string
gdf["GEOID"] = gdf["GEOID"].astype(str)

# Define CSV files with their color mapping
csv_files = {
    "White": (r"D:\Desktop\Fig3d_St.Louis_data\White.csv", "#33bfeb"),
    "Black": (r"D:\Desktop\Fig3d_St.Louis_data\Black.csv", "#d62728"),
}

# Read CSV files
dfs = {}
for key, (file, color) in csv_files.items():
    df = pd.read_csv(file)
    df["GIDBG"] = df["GIDBG"].astype(str)
    df["color"] = color
    dfs[key] = df

# Merge all data into a single GeoDataFrame
df_all = pd.concat(dfs.values(), ignore_index=True)
merged = gdf.merge(df_all, left_on="GEOID", right_on="GIDBG", how="right")

# Convert to WGS84 (EPSG:4326)
merged = merged.to_crs(epsg=4326)

# Convert polygons to centroids for scatter plotting
merged["geometry"] = merged["geometry"].centroid

# Define scatter size mapping based on Variance
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

merged["size"] = merged["Variance"].apply(map_size)

# Plot
fig, ax = plt.subplots(figsize=(12.5, 12.5))
gdf.plot(ax=ax, color="lightgrey", edgecolor="white")

# Plot scatter points for each group
for key, (file, color) in csv_files.items():
    subset = merged[merged["color"] == color]
    ax.scatter(
        subset.geometry.x,
        subset.geometry.y,
        s=subset["size"],
        color=color,
        label=key,
        alpha=0.8,
        edgecolors="black",
        linewidth=0.7
    )

# Add scale bar
scale_length = 5000
latitude_stlouis = 38.63
conversion_factor = 111320 * np.cos(np.radians(latitude_stlouis))
dist_in_deg = scale_length / conversion_factor

ax.plot([min(gdf.bounds.minx), min(gdf.bounds.minx) + dist_in_deg],
        [min(gdf.bounds.miny), min(gdf.bounds.miny)],
        color='black', linewidth=2)
ax.text(min(gdf.bounds.minx) + dist_in_deg / 2,
        min(gdf.bounds.miny) + 0.001,
        f'{scale_length} m',
        fontsize=12, ha='center')

# Add main title
ax.set_title("St. Louis", fontsize=20)

# Set axis labels and grid
ax.set_xlabel("Longitude", fontsize=16)
ax.set_ylabel("Latitude", fontsize=16)
ax.grid(False)

# Customize tick labels
ax.tick_params(axis="x", which="major", bottom=True, labelsize=14)
ax.tick_params(axis="y", which="major", left=True, labelsize=14)

# Create custom legend
handles = [
    plt.scatter([], [], s=200, color=color, label=key, edgecolors="black", linewidth=0.7)
    for key, (file, color) in csv_files.items()
]
ax.legend(handles=handles, loc='upper left', fontsize=14, frameon=False)

# Save figure
plt.savefig(r"D:\Desktop\Fig3d_St.Louis_variance_map.svg", format="svg", bbox_inches="tight")
plt.show()
