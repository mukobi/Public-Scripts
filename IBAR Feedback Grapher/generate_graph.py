"""Load the final feedback form data, find every column with numeric data, and plot bar plots showing the distribution of each column's data along with the question that column was asking all together on one big plot."""

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data

# INPUT_FILE = input('Enter the path of a CSV file...\n')
INPUT_FILE = "C:/Users/Gabe/Downloads/Final Feedback Form-Everyone.csv"

# Format filename to avoid invalid arguments (e.g. \\ on Windows, remove quotes)

INPUT_FILE = INPUT_FILE.replace('\\', '/').replace('"', '').replace("'", '')

df = pd.read_csv(INPUT_FILE)

# Remove the "Last 4 digits of your phone number" column
df = df.drop(columns=['Last 4 digits of your phone number'])

# Find all ratings columns
ratings_columns = df.select_dtypes(include=['int64']).columns

# Make separate graphs for the 0-5 and the 0-10 metrics
for max_rating in [5, 10]:
    # Filter out the columns that don't have a max rating of max_rating
    ratings_columns = df.select_dtypes(include=['int64']).columns
    ratings_columns = [column for column in ratings_columns if df[column].max() == max_rating]

    # Number of total columns
    num_columns = len(ratings_columns)

    # Clear the plot
    plt.clf()

    # Create a new figure to stack all the plots on top of each other with a shared x-axis
    fig, axes = plt.subplots(num_columns, 1, figsize=(10, 1.2 * num_columns))

    # Plot each of the histograms by calculating them manually
    bins = range(1, max_rating + 1)
    means = []
    stdevs = []
    quartile_1s = []
    medians = []
    quartile_3s = []
    for i, column in enumerate(ratings_columns):
        # Different hue for each column
        color = f'C{i}'
        counts = df[column].value_counts().sort_index()
        counts = counts.reindex(bins, fill_value=0)
        axes[i].bar(bins, counts, width=0.9, align='center', label=column, color=color)
        axes[i].set_title(df[column].name, fontsize=12, y=0.7)
        axes[i].set_xticks(bins)

        # Add labels
        for x, y in zip(bins, counts):
            if y == 0:
                continue
            if y < 3:
                align = 'bottom'
                y_position = y + 0.025 * max(counts)
            else:
                align = 'top'
                y_position = y - 0.025 * max(counts)
            label = f'{y} / {len(df[column])} = {y / len(df[column]):.1%}'
            axes[i].text(x, y_position, label, ha='center', va=align, fontsize=8)

        # Calculate statistics
        mean = df[column].mean()
        stdev = df[column].std()
        quartile_1 = df[column].quantile(0.25)
        median = df[column].median()
        quartile_3 = df[column].quantile(0.75)
        means.append(mean)
        stdevs.append(stdev)
        quartile_1s.append(quartile_1)
        medians.append(median)
        quartile_3s.append(quartile_3)

    # Remove vertical space between each plot
    plt.subplots_adjust(hspace=-4)

    # Add a bit of bottom margin for the bottom labels

    # Add a supertitle
    fig.suptitle(f'IBAR 2023 Feedback (1-{max_rating} Questions)', fontsize=16)

    # Set tight bounds
    plt.tight_layout()

    # Set a good font
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = [
        'Bahnschrift', 'Arial',
        'Calibri', 'DejaVu Sans', 'Liberation Sans', 'Tahoma', 'Verdana']

    # Set the x-axis to go from 0 to 10
    # plt.xlim(0, 10)

    # Format the plot so it all shows up
    plt.savefig(f'feedback_0-{max_rating}.png', dpi=300, bbox_inches='tight')

    # Print info about the statistics
    print(f'0-{max_rating} statistics:')
    for i, column in enumerate(ratings_columns):
        print(f'- _{column}_')
        print(f'  - Mean (±Stdev): **{means[i]:.2f}** (±{stdevs[i]:.2f})')
        print(f'  - Quartiles: {quartile_1s[i]:.2f}, **{medians[i]:.2f}**, {quartile_3s[i]:.2f}')

    print('\n\n####################\n\n')
