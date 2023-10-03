"""
For discussion group scheduling for Stanford AI Alignment classes.
Given we've chosen some discussion section times for our facilitators,
iterate over each student and print which facilitator groups they can make.
"""

import os
import csv

SORT_BY_AVAILABILITY_INSTEAD_OF_NAME = False

# Find whatever CSV file is in the local folder using list comprehension
# INPUT_FILE = [f for f in os.listdir(".") if f.endswith(".csv")][0]
INPUT_FILE = [f for f in os.listdir(".") if f.endswith(".csv")]
if len(INPUT_FILE) == 1:
    INPUT_FILE = INPUT_FILE[0]
elif len(INPUT_FILE) == 0:
    INPUT_FILE = input("Enter the path of the CSV file: ").strip().strip('"').strip("'")
else:
    raise ValueError(f"Multiple input files found:\n{INPUT_FILE}")


# Lock in the facilitator times
facilitator_times_and_group_names = {
    ("Peter Gebauer 1", "Tu 4:30-5:50 PM", "Red"),
    ("Gabriel Mukobi 1", "W 1:30-2:50 PM", "Yellow"),
    ("Scott Viteri 1", "Th 1:30-2:50 PM", "Green"),
    ("Peter Gebauer 2", "F 3:00-4:20 PM", "Blue"),
}
# Print the names of each section
print("Facilitator times:")
for facilitator, time, group_name in facilitator_times_and_group_names:
    print(f"{group_name}: {time} ({' '.join(facilitator.split()[:-1])})")
print()

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
            num_groups = int(row["Chosen num sections"])
            for i in range(num_groups):
                facilitators.append((f"{name} {i+1}", availability))
        else:
            raise ValueError(role)

# Get each student and their available groups (facilitator and time)
student_possible_groups = []
for student_name, student_availability in students:
    valid_groups = []
    for facilitator, time, group_name in facilitator_times_and_group_names:
        if time in student_availability:
            valid_groups.append(group_name)
    student_possible_groups.append((student_name, valid_groups))

if SORT_BY_AVAILABILITY_INSTEAD_OF_NAME:
    # Sort the students by the number of available groups, least to most
    student_possible_groups.sort(key=lambda x: len(x[1]))
else:
    # Sort the students by name
    student_possible_groups.sort(key=lambda x: x[0])

# Print out the avaiabilities
for student_name, student_availability in student_possible_groups:
    print(f'{student_name}: {", ".join(student_availability)}')
