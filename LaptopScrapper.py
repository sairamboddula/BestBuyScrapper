from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from json import loads as jsonParse

my_url = "https://www.bestbuy.com/site/searchpage.jsp?cp=1&searchType=search" \
         "&_dyncharset=UTF-8&ks=960&sc=Global&list=y&usc=All%20Categories" \
         "&type=page&id=pcat17071&iht=n&seeAll=" \
         "&browsedCategory=pcmcat247400050000&st=categoryid%24pcmcat247400050000" \
         "&qp=systemmemoryram_facet%3DRAM~16%20gigabytes"

client = urlopen(my_url)
page_html = client.read()
client.close()

page_soup = soup(page_html, "html.parser")

laptops = page_soup.findAll("div", {"class": "list-item"})

filename = "laptops.csv"
f = open(filename, "w")
headers = "Product Title, Brand, Rating, Available, Product Link"
f.write(headers + "\n")

for laptop in laptops:
    rating = laptop["data-average-rating"]
    brandJson = laptop["data-brand"]
    brand = jsonParse(brandJson)['brand']
    condition = laptop["data-condition"]
    availabilityJson = laptop["data-availability"]
    availability = str(jsonParse(availabilityJson)['pickup']['available'])
    # priceJson = laptop["data-price-json"]
    # currentPrice = jsonParse(priceJson)["currentPrice"]
    # regularPrice = jsonParse(priceJson)["regularPrice"]
    # savings = jsonParse(priceJson)["savingsAmount"]
    # savingsPercent = jsonParse(priceJson)["priceDomain"]["totalSavingsPercent"]
    # timeAndDate = jsonParse(priceJson)["priceDomain"]["currentAsOfDate"]
    productUrl = "www.bestbuy.com" + laptop["data-url"]
    productTitle = laptop["data-title"]
    f.write(productTitle + "," + brand + "," + rating + "," + availability + "," + productUrl + "\n")

f.close()
