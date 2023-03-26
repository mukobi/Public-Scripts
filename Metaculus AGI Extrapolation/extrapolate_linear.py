"""
Loads Metaculus predictions for "When will (Strong) AGI be achieved?" and
extrapolates out to estimate what they'll update down to.
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

# dates = [
#     ('2020-10-01', '2064-06-06'),
#     ('2020-11-01', '2051-01-25'),
#     ('2020-12-01', '2047-12-05'),
#     ('2021-01-01', '2044-09-27'),
#     ('2021-02-01', '2048-09-30'),
#     ('2021-03-01', '2048-05-12'),
#     ('2021-04-01', '2047-06-12'),
#     ('2021-05-01', '2049-10-06'),
#     ('2021-06-01', '2047-08-18'),
#     ('2021-07-01', '2052-05-15'),
#     ('2021-08-01', '2056-06-14'),
#     ('2021-09-01', '2055-01-11'),
#     ('2021-10-01', '2054-04-13'),
#     ('2021-11-01', '2053-08-16'),
#     ('2021-12-01', '2053-05-13'),
#     ('2022-01-01', '2052-02-28'),
#     ('2022-02-01', '2059-04-14'),
#     ('2022-03-01', '2055-12-03'),
#     ('2022-04-01', '2054-05-03'),
#     ('2022-05-01', '2045-11-09'),
#     ('2022-06-01', '2040-04-18'),
#     ('2022-07-01', '2036-12-12'),
#     ('2022-08-01', '2040-03-17'),
#     ('2022-09-01', '2041-11-18'),
#     ('2022-10-01', '2041-10-21'),
#     ('2022-11-01', '2040-05-05'),
#     ('2022-12-01', '2039-06-13'),
#     ('2023-01-01', '2037-10-26'),
#     ('2023-02-01', '2040-05-15'),
#     ('2023-03-01', '2039-11-16'),
#     ('2023-04-01', '2033-04-08'),
# ]


# df = pd.DataFrame(dates)
# df.columns = ['current_date', 'agi_predicted_date']
# df['current_date'] = pd.to_datetime(df['current_date'])
# df['days_since_first_date'] = (df['current_date'] - df['current_date'].min()).dt.days
# df['years_since_first_date'] = df['days_since_first_date'] / 365 + (2020 + 10. / 12)
# df['agi_predicted_date'] = pd.to_datetime(df['agi_predicted_date'])
# df['date_to_agi'] = df['agi_predicted_date'] - df['current_date']
# df['days_to_agi'] = df['date_to_agi'].dt.days
# df['years_to_agi'] = df['days_to_agi'] / 365
# # Get year as a decimal
# df['years_of_agi'] = df['agi_predicted_date'].dt.year + df['agi_predicted_date'].dt.dayofyear / 365

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
# Add a y=x graph (dashed)
plt.plot([left_bound, right_bound], [left_bound, right_bound], color='crimson', linestyle='--')

# Calculate the slope of the regression
regression_line = g.get_lines()[0]
slope = (regression_line.get_ydata()[99] - regression_line.get_ydata()[0]) / \
    (regression_line.get_xdata()[99] - regression_line.get_xdata()[0])

# Find the point where the x-value is the same as the y-value (actually the closest)
closest_point = (0, 0)
closest_distance = 1e9
for x, y in zip(regression_line.get_xdata(), regression_line.get_ydata()):
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
# Add a legend
plt.legend(['Metaculus Predictions', f'Regression (m = {slope:.2})', 'Error', 'y=x (Actual Year = Prediction)'])

# plt.ylim(bottom=0, top=50)
g.tick_params('x', rotation=30)
plt.xlabel('Prediction Dates')
plt.ylabel('Predicted Date of AGI')
plt.title('Metaculus Date of Strong AGI Extrapolation')

# Format the graph big and pretty
plt.gcf().set_size_inches(8, 6)
plt.tight_layout()


plt.savefig('metaculus_strong_agi_extrapolation.png')
# plt.show()

print('Finished!')
