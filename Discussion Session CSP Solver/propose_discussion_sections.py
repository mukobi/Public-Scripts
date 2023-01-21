"""Propose discussion sections for SAIA Class Scheduling using a CSP solver."""

import os
import csv
import functools
from datetime import datetime
from typing import Dict, List, Tuple

from matplotlib import pyplot as plt

import constraint

from tqdm import tqdm

# Constants
# Groups with fewer than this number of students are invalid.
MIN_GROUP_SIZE = 2
# Filter the students to remove students with too much availability to make the problem easier.
MAX_STUDENT_AVAILABILITY = 6  
# How often we expect a solution to be found, based on the number of solutions found so far. Only used for printing progress.
EST_SOLUTION_DENSITY = 8364 / 22617340087890625000  


# Find whatever CSV file is in the local folder using list comprehension 
INPUT_FILE = [f for f in os.listdir('.') if f.endswith('.csv')][0]

# Read in data
students = []
facilitators = []
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Full Name']
        role = row['Are you a student or a facilitator?']
        availability = set(row['Availability'].split(','))
        if role == 'Student':
            students.append((name, availability))
        elif role == 'Facilitator':
            # Duplicate the facilitator for each number of groups they can facilitate
            num_groups = int(row['Chosen num sections'])
            for i in range(num_groups):
                facilitators.append((f'{name} {i+1}', availability))
        else:
            raise ValueError(role)

# Create CSP
problem = constraint.Problem(constraint.BacktrackingSolver())

# Count the number of variable configurations to estimate progress
possible_configurations = 1

# Add variables: each faciltator chooses a time
for facilitator in facilitators:
    name, availability = facilitator
    availability = list(availability)
    problem.addVariable(name, availability)
    possible_configurations *= len(availability)

facilitator_names = [name for name, _ in facilitators]
print(facilitator_names)

# Add variables: each student chooses a facilitator
num_students_removed = 0
filtered_students = []
for student in students:
    name, availability = student
    # Filter the students to remove students with too much availability to make the problem easier
    if len(availability) > MAX_STUDENT_AVAILABILITY:
        num_students_removed += 1
        continue
    possible_configurations *= len(facilitator_names)
    problem.addVariable(name, facilitator_names)
    filtered_students.append(student)

student_names = [name for name, _ in filtered_students]

print(f'Removed {num_students_removed}/{len(students)} students with more than {MAX_STUDENT_AVAILABILITY} availabilities.')

print(f'Total possible configurations: {possible_configurations}')

# Add constraint: For each student, they must be available at the time
# that their facilitator has chosen.
for student in filtered_students:
    student_name, student_availability = student

    def build_availability_constraint(student_availability):
        def constraint_func(chosen_facilitator, *facilitator_times):
            facilitator_time = facilitator_times[facilitator_names.index(chosen_facilitator)]
            return facilitator_time in student_availability
        return constraint_func
    problem.addConstraint(build_availability_constraint(student_availability),
                          (student_name, *facilitator_names))

# Add constraint: For each facilitator, they must have at least MIN_GROUP_SIZE students.
# Implemented as for each facilitator, the number of students choosing them is at least MIN_GROUP_SIZE.
for facilitator_name in facilitator_names:
    def build_size_constraint_func(facilitator_name):
        def constraint_func(*facilitator_choices):
            students_in_this_group = len([choice for choice in facilitator_choices if choice == facilitator_name])
            return students_in_this_group >= MIN_GROUP_SIZE
        return constraint_func

    problem.addConstraint(build_size_constraint_func(facilitator_name), student_names)

# Solve CSP, showing a count of the number of solutions iteratively
solutions = []
est_num_solutions = EST_SOLUTION_DENSITY * possible_configurations
for solution in tqdm(problem.getSolutionIter(), total=est_num_solutions):
    solutions.append(solution)
    # print(f'Found {len(solutions)} solutions! Progress: {len(solutions) / est_num_solutions * 100:.2f}%', end='\r')

print(f'Found {len(solutions)} solutions!')

# Print solutions
for i, solution in enumerate(solutions):
    print(f'Solution {i + 1}:')
    for student, time in solution.items():
        print(f'{student}: {time}')
    print()
    if i + 1 >= 2:
        break

print('No more solutions found.')

# For each facilitator, get the times from all the solutions.
facilitator_solution_times = []
for facilitator_name in facilitator_names:
    times = [solution[facilitator_name] for solution in solutions]
    facilitator_solution_times.append((facilitator_name, times))

    # Print the sum of each time
    time_counts = {}
    for time in times:
        if time not in time_counts:
            time_counts[time] = 0
        time_counts[time] += 1
    for time, count in time_counts.items():
        print(f'{facilitator_name} - {time}: {count}')

# Extract unique times from all facilitators' times lists
unique_times = set()
for facilitator, times in facilitator_solution_times:
    for time in times:
        unique_times.add(time)

# A custom comparison function. Expects times formatted like 'M 3:00-4:20 PM'
def compare_times(t1, t2):
    # Extract day, starting time, and AM/PM from the time string
    day1, time1, ampm1 = t1.split()
    day2, time2, ampm2 = t2.split()
    start_time1, _ = time1.split("-")
    start_time2, _ = time2.split("-")
    #Converting times in 24 hours format
    start_time1 = datetime.strptime(start_time1+ampm1,"%I:%M%p").strftime("%H:%M")
    start_time2 = datetime.strptime(start_time2+ampm2,"%I:%M%p").strftime("%H:%M")
    # Creating dict of days and their numerical value
    days = {'M':1, 'Tu':2, 'W':3, 'Th':4, 'F':5, 'Sa':6, 'Su':7}
    if days[day1] != days[day2]:
        return days[day1]-days[day2]
    else:
        if start_time1 != start_time2:
            return -1 if start_time1 < start_time2 else 1
        else:
            return 0

# Convert times to datetime objects and sort by date and time.
unique_times = sorted(unique_times, key=functools.cmp_to_key(compare_times))

# Plot a histogram of the times that most often occured
# in the solutions. Shows the graphs at the same time.
# Reduce the font of everything
plt.rcParams.update({'font.size': 6})

# Plot histograms for each facilitator
fig, ax = plt.subplots(nrows=len(facilitator_solution_times), ncols=1, sharey=True, sharex=True)
for i, (facilitator_name, times) in enumerate(facilitator_solution_times):
    # Count occurrences of each time in facilitator's times list
    time_counts = {time: times.count(time) for time in unique_times}

    # Plot histogram
    ax[i].hist(list(time_counts.keys()), weights=list(time_counts.values()), label=facilitator_name)
    ax[i].set_title(facilitator_name)
    ax[i].set_ylabel('Count')
    ax[i].set_xlabel('Time')
    ax[i].legend()

# adjust the spacing between subplots
fig.subplots_adjust(hspace=1.0)

fig.suptitle('Facilitator Times')
fig.align_xlabels()

# Make sure there is an x-label for every bin
plt.xticks(list(unique_times), rotation=15, horizontalalignment='right')

# Add margins to the bottom to show the labels
plt.subplots_adjust(bottom=0.2)

# Save the plot to a file, but big so it all shows up
fig.savefig('facilitator_times.png', dpi=720)

plt.show()