import csv
 
csv_data_file = 'out.csv'
out_file = 'processed.csv'

# import csv file with species data
listfile_unprocessed = []
with open(csv_data_file, newline='') as csvfile:
     listfile = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in listfile:
         listfile_unprocessed.append(row)

# Remove header row
listfile_unprocessed.pop(0)

species_data = {}
assessment_values = set()

for line in listfile_unprocessed:
    sci_name = line[0]
    assessment_year = line[-2]
    assessment_val = line[-1]
    if assessment_val == 'V' or assessment_val == 'Vulnerable':
        assessment_val = 'VU'
    elif 'Critically Endangered' in assessment_val and '(Possibly Extinct)' in assessment_val:
        assessment_val = 'CR(PE)'
    elif 'Critically Endangered' in assessment_val:
        assessment_val = 'CR'
    elif assessment_val == 'E' or assessment_val == 'Endangered':
        assessment_val = 'EN'
    elif assessment_val == 'Near Threatened':
        assessment_val = 'NT'
    elif assessment_val == 'Data Deficient':
        assessment_val = 'DD'
    elif assessment_val == 'Least Concern':
        assessment_val = 'LC'
    assessment_values.add(assessment_val)
    print(sci_name)
    if sci_name in species_data:
        assessment_list = species_data[sci_name]
        assessment_list.append([assessment_year, assessment_val])
    else:
        species_data.update({sci_name: [[assessment_year, assessment_val]]})

def write_results(sci_name, year, assessed_val):
    with open(out_file, 'a', newline='') as csvfile:
        outputter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        row_list = []
        row_list.append(sci_name)
        row_list.append(year)
        row_list.append(assessed_val)
        print(row_list)
        outputter.writerow(row_list)

# Read it backwards from 2015 to 1998 instead of dealing with sketchy sorting, still hasn't been tested
for sci_name, assessment_list in species_data.items():
    assessment_list.reverse()
    print(sci_name)
    last_assessed_val = 'NA'
    last_assessed_year = 1965
    assessment_table = {}
    for assessment in assessment_list:
        year = 1965
        assessment_year = int(assessment[0])
        assessed_val = assessment[1]
        while year < 2016:
            if assessment_year == year:
                last_assessed_val = assessed_val
                last_assessed_year = assessment_year
            if year >= last_assessed_year:
                assessment_table[year] = last_assessed_val
                print(year, last_assessed_val)
            year += 1
    print(assessment_list)
    for row in assessment_table.items():
        if row[0] > 1997:
            write_results(sci_name, row[0], row[1])
    
