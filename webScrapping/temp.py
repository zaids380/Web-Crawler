import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import random

#
# def get_proxies():
#     url = 'https://free-proxy-list.net/'
#     soup=bs(requests.get(url).content, 'html.parser')
#     proxies=[]
#     for row in soup.find("table", attrs={"id":"proxylisttable"}).find_all('tr')[1:]:
#         tds=row.find_all("td")
#         try:
#             ip=tds[0].text.strip()
#             port=tds[1].text.strip()
#             proxies.append(str(ip)+':'+str(port))
#         except IndexError:
#             continue
#     return proxies
#
# proxies=get_proxies()
# print(proxies)
# proxy_ip_port=proxies[random.randint(0,len(proxies)-1)]
# proxy=Proxy()
# proxy.proxyType=ProxyType.MANUAL
# proxy.httpProxy=proxy_ip_port
# proxy.sslProxy=proxy_ip_port
#
# capabilities=webdriver.DesiredCapabilities.CHROME
# proxy.add_to_capabilities(capabilities)
from selenium.webdriver.support.wait import WebDriverWait


def flipkart(product, no_of_products, sort_by, min_price, max_price, driver):
    # global driver
    # chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)
    # driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=chrome_options)
    print("preloaded")

    driver.get('https://www.flipkart.com')
    print("loaded")
    time.sleep(2)

    # close the login modal
    button = driver.find_element_by_xpath("/html/body/div[2]/div/div/button")
    button.click()

    # search mobile
    time.sleep(1)
    textbox = driver.find_element_by_name('q')
    textbox.send_keys(product)

    # click button to search
    time.sleep(2)
    searchbtn = driver.find_element_by_class_name('L0Z3Pu')
    searchbtn.click()

    # extracts links
    time.sleep(3)
    flipkart_links = []
    prod_count = 0
    flag = 0
    nc = 1
    flipkart_sort = dict()
    flipkart_sort['Relevance'] = '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/div[1]'
    # flipkart_sort['Popularity'] = '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/div[2]'
    flipkart_sort['Low_to_High'] = '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/div[3]'
    flipkart_sort['High_to_Low'] = '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/div[4]'
    flipkart_sort['Newest_First'] = '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[1]/div/div/div[2]/div[5]'

    min_price_dict = dict()
    min_price_dict['Min'] = 0
    min_price_dict['250'] = 1
    min_price_dict['500'] = 2
    min_price_dict['1000'] = 3
    min_price_dict['2000'] = 4
    min_price_dict['5000'] = 5

    max_price_dict = dict()
    max_price_dict['250'] = 0
    max_price_dict['500'] = 1
    max_price_dict['1000'] = 2
    max_price_dict['2000'] = 3
    max_price_dict['5000'] = 4
    max_price_dict['10000'] = 5
    max_price_dict['18000'] = 6
    max_price_dict['25000'] = 7
    max_price_dict['35000'] = 8
    max_price_dict['Max'] = 9

    sort = driver.find_element_by_xpath(flipkart_sort[sort_by])
    sort.click()

    #this needs to be automated
    price_range = driver.find_elements_by_class_name('_2YxCDZ')
    Select(price_range[1]).select_by_visible_text('₹' + max_price)
    time.sleep(2)
    Select(price_range[0]).select_by_visible_text('₹' + min_price)
    time.sleep(2)
    mins=[]
    maxs=[]

    min_range=price_range[0].find_elements_by_class_name('_3AsjWR')
    for all_min in min_range:
        mins.append(all_min.text)
    print(mins)
    max_range=price_range[1].find_elements_by_class_name('_3AsjWR')
    for all_max in max_range:
        maxs.append(all_max.text)
    print(maxs)

    # fetching all links
    while True:
        time.sleep(2)

        # time.sleep(1)
        elements = driver.find_elements_by_css_selector('._2rpwqI')
        for elem in elements:
            flipkart_links.append(elem.get_attribute('href'))
            prod_count += 1
            if prod_count == no_of_products:
                flag = 1
                break
        if flag == 0:
            if nc == 1:
                next = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[26]/div/div/nav/a[11]')
                nc = 0
            else:
                next = driver.find_element_by_xpath(
                    '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[26]/div/div/nav/a[12]')
            next.click()
            time.sleep(2)
        else:
            break
    # print(flipkart_links, len(flipkart_links))

    # fetching product details
    product_price = []
    product_name = []
    model_name = []
    source = []
    category = []
    color = []
    category_types = ['Browse Type', 'Headphone Type', 'Opening Mechanism', 'Output Interface']
    models_types = ['Model Number', 'Model Name']

    for link in flipkart_links:
        driver.get(link)
        # scrapping price
        delivery_input = driver.find_element_by_class_name('_36yFo0')
        delivery_input.send_keys("400072")
        delivery_btn = driver.find_element_by_class_name('_2P_LDn')
        delivery_btn.click()
        time.sleep(2)
        delivery = driver.find_elements_by_class_name('_3XINqE')

        if 'Delivery in' in delivery[0].text or 'Delivery by' in delivery[0].text:
            price = driver.find_element_by_css_selector('._16Jk6d')
            product_price.append(price.text[0] + ' ' + price.text[1:])

            # scrapping name
            name = driver.find_element_by_class_name('B_NuCI')
            product_name.append(name.text.strip())

            # scrapping other details
            table = driver.find_elements_by_class_name('_14cfVK')
            rows = table[0].find_elements_by_tag_name('tr')
            temp_dict = dict()
            for row in rows:
                col = row.find_elements_by_tag_name('td')
                temp_dict[col[0].text] = col[1].text

            for i in category_types:
                if i in temp_dict:
                    category.append(temp_dict[i])
                    break
            else:
                category.append("Unavailable")
            for i in models_types:
                if i in temp_dict:
                    model_name.append(temp_dict[i])
                    break
            else:
                model_name.append("Unavailable")
            # print(temp_dict)
            source.append("Flipkart")
        else:
            print('not deliverable')
    return product_name, product_price, model_name, source, category


