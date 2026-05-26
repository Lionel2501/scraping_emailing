import re
import requests
from bs4 import BeautifulSoup
import mysql.connector


def get_emails(urls):
    data = []
    for url_tuple in urls:
        url = url_tuple[0]
        if url is not None:
            try:
                response = requests.get(url)
                
                if response.status_code != 200:
                    print(f"URL: {url} - Código de estado: {response.status_code}")
                else:
                    print(f"URL OK: {url}")
                    

            except requests.exceptions.RequestException as e:
                print(f"Error al acceder a la URL: {url} , error: {e}")
                
def get_data_from_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='cessi'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT website FROM main WHERE email IS NULL")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

if __name__ == "__main__":
    data = get_data_from_db()
    get_emails(data)