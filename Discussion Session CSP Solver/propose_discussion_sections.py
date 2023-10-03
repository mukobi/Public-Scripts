"""
Propose discussion sections for SAIA Class Scheduling using a CSP solver.
The idea is that we find all the solutions and plot which times had the most solutions.
Then, if you choose those times for the sections, you have more choice in the students.
Rather idiosyncratic to SAIA's class scheduling form: https://airtable.com/shrl6KTTzPVNyLzmi
"""

import colorsys
import os
import csv
import functools
from datetime import datetime

from matplotlib import pyplot as plt

import constraint

from tqdm import tqdm

# Parameters
# Groups with fewer than this number of students are invalid.
MIN_GROUP_SIZE = 3
# Filter the students to remove students with too much or too little availability to make the problem easier.
MAX_STUDENT_AVAILABILITY = 12
MIN_STUDENT_AVAILABILITY = 5

# How often we expect a solution to be found, based on the number of solutions found so far. Only used for printing progress.
EST_SOLUTION_DENSITY = 8364 / 22617340087890625000

PRINT_SOLUTIONS = False


# Find whatever CSV file is in the local folder using list comprehension
INPUT_FILE = [f for f in os.listdir(".") if f.endswith(".csv")]
if len(INPUT_FILE) == 1:
    INPUT_FILE = INPUT_FILE[0]
elif len(INPUT_FILE) == 0:
    INPUT_FILE = input("Enter the path of the CSV file: ").strip().strip('"').strip("'")
else:
    raise ValueError(f"Multiple input files found:\n{INPUT_FILE}")

# Read in data
students = []
facilitators = []
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["Full Name"]
        role = row["Are you a student or a facilitator?"]
        availability = set(row["Availability"].split(","))
        if role == "Student":
            students.append((name, availability))
        elif role == "Facilitator":
            # Duplicate the facilitator for each number of groups they can facilitate
            try:
                num_groups = int(row["Chosen num sections"])
            except ValueError as exc:
                raise ValueError(
                    f'Invalid number of groups for {name} (please enter manually): {row["Chosen num sections"]}'
                ) from exc
            for i in range(num_groups):
                facilitators.append((f"{name} {i+1}", availability))
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
print(f'Facilitators: {", ".join(facilitator_names)}')

# Add variables: each student chooses a facilitator
num_students_removed_too_much = 0
num_students_removed_too_little = 0
filtered_students = []
for student in students:
    name, availability = student
    # Filter the students to remove students with too much or little availability to make the problem easier
    if len(availability) > MAX_STUDENT_AVAILABILITY:
        num_students_removed_too_much += 1
        continue
    if len(availability) < MIN_STUDENT_AVAILABILITY:
        num_students_removed_too_little += 1
        continue
    possible_configurations *= len(facilitator_names)
    problem.addVariable(name, facilitator_names)
    filtered_students.append(student)

student_names = [name for name, _ in filtered_students]

print(
    f"Removed {num_students_removed_too_much}/{len(students)} students with more than {MAX_STUDENT_AVAILABILITY} availabilities."
)
print(
    f"Removed {num_students_removed_too_little}/{len(students)} students with fewer than {MIN_STUDENT_AVAILABILITY} availabilities."
)

print(f"Total possible configurations: {possible_configurations}")

# Add constraint: For each student, they must be available at the time
# that their facilitator has chosen.
for student in filtered_students:
    student_name, student_availability = student

    def build_availability_constraint(student_availability):
        def constraint_func(chosen_facilitator, *facilitator_times):
            facilitator_time = facilitator_times[
                facilitator_names.index(chosen_facilitator)
            ]
            return facilitator_time in student_availability

        return constraint_func

    problem.addConstraint(
        build_availability_constraint(student_availability),
        (student_name, *facilitator_names),
    )

