"""
For discussion group scheduling for Stanford AI Alignment classes.
Given we've chosen some discussion section times for our facilitators,
iterate over each student and print which facilitator groups they can make.
"""

import os
import csv

# Find whatever CSV file is in the local folder using list comprehension
INPUT_FILE = [f for f in os.listdir('.') if f.endswith('.csv')][0]
SORT_BY_AVAILABILITY_INSTEAD_OF_NAME = False

# Lock in the facilitator times
facilitator_times_and_group_names = {
    ('Aaron Scher 1', 'Tu 4:30-5:50 PM', 'Yellow'),
    ('Gabe Mukobi 1', 'Tu 3:00-4:20 PM', 'Red'),
    ('Michael Byun', 'W 3:00-4:20 PM', 'Green'),
    ('Aaron Scher 2', 'F 4:30-5:50 PM', 'Purple'),
    ('Gabe Mukobi 2', 'Th 10:30-11:50 AM', 'Blue'),
}

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
