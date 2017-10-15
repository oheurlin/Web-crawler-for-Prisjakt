import bs4
import re
import smtplib
import csv
import MailSender
from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup
from datetime import datetime

url = 'https://www.prisjakt.nu/kategori.php?m=s332317033&o=produkt_pris_inkmoms#rparams=m=s332317098'

#Opening the URL and grabbing the HTML page
client = req(url)
page_html = client.read()
client.close()

page_soup = soup(page_html, "html.parser")

#Grabs each container
containers = page_soup.findAll("tr" ,{"onclick":"expoc(event, this);"})


#Creates a new .csv file
time = str(datetime.now().strftime('%Y%m%d'))
f = open('ScrapedProducts' + time + '.csv', 'w')
headers = 'Product, Price (SEK), Size (inches)\n'
f.write(headers)

for container in containers:
    # Grabs each product's price and name
    num = 0
    container.append
    pricerow = container.find("td", {"class": "empty r"})
    pricerowstr = str(pricerow)
    pricerowstr.replace("&nbsp;", "")

    for i in range(len(pricerowstr) - 1):
        if pricerowstr[i] == ":" and pricerowstr[i + 1] == "-":
            if pricerowstr[i - 6].isdigit():
                n = 6
            else:
                n = 5
            priceraw = pricerowstr[i - n: i]
            price = priceraw.replace(" ", "")

    productrow = container.select_one('a').text
    product = str(productrow)

    sizerow = container.select(".cell-bar")
    sizerowstr = str(sizerow)
    for i in range(len(sizerowstr) - 1):
        if sizerowstr[i] == "t" and sizerowstr[i + 1] == "u" and sizerowstr[i + 2] == "m":
            if sizerowstr[i - 5].isdigit():
                n = 5
            else:
                n = 4
            sizeraw = sizerowstr[i - n: i]
            size = sizeraw.replace(",", ".")

    # Writes the name and price to the .csv file
    f.write(product + "," + price + "," + size + "\n")
    num = +1

#Compares yesterdays prices with todays
today_dict = dict()
f.close()
with open('ScrapedProducts' + time + '.csv', "r") as today:
    today_reader = csv.reader(today, delimiter=',')
    for row in today_reader:
        today_dict[row[0]] = row[1]

yesterdaytime_str = str(int(str(datetime.now().strftime('%Y%m%d'))) - 1)
with open('ScrapedProducts' + yesterdaytime_str + '.csv', "r") as yesterday_file:
    yesterday_reader = csv.reader(yesterday_file, delimiter = ',')
    for row in yesterday_reader:
        if row[0] in today_dict:
            if row[1] != today_dict.get(row[0]):
                attach_name = 'NewPrices' + time + '.csv'
                attach = open('NewPrices' + time + '.csv', 'w')
                headers = 'Product, New Price (SEK), Old Price (SEK), Size (inches)\n'
                attach.write(headers)
                attach.write(row[0] + "," + row[1] + "," + today_dict.get(row[0]) + "," + row[2] +"\n")

newmail = MailSender.Mailer(attach_name)
f.close()
