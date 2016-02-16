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
    if assessment_val == 'V':
        assessment_val = 'VU'
    elif assessment_val == 'CR      (Possibly Extinct)':
        assessment_val = 'CR(PE)'
    elif assessment_val == 'E':
        assessment_val = 'EN'
    assessment_values.add(assessment_val)
    print(sci_name)
    if sci_name in species_data:
        assessment_list = species_data[sci_name]
        assessment_list.append([assessment_year, assessment_val])
        species_data.update({sci_name: assessment_list})
    else:
        species_data.update({sci_name: [[assessment_year, assessment_val]]})
    species_data[sci_name].sort()
    print(species_data[sci_name])

def write_results(sci_name, year, assessed_val):
    with open(out_file, 'a', newline='') as csvfile:
        outputter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        row_list = []
        row_list.append(sci_name)
        row_list.append(year)
        row_list.append(assessed_val)
        print(row_list)
        outputter.writerow(row_list)

for sci_name, assessment_list in species_data.items():
    year = 1965
    last_assessed_val = 'NA'
    for assessment in assessment_list:
        assessment_year = int(assessment[0])
        assessed_val = assessment[1]
        while year < 2016:
            if assessment_year == year:
                last_assessed_val = assessed_val
            if year > 1997:
                print(year)
                print(year > 1997)
                write_results(sci_name, year, last_assessed_val)
            year += 1
    
