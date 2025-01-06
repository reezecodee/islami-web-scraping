import requests
from bs4 import BeautifulSoup

url = 'https://www.cnnindonesia.com/edukasi/20240521125036-569-1100345/niat-sholat-5-waktu-sendiri-dan-berjamaah-arab-latin-artinya'

# Ambil konten halaman
response = requests.get(url)
response.raise_for_status()

# Parsing HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Ambil elemen h3 (jenis sholat), h4 (niat sholat), dan teks Arab
h3_elements = [h3.text.strip().replace("1. ", "").replace("2. ", "").replace("3. ", "").replace("4. ", "").replace("5. ", "") for h3 in soup.find_all('h3')]
h4_elements = [h4.text.strip() for h4 in soup.find_all('h4')]
arab_elements = [p.text.strip() for p in soup.find_all('p', style="text-align: right;")]  # Ambil teks Arab berdasarkan style

# Ambil elemen <p> dengan teks Arab-Latin dan artinya
p_with_em = [p.text.strip() for p in soup.find_all('p') if p.find('em')]
p_siblings = [p.find_next_sibling('p').text.strip().replace("Artinya:", "").strip() for p in soup.find_all('p') if p.find('em') and p.find_next_sibling('p')]

# Gabungkan data berdasarkan urutan jenis sholat
data = []
for i, jenis in enumerate(h3_elements):
    niat_sholat = h4_elements[i * 2:(i * 2) + 2]  # Ambil 2 niat untuk setiap jenis sholat
    arab_latin = p_with_em[i * 2:(i * 2) + 2]  # Ambil 2 arab latin untuk setiap jenis sholat
    arti = p_siblings[i * 2:(i * 2) + 2]  # Ambil 2 arti untuk setiap jenis sholat
    arab = arab_elements[i * 2:(i * 2) + 2]  # Ambil 2 teks Arab untuk setiap jenis sholat

    # Tambahkan data ke dalam struktur
    for j in range(2):  # Dua kali karena setiap jenis sholat punya 2 kategori (sendiri dan berjamaah)
        data.append({
            "jenisSholat": jenis,
            "niatSholat": niat_sholat[j] if j < len(niat_sholat) else None,
            "arab": arab[j] if j < len(arab) else None,
            "arabLatin": arab_latin[j] if j < len(arab_latin) else None,
            "arti": arti[j] if j < len(arti) else None
        })

# Simpan ke file .txt dalam format JSON-like
with open('./data/niat-sholat.txt', 'w', encoding='utf-8') as file:
    file.write("[\n")
    for item in data:
        file.write("    {\n")
        file.write(f"        jenisSholat: \"{item['jenisSholat']}\",\n")
        file.write(f"        niatSholat: \"{item['niatSholat']}\",\n")
        file.write(f"        arab: \"{item['arab']}\",\n")
        file.write(f"        latin: \"{item['arabLatin']}\",\n")
        file.write(f"        arti: {item['arti']}\n")
        file.write("    },\n")
    file.write("]\n")

