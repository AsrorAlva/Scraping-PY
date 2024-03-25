from playwright.sync_api import sync_playwright
import pandas as pd
import time

def auto_scroll(page):
    last_height = page.evaluate("document.body.scrollHeight")
    while True:
        # Scroll ke bawah
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        # Tunggu sebentar untuk pemuatan konten baru
        time.sleep(2)
        # Hitung ketinggian yang baru
        new_height = page.evaluate("document.body.scrollHeight")
        # Jika ketinggian baru sama dengan yang lama, maka sudah mencapai bagian bawah
        if new_height == last_height:
            break
        last_height = new_height

def main():
    with sync_playwright() as p:
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        bandara_keberangkatan = 'JKT.CITY'
        bandara_kedatangan = 'YIA.CITY'
        keberangkatan = '2024-05-21'
        # kedatangan = '2024-03-27'

        # room = '3'
        total_pages = 10  # Jumlah halaman yang ingin Anda crawl

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        all_transport_list = []  # Inisialisasi list untuk semua data transportasi dari semua halaman

        for page_number in range(1, total_pages + 1):
            page_url = f'https://flights.booking.com/flights/JKT.CITY-YIA.CITY/?type=ONEWAY&adults=1&cabinClass=ECONOMY&children=&from={bandara_keberangkatan}&to={bandara_kedatangan}&fromCountry=ID&toCountry=ID&fromLocationName=Jakarta&toLocationName=Yogyakarta&depart={keberangkatan}&sort=BEST&travelPurpose=leisure&ca_source=flights_index_sb&aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaGiIAQGYARK4ARfIAQzYAQHoAQH4AQuIAgGoAgO4Arrxg7AGwAIB0gIkMmJmYWM3NjYtMmVkMi00MjYxLTkwNzItMjUzYjc1OWUyMGY52AIG4AIB'
            page.goto(page_url, timeout=240000)

            # Auto scroll untuk memuat lebih banyak hasil
            auto_scroll(page)

            transports = page.locator('//div[@data-testid="searchresults_card"]').all()

            transport_list = []
            for transport in transports:
                transport_dict = {}
                transport_dict['Nama Pesawat'] = transport.locator('//div[@data-testid="flight_card_carrier_0"]').nth(0).inner_text()
                transport_dict['Dari'] = transport.locator('//div[@data-testid="flight_card_segment_departure_airport_0"]').inner_text()
                transport_dict['Ke'] = transport.locator('//div[@data-testid="flight_card_segment_destination_airport_0"]').inner_text()
                transport_dict['Jam berangkat'] = transport.locator('//div[@data-testid="flight_card_segment_departure_time_0"]').inner_text()
                transport_dict['Jam sampai'] = transport.locator('//div[@data-testid="flight_card_segment_destination_time_0"]').inner_text()
                transport_dict['Harga'] = transport.locator('//div[@class="FlightCardPrice-module__priceContainer___nXXv2"]').inner_text()
                # Jika ada atribut lain yang ingin Anda ambil, tambahkan di sini

                transport_list.append(transport_dict)

            # Menggabungkan data dari halaman saat ini ke list yang berisi semua data transportasi
            all_transport_list.extend(transport_list)

            # Menunggu sebentar sebelum navigasi ke halaman berikutnya
            time.sleep(5)

        df = pd.DataFrame(all_transport_list)

        # Menghapus baris yang merupakan duplikat
        df.drop_duplicates(inplace=True)

        df.to_excel('transport-Lombok-final.xlsx', index=False)
        df.to_csv('transport-Lombok-final.csv', index=False)

        browser.close()

if __name__ == '__main__':
    main()