# Add constraint: For each facilitator, they must have at least MIN_GROUP_SIZE students.
# Implemented as for each facilitator, the number of students choosing them is at least MIN_GROUP_SIZE.
for facilitator_name in facilitator_names:

    def build_size_constraint_func(facilitator_name):
        def constraint_func(*facilitator_choices):
            students_in_this_group = len(
                [choice for choice in facilitator_choices if choice == facilitator_name]
            )
            return students_in_this_group >= MIN_GROUP_SIZE

        return constraint_func

    problem.addConstraint(build_size_constraint_func(facilitator_name), student_names)

# Solve CSP, showing a count of the number of solutions iteratively
solutions = []
est_num_solutions = EST_SOLUTION_DENSITY * possible_configurations
for solution in tqdm(problem.getSolutionIter(), total=est_num_solutions):
    solutions.append(solution)
    # print(f'Found {len(solutions)} solutions! Progress: {len(solutions) / est_num_solutions * 100:.2f}%', end='\r')

print(f"Found {len(solutions)} solutions!")

if len(solutions) == 0:
    print("No solutions found :(")
    exit()

if PRINT_SOLUTIONS:
    # Print solutions
    for i, solution in enumerate(solutions):
        print(f"Solution {i + 1}:")
        for student, time in solution.items():
            print(f"{student}: {time}")
        print()
        if i + 1 >= 2:
            break

    print("No more solutions found.")

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
        print(f"{facilitator_name} - {time}: {count}")

# Extract unique times from all facilitators' times lists
unique_times = set()
for facilitator, times in facilitator_solution_times:
    for time in times:
        unique_times.add(time)
unique_times = list(unique_times)

# A custom comparison function. Expects times formatted like 'M 3:00-4:20 PM'


def compare_times(t1, t2):
    # Extract day, starting time, and AM/PM from the time string
    day1, time1, ampm1 = t1.split()
    day2, time2, ampm2 = t2.split()
    start_time1, _ = time1.split("-")
    start_time2, _ = time2.split("-")
    # Converting times in 24 hours format
    start_time1 = datetime.strptime(start_time1 + ampm1, "%I:%M%p").strftime("%H:%M")
    start_time2 = datetime.strptime(start_time2 + ampm2, "%I:%M%p").strftime("%H:%M")
    # Creating dict of days and their numerical value
    days = {"M": 1, "Tu": 2, "W": 3, "Th": 4, "F": 5, "Sa": 6, "Su": 7}
    if days[day1] != days[day2]:
        return days[day1] - days[day2]
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
plt.rcParams.update({"font.size": 7, "figure.figsize": (10, 10)})

# Plot histograms for each facilitator
fig, ax = plt.subplots(
    nrows=len(facilitator_solution_times), ncols=1, sharey=True, sharex=True
)
for i, (facilitator_name, times) in enumerate(facilitator_solution_times):
    # Count occurrences of each time in facilitator's times list
    time_counts = {time: times.count(time) for time in unique_times}

    # Plot a bar for each time
    ax[i].bar(
        list(time_counts.keys()),
        list(time_counts.values()),
        label=facilitator_name,
        width=0.95,
        align="center",
        edgecolor="black",
        linewidth=0.5,
        color="#444",
    )
    # Color this plot with a hue based on i
    ax[i].set_facecolor(
        colorsys.hsv_to_rgb(i / len(facilitator_solution_times), 0.28, 0.93)
    )
    ax[i].set_ylabel("Count")
    ax[i].legend()
    ax[i].grid()


# Make sure there is an x-label for every bin
fig.align_xlabels()
plt.xticks(unique_times, rotation=15, horizontalalignment="right")

# Get rid of the space between the title and the first subplot
fig.subplots_adjust(top=0.95)

fig.suptitle("Facilitator Times - Number of CSP Solutions")

# Save the plot to a file, but big and zoomed out so it's readable.
fig.savefig("facilitator_times.png", dpi=300, bbox_inches="tight", pad_inches=0.05)

plt.show()
