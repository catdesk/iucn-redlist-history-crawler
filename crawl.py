import mechanicalsoup

species = ["Ailuropoda melanoleuca", "Ardea insignis", "Chthonicola sagittatus"]
base_url = "http://www.iucnredlist.org"

print(base_url)

browser = mechanicalsoup.Browser()
page = browser.get(base_url + "/search")
search_form = page.soup.select("form")[0]
search_form.select("#quickSearchText")[0]['value'] = species

search_results = browser.submit(search_form, page.url)

species_listing = search_results.soup.find("span", class_="sciname", string=species[2])
species_listing_link = species_listing.previous_element.attrs['href']
species_page = browser.get(base_url + species_listing_link)

# Need to process synonyms out of html. for entry in synonyms_unprocessed, concatenate what's in spans? do i need to keep "subspecies" (see Ardea insignis)
synonyms_unprocessed = species_page.soup.find(string="Synonym(s):").find_previous("tr").find_all("div")

# Process IUCN Red List Assessments
assessment_table = species_page.soup.find(string="Previously published Red List assessments:").find_previous("tr").find_all("tr")
assessments = []

for row in assessment_table:
    cells = row.find_all("td")
    year = cells[0].string
    level = cells[2].next_element.string.strip().split()[-1].strip('()')
    assessments.append((year, level))

print(assessments)
print("##########1##########")
print(species_listing)
print("##########2##########")
print(synonyms_unprocessed)
print("##########3##########")
print("##########4##########")