def amazon(product, sort_by, min_price, max_price, no_of_product, driver):
    amazon_links = []
    # global driver
    # chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)
    # driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=chrome_options)

    print("preloaded")
    driver.get('https://www.amazon.in')
    print("loaded")
    time.sleep(2)

    search_bar = driver.find_element_by_id('twotabsearchtextbox')
    search_bar.send_keys(product)
    search_btn = driver.find_element_by_id('nav-search-submit-button')
    search_btn.click()

    time.sleep(2)
    amazon_sort = dict()
    amazon_sort['Relevance'] = '//*[@id="s-result-sort-select_0"]'
    amazon_sort['Low_to_High'] = '//*[@id="s-result-sort-select_1"]'
    amazon_sort['High_to_Low'] = '//*[@id="s-result-sort-select_2"]'
    amazon_sort['Newest_First'] = '//*[@id="s-result-sort-select_4"]'

    sort_dropdown = driver.find_element_by_xpath('//*[@id="a-autoid-0"]/span')
    sort_dropdown.click()
    sort = driver.find_element_by_xpath(amazon_sort[sort_by])
    sort.click()

    time.sleep(2)
    min_range = driver.find_element_by_name('low-price')
    min_range.send_keys(min_price)
    max_range = driver.find_element_by_name('high-price')
    max_range.send_keys(max_price)
    range_btn = driver.find_element_by_xpath('//*[@id="p_36/price-range"]/span/form/span[3]/span/input')
    range_btn.click()
    flag = 0
    while True:
        time.sleep(2)
        elements = driver.find_elements_by_xpath("//a[@class='a-size-base a-link-normal s-no-hover a-text-normal']")
        # print(len(elements))
        for elem in elements:
            amazon_links.append(elem.get_attribute('href'))
            if len(amazon_links) == no_of_product:
                flag = 1
                break
        if flag == 0:
            next_btn = driver.find_element_by_class_name('a-pagination')
            next = next_btn.find_element_by_class_name('a-last')
            next_a = next.find_element_by_tag_name('a')
            next_a.click()
        else:
            break
    # print(amazon_links, len(amazon_links))

    product_price = []
    product_name = []
    model_name = []
    source = []
    category = []


    additonal_dict = {}
    technical_dict = {}

    delivery = driver.find_element_by_id('glow-ingress-line2')
    delivery.click()
    time.sleep(2)
    delivery_input = driver.find_element_by_id('GLUXZipUpdateInput')
    delivery_input.send_keys('400072')
    delivery_btn = driver.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span')
    delivery_btn.click()

    for link in amazon_links:
        driver.get(link)

        time.sleep(1)

        title = driver.find_element_by_id('productTitle')
        product_name.append(title.text)
        price = driver.find_elements_by_id('priceblock_ourprice')
        if len(price) == 0:
            price = driver.find_elements_by_id('priceblock_dealprice')
        if len(price) == 0:
            price = driver.find_elements_by_id('priceblock_saleprice')

        product_price.append(price[0].text)

        source.append('Amazon')
        table = driver.find_element_by_id('productDetails_techSpec_section_1')
        rows = table.find_elements_by_tag_name('tr')
        for row in rows:
            th = row.find_element_by_tag_name('th')
            td = row.find_element_by_tag_name('td')
            technical_dict[th.text] = td.text

        if 'Item model number' in technical_dict:
            model_name.append(technical_dict['Item model number'])
        elif 'Series' in technical_dict:
            model_name.append(technical_dict['Series'])
        else:
            model_name.append('Not Available')
        technical_dict = {}

        table = driver.find_element_by_id('productDetails_detailBullets_sections1')
        rows = table.find_elements_by_tag_name('tr')
        for row in rows:
            th = row.find_element_by_tag_name('th')
            td = row.find_element_by_tag_name('td')
            additonal_dict[th.text] = td.text

        if 'Generic Name' in additonal_dict:
            category.append(additonal_dict['Generic Name'])
        else:
            category.append('Not Available')
        additonal_dict = {}
    print(model_name, len(model_name))
    print(category, len(category))

    return product_name, product_price, model_name, source, category


