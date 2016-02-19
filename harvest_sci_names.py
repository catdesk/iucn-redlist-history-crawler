import csv
import json
import urllib.request

base_url = 'http://apiv3.iucnredlist.org/api/v3'
token = # need to import from token.txt

csv_data_file = 'table1.csv'
column_number = 1
out_file = 'synonyms.csv'

species_list = []
searched_list = []
unsearched_list = []
names_and_synonyms = {}

# import csv file with species names
listfile_unprocessed = []
with open(csv_data_file, newline='') as csvfile:
     listfile = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in listfile:
         listfile_unprocessed.append(row)

for row in listfile_unprocessed:
    species_name = row[(column_number - 1)]
    if species_name not in species_list:
        species_list.append(species_name)

# Remove header row
listfile_unprocessed.pop(0)

def request_synonyms(sci_name):
    req = urllib.request.urlopen(base_url + '/species/synonym/' + sci_name + token)
    
    req_body = req.read().decode('utf-8')
    req_json = json.loads(req_body)
    
    for listing in req_json['result']:
        accepted_name = listing['accepted_name']
        synonym = listing['synonym']
        if accepted_name in names_and_synonyms:
            synonym_list = names_and_synonyms[accepted_name]
            if synonym not in synonym_list:
                synonym_list.append(synonym)
        else:
            names_and_synonyms.update({accepted_name: [synonym]})

    check_if_in_list(species_list, accepted_name, unsearched_list)

def check_if_in_list(search_list, species_name, unsearched_list):
    if species_name not in search_list:
        print('not in search list')
        print('species_name')
        if species_name not in unsearched_list:
            unsearched_list.append(species_name)
            print('Unsearched:')
            print('species_name')
            print('unsearched_list')

for species in species_list:
    unsearched_list.append(species)

while unsearched_list:
    species = unsearched_list.pop(0)
    request_synonyms(species)
    searched_list.append(species)
