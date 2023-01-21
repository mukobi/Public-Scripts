"""
For discussion group scheduling for Stanford AI Alignment classes.
Given we've chosen some discussion section times for our facilitators,
iterate over each student and print which facilitator groups they can make.
"""

import os
import csv

# Find whatever CSV file is in the local folder using list comprehension 
INPUT_FILE = [f for f in os.listdir('.') if f.endswith('.csv')][0]

# Set facilitator times
facilitator_locked_in_times = {
    'Aaron Scher 1': 'W 3:00-4:20 PM',
    'Gabe Mukobi': 'M 4:30-5:50 PM',
}

# Read in data
students = []
facilitators = []
with open(INPUT_FILE, 'r') as f:
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

# Print out each student and their available groups (facilitator and time)
for student_name, student_availability in students:
    valid_groups = []
    for facilitator, time in facilitator_locked_in_times.items():
        if time in student_availability:
            valid_groups.append(f'{facilitator} ({time})')
    print(f'{student_name}: {", ".join(valid_groups)}')
