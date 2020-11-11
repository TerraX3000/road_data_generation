from bs4 import BeautifulSoup
import requests
import csv

# source = requests.get('https://www.manta.com/mb_45_E026X000_43/highway_and_street_construction/tennessee?pg=1').text

# print(soup.prettify())

csv_file = open('data/roadconstructioncompanies_georgia.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Company', 'Address', 'City', 'State', 'Zip', 'Website'])

count = 1

# for file in ['road01.html', 'road02.html', 'road03.html', 'road04.html']:
for file in ['data/road_ga01.html', 'data/road_ga02.html', 'data/road_ga03.html', 'data/road_ga04.html', 'data/road_ga05.html']:
    with open(file) as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    for business in soup.find_all('li', itemtype="http://schema.org/LocalBusiness"):
        print(count)
        company = business.find('strong', itemprop="name")
        company = company.text.strip()
        print(company)

        streetAddress = business.find('span', itemprop="streetAddress")
        if streetAddress:
            streetAddress = streetAddress.text
            print(streetAddress)
        else:
            streetAddress = ''
        addressLocality = business.find('span', itemprop="addressLocality")
        addressLocality = addressLocality.text
        print(addressLocality)
        addressRegion = business.find('span', itemprop="addressRegion")
        addressRegion = addressRegion.text
        print(addressRegion)
        postalCode = business.find('span', itemprop="postalCode")
        postalCode = postalCode.text
        print(postalCode)
        website = business.find('meta', itemprop="sameAs")
        if website:
            website = website["content"]
            print(website)
        else:
            website = ''
        print()
        count = count + 1
        csv_writer.writerow(
            [company, streetAddress, addressLocality, addressRegion, postalCode, website])

csv_file.close()
