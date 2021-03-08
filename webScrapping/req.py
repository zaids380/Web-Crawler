import requests
from bs4 import BeautifulSoup as bs
url='https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
soup=bs(requests.get(url).content,'html.parser')
# print(soup)
mydiv=soup.findAll("select", {"class": "_2YxCDZ"})
# print(mydiv)
price=[]
for div in mydiv:
    temp=[]
    for opt in div.find_all('option'):
        temp.append(opt.text)
    price.append(temp)
