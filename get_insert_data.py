import cloudscraper
import requests 
from bs4 import BeautifulSoup
import mysql.connector
import json
import re

def extract_company_name(website):
    pattern = re.compile(r'^(https?://www\.|https?://|www\.)|(https?://|www\.)?\.com$')
    cleaned_website = pattern.sub('', website) 
    cleaned_website = cleaned_website.split('.')[0]
    
    return cleaned_website

data = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
cookies = {'cookie_name': 'cookie_value'}
url = 'https://cessi.org.ar/socios/'
response = requests.get(url, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.text, 'lxml')

dataMain = soup.find('div', class_='logos-list anim2')
rows = dataMain.find_all('div', class_='row')

for row in rows:
    links = row.find_all('a', class_='w-100')
    
    for link in links:
        if link and link.has_attr('href'):
            data.append(link['href'])
         
result = []

for d in data:

    try:
        testLink = d

        responseLink = requests.get(
            testLink,
            headers=headers,
            cookies=cookies,
            timeout=10
        )

        if responseLink.status_code != 200:
            print(f"Erreur HTTP {responseLink.status_code} -> {testLink}")
            continue

        soupLink = BeautifulSoup(responseLink.text, 'lxml')

        dataLink = soupLink.find('div', class_='row socio-info anim3')

        if not dataLink:
            print(f"Bloc socio-info introuvable -> {testLink}")
            continue

        rowLink = dataLink.find_all('div', class_='col-12 col-sm-6 col-lg-3')

        website = None
        email = None
        empresa = None

        # WEBSITE
        if len(rowLink) > 1:

            website_tag = rowLink[1].find('a')

            if website_tag:
                website = website_tag.get_text(strip=True)

                try:
                    empresa = extract_company_name(website)
                except Exception as e:
                    print(f"Erreur extraction company -> {e}")

        # EMAIL
        if len(rowLink) > 2:

            email_tag = rowLink[2].find('a')

            if email_tag:
                email = email_tag.get_text(strip=True)

        if email and email.strip():

            obj = {
                'email': email,
                'empresa': empresa,
                'website': website,
                'link': testLink
            }

            result.append(obj)

            print(f"SUCCESS -> {empresa}")

        else:
            print(f"EMAIL ABSENT -> {testLink}")

    except Exception as e:
        print(f"Erreur sur {d}")
        print(e)

data_to_insert = [(item['email'], item['empresa'], item['website'], item['link']) for item in result]

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='cessi'
    )
    
    cursor = conn.cursor()
    
    mySql_insert_query = "INSERT INTO main (email, empresa, website, link) VALUES (%s, %s, %s, %s)"
    cursor.executemany(mySql_insert_query, data_to_insert)
    conn.commit()
    
except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conn.close()


