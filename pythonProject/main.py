import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup
from IPython.display import HTML
from datetime import date
import warnings

# Setting up 'requests' to make HTTPS requests properly takes some extra steps... we'll skip them for now.
requests.packages.urllib3.disable_warnings()

warnings.filterwarnings("ignore")

snapshot_url = 'https://mobelix.com.mk/mk/mobilni-telefoni'
snapshot = requests.get(snapshot_url)
raw_html = snapshot.text
soup = BeautifulSoup(raw_html, 'html.parser')

phone_titles = soup.find_all('h5', {"class": "mb-0"})
p_titles_simple = []
for i in range(0, len(phone_titles)):
    p_titles_simple.append(phone_titles[i].text)

phone_types = soup.find_all('h3', {"class": "h5 font-weight-normal"})
p_types_simple = []
for i in range(0, len(phone_types)):
    p_types_simple.append(phone_types[i].text)

phone_prices = soup.find_all('p', {"class": "h5 price"})
p_prices_simple = []
for i in range(0, len(phone_prices)):
    unwanted = phone_prices[i].find('del')
    if unwanted:
        unwanted.extract()
    p_prices_simple.append(int(phone_prices[i].text
                               .replace('.00 ден', '')
                               .replace(",", "")
                               .replace(".", "")))

print(p_prices_simple)

# card_classes = soup.seleact('.Card-eyebrow')
#
# classes = []
# for i in range(0, len(card_classes)):
#     classes.append(card_classes[i].select_one('div').text)
#
# for i in range(len(card_classes), len(card_titles)):
#     classes.append(classes[len(card_classes) - 1])
#
# matrix = []
# for i in range(0, len(classes)):
#     node = {'Title': titles[i], 'Date': times[i], 'Class': classes[i]}
#     matrix.append(node)
#
# df = pd.DataFrame(matrix)
#
# matrix = []
# for i in range(0, len(classes)):
#     matrix.append([titles[i], times[i], classes[i]])
#
# df_new = pd.DataFrame(np.array(matrix), columns=['Title', 'Date', 'Class'])
#
# print(df_new)
