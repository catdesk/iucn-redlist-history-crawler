import mechanicalsoup
import random
import time
import csv

csv_name_file = 'table1.csv'
column_number = 1 # Column with scientific names to query for

species_list = []
species_data = []

base_url = "http://www.iucnredlist.org"
browser = mechanicalsoup.Browser()
page = browser.get(base_url + "/search")

# import csv file with species names
listfile_unprocessed = []
with open(csv_name_file, newline='') as csvfile:
     listfile = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in listfile:
         listfile_unprocessed.append(row)

print(listfile_unprocessed)

for row in listfile_unprocessed:
    species_name = row[(column_number - 1)]
    if species_name not in species_list:
        species_list.append(species_name)

species_list.pop(0) # Get rid of column title
print(species_list)

def get_species_data(page, species):
    search_form = page.soup.select("form")[0]
    search_form.select("#quickSearchText")[0]['value'] = species

    search_results = browser.submit(search_form, page.url)

    species_listing = search_results.soup.find("span", class_="sciname", string=species)
    species_listing_link = species_listing.previous_element.attrs['href']
    species_page = browser.get(base_url + species_listing_link)
    
    print(species_listing)
    print(species_listing_link)
    print(species_page)

    # Need to process synonyms out of html. for entry in synonyms_unprocessed, concatenate what's in spans? do i need to keep "subspecies" (see Ardea insignis)
    synonyms_unprocessed = ''
    if species_page.soup.find(string="Synonym(s):") != None:
      synonyms_unprocessed = species_page.soup.find(string="Synonym(s):").find_previous("tr").find_all("div")

    synonyms = []
    
    for synonym in synonyms_unprocessed:
        #not finished here....
        synonyms.append(str(synonym).strip("</div>").strip()) # for just turning it all into a string 
        print(synonyms)
    
    # Process IUCN Red List Assessments
    assessment_table = species_page.soup.find(string="Previously published Red List assessments:").find_previous("tr").find_all("tr")
    assessments = []
    
    for row in assessment_table:
        cells = row.find_all("td")
        year = cells[0].string
        level = cells[2].next_element.string.strip().split()[-1].strip('()')
        assessments.append((year, level))

    species_data.append((species, synonyms, assessments))

for species in species_list:
    random_sleep = random.randint(1, 5)
    print(random_sleep)
    time.sleep(random_sleep)
    print("#####specie#####")
    print(species)
    get_species_data(page, species)
    


print("######species_data#####")
print("##########1##########")
print(species_data)
print("##########2##########")
print("##########3##########")
print("##########4##########")

