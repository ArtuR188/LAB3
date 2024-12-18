import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

df['date'] = pd.to_datetime(df['date'])
latest_date = df['date'].max()
df_latest = df[df['date'] == latest_date]

world = world.rename(columns={'name': 'location'})
merged = world.set_index('location').join(df_latest.set_index('location'))

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged.plot(column='total_cases', ax=ax, legend=True,
            legend_kwds={'label': "Total COVID-19 Cases by Country", 'orientation': "horizontal"})
ax.set_title(f"COVID-19 Cases by Country as of {latest_date.strftime('%B %d, %Y')}")
plt.show()

country = 'Ukraine'
df_country = df[df['location'] == country]

plt.figure(figsize=(10, 6))
plt.plot(df_country['date'], df_country['new_cases'], label='New Cases')
plt.plot(df_country['date'], df_country['total_cases'], label='Total Cases')
plt.title(f"COVID-19 Trend in {country}")
plt.xlabel('Date')
plt.ylabel('Cases')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

df_growth = df.groupby('location').last()[['total_cases']].sort_values('total_cases', ascending=False)
top_growth = df_growth.head(5)
bottom_growth = df_growth.tail(5)

print("Countries with the most cases:")
print(top_growth)

print("\nCountries with the least cases:")
print(bottom_growth)
