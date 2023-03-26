"""
Loads Metaculus predictions for "When will (Strong) AGI be achieved?" and
extrapolates out to estimate what they'll update down to.

https://www.metaculus.com/questions/5121/date-of-artificial-general-intelligence/

Code originally by Rylan Schaeffer.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import datetime

df = pd.read_json('./predictions.json')
# Convert string times to datetime
df['date_of_prediction'] = pd.to_datetime(df['date_of_prediction'])
# Normalize timezone
df['date_of_prediction'] = df['date_of_prediction'].dt.tz_localize(None)
# Create a new column with the year as a decimal (row.time.year + row.time.dayofyear / 365)
df['date_of_prediction'] = df['date_of_prediction'].dt.year + df['date_of_prediction'].dt.dayofyear / 365

left_bound = 2020.6
right_bound = 2027

plt.xlim(left=left_bound, right=right_bound)
g = sns.regplot(
    data=df,
    x='date_of_prediction',
    y='agi_prediction',
    truncate=False,
    color='royalblue',
)

# Now, let's just try a regression using the data after 2022 (when the slope suddenly changes)
split_point = 2022
df2 = df[df['date_of_prediction'] > split_point]
g2 = sns.regplot(
    data=df2,
    x='date_of_prediction',
    y='agi_prediction',
    truncate=False,
    color='green',
)

# Calculate the slope of the regressions
regression_line1 = g.get_lines()[0]
slope1 = (regression_line1.get_ydata()[99] - regression_line1.get_ydata()[0]) / \
    (regression_line1.get_xdata()[99] - regression_line1.get_xdata()[0])

regression_line2 = g2.get_lines()[1]
slope2 = (regression_line2.get_ydata()[99] - regression_line2.get_ydata()[0]) / \
    (regression_line2.get_xdata()[99] - regression_line2.get_xdata()[0])
print(slope1)
print(slope2)


# Add a y=x graph (dashed)
plt.plot([left_bound, right_bound], [left_bound, right_bound], color='crimson', linestyle='--')

# Find the point where the x-value is the same as the y-value (actually the closest)
closest_point = (0, 0)
closest_distance = 1e9
for x, y in zip(regression_line1.get_xdata(), regression_line1.get_ydata()):
    distance = abs(x - y)
    if distance < closest_distance:
        closest_point = (x, y)
        closest_distance = distance
plt.plot(closest_point[0], closest_point[1], 'ro', markersize=10)

# Convert the point to a date (e.g. 2020.5 -> 2020 June 1)
days = 365 * (closest_point[0] - int(closest_point[0]))
closest_point_date = datetime.datetime(int(closest_point[0]), 1, 1) + datetime.timedelta(days=days)

# Add a label to the intersection point
plt.text(closest_point[0], closest_point[1]+2,
         f'AGI: {closest_point[0]:.2f}\n({closest_point_date.strftime("%Y %b %d")})')


# Do the above for the second line
closest_point2 = (0, 0)
closest_distance2 = 1e9
for x, y in zip(regression_line2.get_xdata(), regression_line2.get_ydata()):
    distance = abs(x - y)
    if distance < closest_distance2:
        closest_point2 = (x, y)
        closest_distance2 = distance
plt.plot(closest_point2[0], closest_point2[1], 'ro', markersize=10)

# Convert the point to a date (e.g. 2020.5 -> 2020 June 1)
days = 365 * (closest_point2[0] - int(closest_point2[0]))
closest_point_date2 = datetime.datetime(int(closest_point2[0]), 1, 1) + datetime.timedelta(days=days)

# Add a label to the intersection point
plt.text(closest_point2[0], closest_point2[1]+2,
         f'AGI: {closest_point2[0]:.2f}\n({closest_point_date2.strftime("%Y %b %d")})')


# Add a legend
plt.legend([
    'Metaculus Predictions Full',
    f'Regression Full (m = {slope1:.2})',
    'Error Full',
    'Metaculus Predictions Post-2022',
    f'Regression Post-2022 (m = {slope2:.2f})',
    'Error Post-2022',
    'y=x (Predicted Year = Actual Year)',
    'AGI extrapolations (when the\nMetaculus prediction = the actual\nyear at the observed update rate))',
])

plt.ylim(bottom=2020, top=2070)
g.tick_params('x', rotation=30)
plt.xlabel('Prediction Dates')
plt.ylabel('Predicted Date of AGI')
plt.title('Metaculus Date of Strong AGI Extrapolation (Linear)')

# Format the graph big and pretty
plt.gcf().set_size_inches(8, 6)
plt.tight_layout()

plt.savefig('metaculus_strong_agi_extrapolation_linear.png')
# plt.show()

print('Finished!')
