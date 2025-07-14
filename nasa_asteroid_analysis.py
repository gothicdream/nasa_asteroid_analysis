"""
NASA Asteroid Data Visualization
--------------------------------
This script fetches Near-Earth Object (NEO) data from NASA's API, processes the information,
and visualizes the asteroid diameter and miss distance.

Requirements:
- requests
- pandas
- matplotlib
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt

# === Configuration ===
API_KEY = 'API_KEY'
API_URL = f'https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={API_KEY}'

# === Fetch Data ===
response = requests.get(API_URL)
data = response.json()

near_earth_objects = data.get('near_earth_objects', [])

# === Process Data ===
processed_data = []

for asteroid in near_earth_objects:
    name = asteroid.get('name')
    diameter = asteroid['estimated_diameter']['kilometers']['estimated_diameter_max']
    
    if asteroid['close_approach_data']:
        close_approach = asteroid['close_approach_data'][0]
        approach_date = close_approach.get('close_approach_date')
        miss_distance = float(close_approach['miss_distance']['kilometers'])
    else:
        approach_date = None
        miss_distance = None

    processed_data.append({
        'name': name,
        'estimated_diameter': diameter,
        'close_approach_date': approach_date,
        'miss_distance': miss_distance
    })

# Convert to DataFrame
df = pd.DataFrame(processed_data)
print(df)

# === Visualization ===

# Bar Chart: Estimated Diameters
plt.figure(figsize=(12, 6))
plt.bar(df['name'], df['estimated_diameter'], color='steelblue')
plt.xticks(rotation=90)
plt.title('Estimated Diameter of Near-Earth Objects')
plt.xlabel('Asteroid Name')
plt.ylabel('Diameter (km)')
plt.tight_layout()
plt.show()

# Scatter Plot: Miss Distances by Date
# Remove rows with missing data for plotting
scatter_df = df.dropna(subset=['close_approach_date', 'miss_distance'])

plt.figure(figsize=(12, 6))
plt.scatter(scatter_df['close_approach_date'], scatter_df['miss_distance'], color='crimson')
plt.xticks(rotation=45)
plt.title('Miss Distance of Near-Earth Objects')
plt.xlabel('Close Approach Date')
plt.ylabel('Miss Distance (km)')
plt.tight_layout()
plt.show()
