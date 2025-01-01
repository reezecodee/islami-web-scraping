import requests
from bs4 import BeautifulSoup

url = 'https://dev.to/reezecodee/apa-itu-bahasa-html-45i4' 

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('p')

    for idx, title in enumerate(titles, 1):
        print(f"{idx}. {title.get_text()}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
