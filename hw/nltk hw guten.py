import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup


def get_cse_lab(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    content = soup.select_one('#data')

    headers = [hearder.text.strip() for hearder in content.find_all('th')]
    rows = content.find('tbody').find_all('tr')
    items = [{head: value.get_text().strip() for head, value in zip(headers, row.find_all('td'))} for row in rows]

    return items

url = 'https://www.fantasypros.com/nfl/reports/leaders/rb.php?year=2015&start=1&end=17'
table = get_cse_lab(url)
df = pd.DataFrame(table)


df1 = df[:10]
s = df1['Avg'].values
a = df1['Player'].values
d = np.arange(len(a))
e = list(map(lambda x: float(x),s))
plt.barh(df1['Player'],e)
plt.show()