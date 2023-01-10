"""Propose discussion sections for SAIA Class Scheduling using a CSP solver."""

import csv
from typing import Dict, List, Tuple

from matplotlib import pyplot as plt

import constraint

# Constants
INPUT_FILE = './SAIA Class Scheduling-STS 20SI All.csv'
MIN_GROUP_SIZE = 4

# Read in data
students = []
facilitators = []
with open(INPUT_FILE, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Full Name']
        role = row['Are you a student or a facilitator?']
        availability = set(row['Which of these 80-minute class times can you make weekly?'].split(','))
        if role == 'Student':
            students.append((name, availability))
        elif role == 'Facilitator':
            facilitators.append((name, availability))
        else:
            raise ValueError(role)

student_names = [name for name, _ in students]
facilitator_names = [name for name, _ in facilitators]

# Create CSP
problem = constraint.Problem()

# Add variables: each faciltator chooses a time
for facilitator in facilitators:
    name, availability = facilitator
    problem.addVariable(name, list(availability))

# Add variables: each student chooses a facilitator
for student in students:
    name, availability = student
    problem.addVariable(name, facilitator_names)

# Add constraint: For each student, they must be available at the time
# that their facilitator has chosen.
for student in students:
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

# Solve CSP
solutions = problem.getSolutions()
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

# Plot a histogram of the times that most often occured
# in the solutions. Shows the graphs at the same time.
fig, ax = plt.subplots(nrows=len(facilitator_solution_times), ncols=1, sharey=True, sharex=True)
for i, (facilitator_name, times) in enumerate(facilitator_solution_times):
    ax[i].hist(times)
    ax[i].set_title(f'{facilitator_name}')
    ax[i].set_xlabel('Time')
    ax[i].set_ylabel('Count')

# adjust the spacing between subplots
fig.subplots_adjust(hspace=0.5)

fig.suptitle('Facilitator Times')
fig.align_xlabels()
plt.show()