product = 'laptop'
no_of_product = 5
sort_by = 'High_to_Low'
min_price = '200'
max_price = '2000+'

global driver
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=chrome_options)
amazon_name, amazon_price, amazon_model, amazon_source, amazon_category = amazon(product, sort_by, min_price, max_price,
                                                                                 no_of_product, driver)
# flipkart_name, flipkart_price, flipkart_model, flipkart_source, flipkart_category = flipkart(product, no_of_product,
#                                                                                              sort_by, min_price,
#                                                                                              max_price, driver)

print('name', len(amazon_name))
print('price', len(amazon_price))
print('model', len(amazon_model))
print('source', len(amazon_source))
print('category', len(amazon_category))

# print(len(flipkart_name))
# if len(flipkart_name) > 0:
#     for i in range(len(flipkart_name)):
#         print(flipkart_name[i], flipkart_price[i], flipkart_model[i], flipkart_source[i], flipkart_category[i])
#
# # data = {"name": amazon_name + flipkart_name, "price": amazon_price + flipkart_price,
#         "source": amazon_source + flipkart_source, "model": amazon_model + flipkart_model,
#         "Category": amazon_category + flipkart_category}
# df = pd.DataFrame(data)
# df.to_csv("data.csv")
# print(df)

# container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div._1YokD2._3Mn1Gg >
# div:nth-child(5) > div > div:nth-child(2) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.URwL2w.col.col-9-12 > ul > li

# container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div._1YokD2._3Mn1Gg >
# div:nth-child(4) > div > div:nth-child(2) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.URwL2w.col.col-9-12 > ul > li

# container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div._1YokD2._3Mn1Gg >
# div:nth-child(5) > div > div:nth-child(2) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.URwL2w.col.col-9-12 > ul > li

# container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div._1YokD2._3Mn1Gg >
# div:nth-child(4) > div > div:nth-child(2) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.URwL2w.col.col-9-12 > ul > li

# container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div._1YokD2._3Mn1Gg >
# div:nth-child(5) > div > div:nth-child(2) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.URwL2w.col.col-9-12 > ul > li

# container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div._1YokD2._3Mn1Gg >
# div:nth-child(4) > div > div:nth-child(2) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.URwL2w.col.col-9-12 > ul > li

# container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div._1YokD2._3Mn1Gg >
# div:nth-child(5) > div > div:nth-child(2) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.URwL2w.col.col-9-12 > ul > li

# container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div._1YokD2._3Mn1Gg >
# div:nth-child(5) > div > div:nth-child(2) > div > div:nth-child(1) > table > tbody > tr:nth-child(3) > td.URwL2w.col.col-9-12 > ul > li

# for some product it was showing the time for delivery and for some nothing
