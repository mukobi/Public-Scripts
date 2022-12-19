import csv

# File selection
INPUT_FILE = input('Enter the path of a CSV file...\n')

# Open the CSV file
with open(INPUT_FILE, 'r') as file:
    # Read the CSV data into a list of dictionaries
    reader = csv.DictReader(file)
    input_data = list(reader)

# Calculate the stuff for each student
for input_row in input_data:
    for possible_name_key in ['Name', 'name', 'Full Name', 'full name', 'fullname', 'FullName']:
        try:
            full_name = input_row[possible_name_key]
            if full_name != '':
                input_row['first_name'] = full_name.split(' ')[0].strip()
        except KeyError:
            continue


# Write output
with open(INPUT_FILE, 'w', newline='\n') as file:
    # Write the CSV data
    writer = csv.DictWriter(file, fieldnames=input_data[0].keys())
    writer.writeheader()
    writer.writerows(input_data)
