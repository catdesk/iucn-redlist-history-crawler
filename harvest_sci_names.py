import csv
import json
import urllib.request

base_url = 'http://apiv3.iucnredlist.org/api/v3'
token = # need to import from token.txt

# just pulled all this csv stuff from other file, didn't customise for this use yet
csv_data_file = 'table1.csv'
out_file = 'synonyms.csv'

# see crawler for how to use only specific column
# import csv file with species data
listfile_unprocessed = []
with open(csv_data_file, newline='') as csvfile:
     listfile = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in listfile:
         listfile_unprocessed.append(row)

# Remove header row
listfile_unprocessed.pop(0)

names_and_synonyms = {}
    
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

        # Make sure all synonyms are grabbed if original search is not an accepted name
        if accepted_name not in search_list:

print(names_and_synonyms)
request_synonyms('Geoemyda rubida')
print(names_and_synonyms)
request_synonyms('Rhinoclemmys rubida')
print(names_and_synonyms)
