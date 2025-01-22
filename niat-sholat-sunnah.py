import requests
from bs4 import BeautifulSoup

# URL halaman web yang ingin di-scrape
url = "https://www.sonora.id/read/423799860/18-macam-sholat-sunnah-dan-niatnya-yang-harus-diketahui?page=all#goog_rewarded"

# Mengunduh konten HTML dari URL
response = requests.get(url)
html_content = response.text

# Parsing HTML dengan Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')

# Temukan semua bagian yang mengandung data sholat
sholat_items = soup.find_all('p')

# List untuk menyimpan data sholat
sholat_data = []

# Loop melalui setiap item sholat
for item in sholat_items:
    # Cari teks yang mengandung nama sholat
    if item.find('strong'):
        nama_sholat = item.find('strong').text.strip()
        
        # Hindari mengambil tag <strong> yang mengandung "Sonora.ID -" atau "Baca Juga:"
        if "Sonora.ID -" not in nama_sholat and "Baca Juga:" not in nama_sholat:
            # Inisialisasi variabel untuk teks Arab, Latin, dan arti
            teks_arab = ""
            teks_latin = ""
            arti = ""
            
            # Cari teks Arab (biasanya dalam tag <p> setelah <strong>)
            next_p = item.find_next('p')
            if next_p:
                next_p = next_p.find_next('p') 
                if next_p and not next_p.find('strong'): 
                    next_p = next_p.find_next('p') 
                if next_p and not next_p.find('strong'): 
                    teks_arab = next_p.text.strip()
            
            # Cari teks Latin (biasanya dalam tag <em> setelah teks Arab)
            next_em = next_p.find_next('em') if next_p else None
            if next_em:
                teks_latin = next_em.text.strip()
            
            # Cari arti (biasanya dalam tag <p> setelah teks Latin)
            next_p_arti = next_em.find_next('p') if next_em else None
            if next_p_arti and "Artinya:" in next_p_arti.text:
                arti = next_p_arti.text.strip().replace("Artinya: ", "")
            
            # Simpan data ke dalam list
            sholat_data.append({
                'Nama Sholat': nama_sholat,
                'Teks Arab': teks_arab,
                'Teks Latin': teks_latin,
                'Arti': arti
            })

# Menyimpan hasil ke dalam file .txt
with open("hasil_sholat.txt", "w", encoding="utf-8") as file:
    for sholat in sholat_data:
        file.write(f"Nama Sholat: {sholat['Nama Sholat']}\n")
        file.write(f"Teks Arab: {sholat['Teks Arab']}\n")
        file.write(f"Teks Latin: {sholat['Teks Latin']}\n")
        file.write(f"Arti: {sholat['Arti']}\n")
        file.write("-" * 50 + "\n")

print("Data telah disimpan ke dalam file hasil_sholat.txt")