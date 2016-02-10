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
synonyms_unprocessed = species_page.soup.find(string="Synonym(s):").find_previous("tr").find_all("div")

print("##########1##########")
print(species_listing)
print("##########2##########")
print("##########3##########")
print("##########4##########")

