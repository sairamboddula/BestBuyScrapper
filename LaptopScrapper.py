from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from json import loads as jsonParse
from tkinter import filedialog

my_url = "https://www.bestbuy.com/site/searchpage.jsp?cp=1&searchType=search&st=laptop" \
         "&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&nrp=" \
         "&sp=-currentprice%20skuidsaas&qp=category_facet%3DSAAS~PC%20" \
         "Laptops~pcmcat247400050000%5Esystemmemoryram_facet%3DRAM~16%20gigabytes%5E" \
         "brand_facet%3DBrand~HP&list=n&af=true&iht=y&usc=All%20Categories&ks=960&keys=keys"

client = urlopen(my_url)
page_html = client.read()
client.close()

page_soup = soup(page_html, "html.parser")

laptops = page_soup.findAll("div", {"class": "list-item"})

laptopDetails = ""

for laptop in laptops:
    rating = laptop["data-average-rating"]
    brandJson = laptop["data-brand"]
    brand = jsonParse(brandJson)['brand']
    condition = laptop["data-condition"]
    availabilityJson = laptop["data-availability"]
    # availability = str(jsonParse(availabilityJson)['pickup']['available'])
    productUrl = "https://www.bestbuy.com" + laptop["data-url"]
    productTitle = laptop["data-title"]
    priceJson = laptop["data-price-json"]
    currentPrice = str(jsonParse(priceJson)["currentPrice"])

    try:
        regularPrice = str(jsonParse(priceJson)["regularPrice"])
        savings = str(jsonParse(priceJson)["savingsAmount"])
        savingsPercent = str(jsonParse(priceJson)["priceDomain"]["totalSavingsPercent"])
    except KeyError as e:
        regularPrice = "Not available"
        savings = "Not available"
        savingsPercent = "Not available"

    try:
        availability = str(jsonParse(availabilityJson)['pickup']['available'])
    except KeyError as e:
        availability = "Not available"
    try:
        timeAndDate = str(jsonParse(priceJson)["priceDomain"]["currentAsOfDate"])
    except KeyError as e:
        timeAndDate = "N/A"

    laptopDetails += (productTitle + "," + brand + "," + rating + "," + availability + "," + productUrl + ","
                      + currentPrice + "," + regularPrice + "," + savings + ","
                      + savingsPercent + "," + timeAndDate + "\n")

f = filedialog.asksaveasfile(mode="w", defaultextension=".csv", filetypes=[("All Files", "*.*")])
headers = "Product Title, Brand, Rating, Available, Product Link, Current Price, " \
          "Regular Price, Savings, Savings Percentage, Time stamp"
f.write(headers + "\n")

f.write(laptopDetails)

f.close()
