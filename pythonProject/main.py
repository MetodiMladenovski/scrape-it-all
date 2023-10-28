import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup
from IPython.display import HTML
from datetime import date
import warnings
import matplotlib.pyplot as plt

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

matrix = []
for i in range(0, len(p_titles_simple)):
    node = {'Title': p_titles_simple[i], 'Type': p_types_simple[i], 'Price': p_prices_simple[i]}
    matrix.append(node)

df = pd.DataFrame(matrix)

stats = df.describe()
mean = df['Price'].mean()
median = df['Price'].median()
std = df['Price'].std()
minimum = df['Price'].min()
maximum = df['Price'].max()

df.hist(column='Price')
plt.show()

bargraph = df.plot.bar(x='Type', y='Price')