import requests
from bs4 import BeautifulSoup

url = 'https://nu.or.id/syariah/99-asmaul-husna-dan-artinya-1T8jl' 

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')

with open('./data/asmaul-husna.txt', 'w', encoding='utf-8') as file:
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 3:  
            cell_values = [cell.get_text(strip=True) for cell in cells]
            if cell_values[0] == "No" or cell_values[1] == "Asmaul Husna(Latin)" or cell_values[2] == "Asmaul Husna(Arab)" or cell_values[3] == "Artinya":
                continue
            
            file.write("{\n")
            file.write(f"\t urutan: {cell_values[0]} \n")
            file.write(f"\t latin: {cell_values[1]} \n")
            file.write(f"\t arab: {cell_values[2]} \n")
            file.write(f"\t artinya: {cell_values[3]} \n")
            file.write("},\n")