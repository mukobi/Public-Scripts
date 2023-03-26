"""
For all the Stanford classes in the "Class" column of a CSV file, get the
class title if it doesn't exist, get the quartes that the class is offered,
and write them to the same CSV file for easier course scheduling.

Overly specific to my format at https://docs.google.com/spreadsheets/d/1xBFkjG0QsqiVO62wHE0PvM8uVODwG9SBvLIYkvkiPjo/edit
"""

import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Ignore reportOptionalMemberAccess in Pylance
# (https://stackoverflow.com/questions/4998629/syntaxerror-non-keyword-arg-after-keyword-arg)

# File selection
INPUT_FILE = input('Enter the path of a CSV file...\n')
# INPUT_FILE = './Classes I Want To Take - Gabe Mukobi - Classes.csv'

# Format filename to avoid invalid arguments (e.g. \\ on Windows, remove quotes)
INPUT_FILE = INPUT_FILE.replace('\\', '/').replace('"', '').replace("'", '')

# Load in CSV data
input_data = []
with open(INPUT_FILE, 'r', encoding='utf-8') as file:
    # Read the CSV data into a list of dictionaries
    reader = csv.DictReader(file)
    input_data = list(reader)

# Skip first row due to merged 2-row header
input_data = input_data[1:]

# Debug: Only do a few rows
# input_data = input_data[450:]

# Store the UG-reqs requirements as a dictionary to print at the end
# E.g. {'WAY-AQR': ['ENGR 76', ...], ...}
# Don't write them to the file so the user can pick which ones are important or not.
all_ug_reqs = {}

# For each row
for row in tqdm(input_data):
    # Get the class name
    class_name = row['Class']

    # Remove any spaces in the class name (e.g. CS 224N -> CS224N)
    class_name_nospace = class_name.replace(' ', '')

    # Get the class quarters
    url = 'https://explorecourses.stanford.edu/print?filter-term-Winter=on&filter-term-Autumn=on&filter-term-Spring=on&filter-coursestatus-Active=on&q=' + class_name_nospace
    response = requests.get(url, timeout=1000)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the .searchResult that contains `<span class="courseNumber">{class_name}:</span>`
    course_span = soup.find('span', text=lambda text: bool(text) and (class_name + ':' in text))
    if course_span is None:
        # If the class name is not found, skip this row
        row['Aut'] = row['Win'] = row['Spr'] = 'FALSE'
        continue

    # Go up three parent levels to the .searchResult
    search_result = course_span.findParent('div', {'class': 'searchResult'})

    if search_result is None:
        # If the class name is not found, skip this row
        row['Aut'] = row['Win'] = row['Spr'] = 'FALSE'
        continue

    # Get the courseTitle if not already in the CSV
    if row['Title'] == '':
        class_title = search_result.find('span', {'class': 'courseTitle'}).text  # type: ignore
        row['Title'] = class_title

    # Get the class quarters by extracting the relevant text from e.g.
    # <div class="courseAttributes">   Terms: Win | Units: 3-4</div>
    terms_string = search_result.find('div', {'class': 'courseAttributes'}).text  # type: ignore
    terms_string = terms_string.split('Terms:')[1].split('\r')[0].strip()

    # Write the terms we found
    for term_name in ['Aut', 'Win', 'Spr']:
        if term_name in terms_string:
            row[term_name] = 'TRUE'
        else:
            row[term_name] = 'FALSE'

    # Get the UG Requirements (text between 'UG Reqs:' and '\n')
    ug_reqs_string = search_result.find('div', {'class': 'courseAttributes'}).text  # type: ignore
    ug_reqs_string = ug_reqs_string.split('UG Reqs:')
    if len(ug_reqs_string) > 1:
        ug_reqs_string = ug_reqs_string[1].split('\r')[0].strip()
        ug_reqs_for_this_class = ug_reqs_string.split(', ')

        # Add class to dictionary for each UG req
        for ug_req in ug_reqs_for_this_class:
            if ug_req not in all_ug_reqs:
                all_ug_reqs[ug_req] = []
            all_ug_reqs[ug_req].append(class_name)


# Write the output file
with open(INPUT_FILE, 'w', newline='\n', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=input_data[0].keys())
    writer.writeheader()
    for row in input_data:
        writer.writerow(row)

# Alphabetize and print the UG requirements
print('### Requirements Satisfied by Courses ###\n')
for req_name, req_classes in sorted(all_ug_reqs.items()):
    classes_string = "\n".join(sorted(req_classes))
    print(f'## {req_name} ({len(req_classes)}) ##\n{classes_string}\n')
