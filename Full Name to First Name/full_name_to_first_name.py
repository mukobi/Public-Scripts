import csv

# Config
INPUT_FILE = './research_symposium_reminder.csv'
OUTPUT_FILE = f'{INPUT_FILE[:-4]}_with_first_name.csv'


# Open the CSV file
with open(INPUT_FILE, 'r') as file:
    # Read the CSV data into a list of dictionaries
    reader = csv.DictReader(file)
    input_data = list(reader)

# Calculate the stuff for each student
for input_row in input_data:
    if input_row['Name'] == '':
        continue
    input_row['first_name'] = input_row['Name'].split(' ')[0].strip()


# Write output
with open(OUTPUT_FILE, 'w', newline='\n') as file:
    # Write the CSV data
    writer = csv.DictWriter(file, fieldnames=input_data[0].keys())
    writer.writeheader()
    writer.writerows(input_data)
