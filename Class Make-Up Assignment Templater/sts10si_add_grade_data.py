import csv

# Config
INPUT_FILE = 'sts10si_attendance_input.csv'
OUTPUT_FILE_FINISHED = 'sts10si_attendance_output_finished.csv'
OUTPUT_FILE_MAKEUP = 'sts10si_attendance_output_makeup.csv'
REQUIRED_ATTENDANCE = 7
REQUIRED_REFLECTIONS = 6
WORDS_PER_MISSING_THING = 100

# Open the CSV file
with open(INPUT_FILE, 'r') as file:
    # Read the CSV data into a list of dictionaries
    reader = csv.DictReader(file)
    input_data = list(reader)

# Calculate the stuff for each student
output_data_finished = []
output_data_makeup = []
for input_row in input_data:
    if input_row['Name'] == '' or input_row['Enrolled'] != 'TRUE' or 'Dropped' in input_row.values():
        continue
    output_row = {}
    # Contact
    output_row['email'] = input_row['Email'].strip()
    output_row['full_name'] = input_row['Name'].strip()
    output_row['first_name'] = input_row['Name'].split(' ')[0]

    # Existing grades
    attendance_completed = int(input_row['Attendance'].strip())
    reflections_completed = int(input_row['Reflections'].strip())
    output_row['attendance_completed'] = attendance_completed
    output_row['reflections_completed'] = reflections_completed

    # Missing grades
    attendance_missing = REQUIRED_ATTENDANCE - attendance_completed
    reflections_missing = REQUIRED_REFLECTIONS - reflections_completed

    total_missing = attendance_missing + reflections_missing
    words_to_write = WORDS_PER_MISSING_THING * total_missing

    if words_to_write <= 0:
        output_data_finished.append(output_row)
    else:
        # Make-up stuff
        output_row['attendance_missing'] = attendance_missing
        output_row['reflections_missing'] = reflections_missing

        output_row['total_missing'] = total_missing
        output_row['words_to_write'] = words_to_write

        output_data_makeup.append(output_row)

# Write output
for output_file, output_data in [(OUTPUT_FILE_FINISHED, output_data_finished), (OUTPUT_FILE_MAKEUP, output_data_makeup)]:
    with open(output_file, 'w', newline='\n') as file:
        # Write the CSV data
        writer = csv.DictWriter(file, fieldnames=output_data[0].keys())
        writer.writeheader()
        writer.writerows(output_data)
