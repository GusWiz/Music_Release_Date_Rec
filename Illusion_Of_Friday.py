import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data and clean dates
df = pd.read_csv('track_data_final.csv')
df['release_date'] = pd.to_datetime(df['album_release_date'], errors='coerce')
df = df.dropna(subset=['release_date', 'track_popularity']) # remove NaN datapoints.

# Filter ONLY for Singles
df_single = df[df['album_type'] == 'single'].copy()

# Extract day of week
df_single['day_of_week'] = df_single['release_date'].dt.day_name()
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Group data
day_stats = df_single.groupby('day_of_week').agg(
    track_count=('track_popularity', 'count'),
    median_pop=('track_popularity', 'median')
).reindex(days_order)
df_single.to_csv("Single_Dataset.csv")
# Plotting the Combo Chart
fig, ax1 = plt.subplots(figsize=(10, 6))

# Volume Bar Chart (Gray)
ax1.bar(day_stats.index, day_stats['track_count'], color='darkorange', alpha=0.7)
ax1.set_ylabel('Total Singles Released', color='darkorange')

# Popularity Line Chart (Green)
ax2 = ax1.twinx()
ax2.plot(day_stats.index, day_stats['median_pop'], color="#221BD8", marker='o', linewidth=3)
ax2.set_ylabel('Median Popularity Score', color='#221BD8', fontweight='bold')

sns.despine(right=False)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

plt.title('The Friday Trap: High Volume vs. Lower Popularity for Singles', loc='Center', pad=15)
plt.savefig('01_friday_trap_combo_chart.png', dpi=300, bbox_inches='tight')
plt.show()


# Filter for just Albums and Singles on Fridays
friday_music = df[df['release_date'].dt.day_name() == 'Friday']
friday_comp = friday_music[friday_music['album_type'].isin(['album', 'single'])]

# Calculate median popularity
type_stats = friday_comp.groupby('album_type')['track_popularity'].median().sort_values()

# Plot Horizontal Bar Chart
plt.figure(figsize=(8, 4))
bars = sns.barplot(x=type_stats.values, hue=type_stats.index, palette=['#221BD8', '#FA8C0F'], legend=True)

plt.legend(title='Album Type')
sns.despine(left=True, bottom=True)
plt.tick_params(axis='both', which='both', length=0)
plt.xlabel('Median Popularity Score')
plt.ylabel('Release Type')
plt.title('Why Singles Fail on Friday: Albums Dominate the Algorithm', loc='left', pad=15)
plt.savefig('02_singles_vs_albums_friday.png', dpi=300, bbox_inches='tight')
plt.show()

# Extract month for Singles
df_single['month'] = df_single['release_date'].dt.month
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Group by month
monthly_pop = df_single.groupby('month')['track_popularity'].median()

# Plot
plt.figure(figsize=(10, 5))
plt.plot(month_names, monthly_pop.values, color='gray', linewidth=2, marker='o', label='All Months')

# Highlight May & June (Indices 4 and 5)
plt.plot(month_names[4:6], monthly_pop.values[4:6], color='#221BD8', linewidth=4, marker='o', markersize=8, label='Best Release Window')

sns.despine()
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.title('Target the Spring Lull: Highest Single Popularity in May & June', loc='Center')
plt.ylabel('Median Popularity Score')
plt.legend(loc='best')
plt.savefig('03_spring_lull_monthly_trends.png', dpi=300, bbox_inches='tight')
plt.show()