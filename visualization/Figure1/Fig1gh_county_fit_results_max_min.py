import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Set global font and style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
plt.style.use('seaborn-white')

# File paths
shapefile_path = r"D:\Desktop\County\county.shp"
csv_path = r"D:\Desktop\Fig1gh_county_fit_results_max_min.csv"

# Load shapefile
gdf = gpd.read_file(shapefile_path)
# Construct FIPS code
gdf['FIPS'] = gdf['STATEFP'].str.zfill(2) + gdf['COUNTYFP'].str.zfill(3)

# Load max/min data
df = pd.read_csv(csv_path, dtype={'county': str})

# Merge GeoDataFrame with CSV
merged_gdf = gdf.merge(df, left_on='FIPS', right_on='county', how='left')

# Print data checks
print("Valid data points for 'max':", merged_gdf['max'].notna().sum())
print("Unique values for 'max':", merged_gdf['max'].nunique())
print("Valid data points for 'min':", merged_gdf['min'].notna().sum())
print("Unique values for 'min':", merged_gdf['min'].nunique())

# Define colormap and value range
cmap = plt.cm.plasma_r
vmin, vmax = 0.18, 0.72

# Create figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(26, 14))

# Plot 'max' values
merged_gdf.plot(
    column='max',
    cmap=cmap,
    linewidth=0.2,
    edgecolor='#767171',
    ax=axes[0],
    missing_kwds={"color": "lightgrey"},
    legend=False,
    vmin=vmin,
    vmax=vmax
)

# Plot 'min' values
merged_gdf.plot(
    column='min',
    cmap=cmap,
    linewidth=0.2,
    edgecolor='#767171',
    ax=axes[1],
    missing_kwds={"color": "lightgrey"},
    legend=False,
    vmin=vmin,
    vmax=vmax
)

# Add titles
axes[0].set_title('Peak', fontsize=36, pad=1)
axes[1].set_title('Valley', fontsize=36, pad=1)

# Remove axes
for ax in axes:
    ax.set_axis_off()

# Create colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm.set_array([])

cbar = fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.03, pad=0.1)
cbar.set_label(r'$R(t)$', fontsize=36)
cbar.ax.tick_params(labelsize=28)

# Set colorbar ticks
ticks = np.arange(0.2, 0.8, 0.1).round(1)
cbar.set_ticks(ticks)
cbar.set_ticklabels([str(t) for t in ticks])

# Save figure
output_path = r"D:\Desktop\Fig1gh.svg"
plt.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.13)
plt.savefig(output_path, format='svg', bbox_inches='tight')
plt.close()
