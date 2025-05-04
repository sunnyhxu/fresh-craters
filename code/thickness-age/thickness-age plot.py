import pandas as pd
import matplotlib.pyplot as plt

# Read and preprocess the data
df = pd.read_excel('thickness-age.xls')
df['thickness'] = df['thickness'].round(1)
df['age'] = df['age'].round(2)
df['min'] = df['min'].round(1)
df['max'] = df['max'].round(1)

# Define color mapping
color_map_default = {
    'A1': 'red',
    'A2': 'purple',
    'Oberbeck 1968': 'pink',
    'Nakamura 1975': 'green',
    'Bart 2011': 'blue',
    'Fa 2014': 'orange',
    'Di 2016': 'black'
}

color_map = {
    'A1': 'red',
    'A2': 'red'
}

# Plot the scatter plot
plt.figure(figsize=(10, 6))

for site, group in df.groupby('site'):
    if site == 'A1' or site == 'A2':
        yerr = [group['thickness'] - group['min'], group['max'] - group['thickness']]
        plt.errorbar(group['age'], group['thickness'], yerr=yerr, fmt='o', color=color_map_default.get(site, 'black'), label=site)
    else:
        plt.scatter(group['age'], group['thickness'], color=color_map_default.get(site, 'black'), label=site)

# Customize plot
plt.xlabel('Surface Age (Ga)')
plt.ylabel('Regolith Thickness (m)')
plt.title('Regolith Thickness vs Surface Age')
plt.xlim(2, 4)
plt.ylim(0, 14)
plt.legend()
plt.grid(True)

# Show the plot
plt.show()