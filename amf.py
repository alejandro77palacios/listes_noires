import re
from time import sleep

import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from babel import Locale
from datetime import datetime

locale = Locale('fr')
month_names = {name.lower(): i for i, name in enumerate(locale.months['format']['wide'].values(), start=1)}

def format_date(date_str):
    day, month_name, year = re.split('\s+', date_str)
    month = month_names[month_name]
    date = datetime(int(year), month, int(day))
    return date.strftime('%Y-%m-%d')

options = Options()
options.add_argument("--headless")
driver = Chrome(options=options)
driver.get('https://www.amf-france.org/fr/espace-epargnants/proteger-son-epargne/listes-noires-et-mises-en-garde')

data = []
sleep(3)
driver.find_element(By.XPATH, '//*[@id="tarteaucitronAllDenied2"]').click()

while True:
    try:
        rows = driver.find_elements(By.TAG_NAME, 'tr')[1:]
        print('Current url: ', driver.current_url)
        for row in rows:
            cols = row.find_elements(By.XPATH, './td')
            name = row.find_element(By.TAG_NAME, 'h2').text
            category = cols[1].find_element(By.CSS_SELECTOR, 'span.tag').text
            date = row.find_element(By.CSS_SELECTOR, 'div.date>span').text
            data.append((name, category, format_date(date)))
            print(data[0])
        print('Accumulated data: ', len(data))
        sleep(1)
        driver.find_element(By.XPATH, '//*[@id="block-amf-content"]/div[2]/div/div[2]/div/nav/ul/li[7]').click()
    except:
        print('no more pages')
        break
    sleep(1)

df = pd.DataFrame(data, columns=['name', 'category', 'date'])
df['website'] = df['name']
df['source'] = 'amf'
df = df[['name', 'website', 'category', 'date', 'source']]
df.to_csv('amf.csv', index=False)