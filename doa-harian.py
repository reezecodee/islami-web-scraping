import requests
import re
from bs4 import BeautifulSoup

url = "https://www.haibunda.com/moms-life/20220711103058-76-278670/30-doa-sehari-hari-lengkap-dengan-bacaan-latin-dan-artinya"

response = requests.get(url)
response.raise_for_status()  

soup = BeautifulSoup(response.text, 'html.parser')

doa_elements = soup.find_all('div', class_='isi-text pr-3')[0].find_all('h3')
doa_list = []

for doa_element in doa_elements:
    doa = {}
    
    nama_doa = doa_element.get_text(strip=True)
    filtered_nama_doa = re.sub(r'^\d+\.\s*', '', nama_doa)
    doa['nama'] = filtered_nama_doa

    arab = doa_element.find_next('p', style="text-align: right;").get_text(strip=True)
    doa['arab'] = arab

    arti_p = doa_element.find_next('p', string=lambda text: text and "Artinya:" in text)
    if arti_p:
        doa['arti'] = arti_p.get_text(strip=True).replace('Artinya:', '').strip()

    doa_list.append(doa)

with open('./data/doa-harian.txt', 'w', encoding='utf-8') as file:
    i = 1
    for doa in doa_list:
        file.write("{\n")
        file.write(f"\t urutan: {i}\n")
        file.write(f"\t namaDoa: {doa['nama']}\n")
        file.write(f"\t arab: {doa['arab']}\n")
        file.write(f"\t arti: {doa['arti']}\n")
        file.write("},\n")
        i+=1
