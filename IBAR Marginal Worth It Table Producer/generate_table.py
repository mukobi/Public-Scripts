"""This code will generate a text file named `table.txt` containing the table and an image named `heatmap.png` containing the heatmap. You can then copy the table from the text file and paste it into Google Docs, and insert the image into Google Docs as well."""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV data
# INPUT_FILE = input('Enter the path of a CSV file...\n')
INPUT_FILE = "C:/Users/Gabe/Documents/GitHub/Personal/Public-Scripts/IBAR Marginal Worth It Table Producer/SAIA Retreats (Attendees)-Worth it for Attendees .csv"
# Format filename to avoid invalid arguments (e.g. \\ on Windows, remove quotes)
INPUT_FILE = INPUT_FILE.replace('\\', '/').replace('"', '').replace("'", '')

df = pd.read_csv(INPUT_FILE)

# Rename "How good to have invited them? (How much did they improve the retreat/how valuable was it)" to "How good to have invited them?"
df = df.rename(columns={
               'How good to have invited them? (How much did they improve the retreat/how valuable was it)': 'How good to have invited them?'})

# Rename the 'Berkeley Student' and 'Stanford student' values to 'Berkeley' and 'Stanford'
df['School'] = df['School'].replace({'Berkeley student': 'Berkeley', 'Stanford student': 'Stanford'})

# Calculate the counts and percentages
pivot_table = pd.crosstab(
    df['School'], df['How good to have invited them?'], margins=True)

# Swap the "Stanford" and "Other" rows
pivot_table = pivot_table.reindex(['Stanford', 'Berkeley', 'Other', 'All'])

# Change the x-axis to go in the order [Fairly negative/made things worse, Shouldn't have invited, Unknown/neutral, Slightly beneficial, Very beneficial]
pivot_table = pivot_table[['Shouldn\'t have invited',
                           'Unknown/neutral', 'Slightly beneficial', 'Very beneficial', 'All']]

# Swap the "Stanford student" and "Other" columns
pivot_table_percent = pivot_table.div(pivot_table.iloc[:, -1], axis=0) * 100

### Formatting ###

plt.figure(figsize=(12, 6))
sns.set(font_scale=1.2)

# Set a good font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Bahnschrift', 'Arial',
                                   'Calibri', 'DejaVu Sans', 'Liberation Sans', 'Tahoma', 'Verdana']

### Counts ###

# Save the table as a text file
with open('table_counts.txt', 'w') as f:
    f.write(pivot_table.to_string())

# Create a heatmap using seaborn
# Get the second highest value in the table (so not the All/All) to be the vmax
values = pivot_table.values
vmax = values[values != values.max()].max()
heatmap = sns.heatmap(pivot_table, annot=True, cmap='viridis', vmax=vmax, fmt="d", cbar=False)
heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=0)

# Label the heatmap
plt.xlabel('How good to have invited them? (How much did they improve the retreat/how valuable was it)')
plt.ylabel('School')
plt.title('IBAR Attendee Worth It (Counts)', fontweight='bold', fontsize=16)

# Save the heatmap as an image
plt.savefig('heatmap_counts.png', dpi=300, bbox_inches='tight')

# Clear the plot
plt.clf()

### Percentages ###

# Remove the "All" column because it's all 100%
pivot_table_percent = pivot_table_percent.drop('All', axis=1)

# Save the table as a text file
with open('table_percentages.txt', 'w') as f:
    f.write(pivot_table_percent.to_string())

# Create a heatmap using seaborn (label with % sign)
heatmap = sns.heatmap(pivot_table_percent, annot=True, cmap='viridis', fmt=".1f", cbar=False)
# Add percentage signs
for t in heatmap.texts:
    t.set_text(t.get_text() + '%')

# Label the heatmap
plt.xlabel('How good to have invited them? (How much did they improve the retreat/how valuable was it)')
plt.ylabel('School')
plt.title('IBAR Attendee Worth It (Percentages by Row)', fontweight='bold', fontsize=16)

# Save the heatmap as an image
plt.savefig('heatmap_percentages.png', dpi=300, bbox_inches='tight')
