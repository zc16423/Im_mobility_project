import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set global font style
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'

# City order and assigned colors
order = ['New York', 'Los Angeles', 'Chicago']
colors = ['#4b6aa8', '#f0a02f', '#ee6666']

# Create continuous hourly time index
start_date = pd.to_datetime('2019/4/1 0:00')
end_date = pd.to_datetime('2019/4/5 23:00')
time_index = pd.date_range(start=start_date, end=end_date, freq='H')

# Load CSV data for each city
data_dict = {}
for name in order:
    filepath = rf"D:\Desktop\Fig1c_three_city_data\{name}.csv"
    data_dict[name] = pd.read_csv(filepath)
    data_dict[name]['Date'] = pd.to_datetime(data_dict[name]['Date'])

# Create a new DataFrame indexed by the continuous time index
new_data = pd.DataFrame(index=time_index)

# Populate the new DataFrame with hourly data
for name, data in data_dict.items():
    for _, row in data.iterrows():
        date = row['Date']
        for hour in range(24):
            time = date + pd.Timedelta(hours=hour)
            new_data.loc[time, name] = row[f'{hour}:00']

# Plotting
plt.figure(figsize=(17, 8))
ax = plt.gca()

# Add alternating background shading (each day is 24 hours)
for day in range(5):
    start_time = start_date + pd.Timedelta(days=day)
    time_range_start = start_time
    time_range_end = start_time + pd.Timedelta(hours=24)

    time_start_num = mdates.date2num(time_range_start)
    time_end_num = mdates.date2num(time_range_end)

    # Alternate background color for each day
    if day % 2 == 0:
        ax.axvspan(time_start_num, time_end_num, facecolor='#d9d9d9', alpha=0.3)
    else:
        ax.axvspan(time_start_num, time_end_num, facecolor='#f2f2f2', alpha=0)

# Plot each city's data
for i, name in enumerate(order):
    plt.plot(new_data.index, new_data[name], marker='o', color=colors[i],
             label=name, markersize=8, linewidth=2)

# Axis labels and title
plt.xlabel('Time', fontsize=28)
plt.ylabel(r'$R(t)$', fontsize=28)
plt.title('Weekly Patterns', fontsize=32)

# Format x-axis as month-day
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

# Y-axis limits and grid
plt.ylim(0.2, 0.7)
plt.grid(False)

# Customize axes spines
for spine_location, spine in ax.spines.items():
    if spine_location in ['left', 'bottom']:
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(2)
    else:
        spine.set_visible(False)

# Tick parameters
ax.tick_params(axis='both', which='both', direction='out',
               length=10, width=2, color='black', labelsize=28)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Save the figure
plt.legend(loc='upper right', fontsize=28, frameon=False)
plt.subplots_adjust(left=0.08, right=0.97, top=0.92, bottom=0.1)
plt.savefig(r'D:\Desktop\Fig1c.svg', format='svg')
plt.show()
