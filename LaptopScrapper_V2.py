from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from json import loads as jsonParse

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

my_url = "https://www.bestbuy.com/site/searchpage.jsp?cp=1&searchType=search&st=laptop" \
         "&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&nrp=" \
         "&sp=-currentprice%20skuidsaas&qp=category_facet%3DSAAS~PC%20" \
         "Laptops~pcmcat247400050000%5Esystemmemoryram_facet%3DRAM~16%20gigabytes%5E" \
         "brand_facet%3DBrand~HP&list=n&af=true&iht=y&usc=All%20Categories&ks=960&keys=keys"

client = urlopen(my_url)
page_html = client.read()
client.close()

f = open("laptops.csv", "w")
headers = "Product Title, Brand, Rating, Available, Product Link, Current Price, " \
          "Regular Price, Savings, Savings Percentage, Time stamp" + "\n"
f.write(headers)
page_soup = soup(page_html, "html.parser")

laptops = page_soup.findAll("div", {"class": "list-item"})

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

    f.write(productTitle + "," + brand + "," + rating + "," + availability + "," + productUrl + ","
                      + currentPrice + "," + regularPrice + "," + savings + ","
                      + savingsPercent + "," + timeAndDate + "\n")

f.close()

file_to_attach = 'laptops.csv'
recipient_list = <recipient_list goes here>
subject = <insert the subject of the email>


def send_mail(filename, receiver, sub):

    email_sender = <insert email of the sender>
    email_recipient = receiver
    email_password = <insert the password of the sender email>

    email_subject = sub

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = email_subject

    mail_content = <insert message body here>
    msg.attach(MIMEText(mail_content, 'plain'))

    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + filename)

    msg.attach(part)
    email_text = msg.as_string()
    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.starttls()
    mail_server.login(email_sender, email_password)

    mail_server.sendmail(email_sender, email_recipient, email_text)
    mail_server.quit()

for recipient in recipient_list:
    send_mail(file_to_attach, recipient, subject)
