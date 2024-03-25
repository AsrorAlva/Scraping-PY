from playwright.sync_api import sync_playwright
import pandas as pd
import time

# def auto_scroll(page):
#     last_height = page.evaluate("document.body.scrollHeight")
#     while True:
#         # Scroll ke bawah
#         page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#         # Tunggu sebentar untuk pemuatan konten baru
#         time.sleep(2)
#         # Hitung ketinggian yang baru
#         new_height = page.evaluate("document.body.scrollHeight")
#         # Jika ketinggian baru sama dengan yang lama, maka sudah mencapai bagian bawah
#         if new_height == last_height:
#             break
#         last_height = new_height

def main():
    with sync_playwright() as p:
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        # bandara_keberangkatan = 'JKT.CITY'
        # bandara_kedatangan = 'DPS.AIRPORT'
        #   keberangkatan = '2024-03-27'
        # kursi = '1'
        #   kedatangan = '2024-03-27'

        # room = '3'
        total_pages = 10  # Jumlah halaman yang ingin Anda crawl

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        all_transport_list = []  # Inisialisasi list untuk semua data transportasi dari semua halaman

        for page_number in range(1, total_pages + 1):
            page_url = f'https://www.google.com/search?sca_esv=78007b2132e03760&tbs=lf:1,lf_ui:9&tbm=lcl&sxsrf=ACQVn0-nN08VLALhwnZT8KVBSy_Y_DVdKg:1710948653141&q=tempat+kuliner+di+bali+maps&rflfq=1&num=10&sa=X&ved=2ahUKEwjE2su1lIOFAxUXbGwGHd2JABIQjGp6BAgaEAE&biw=1280&bih=598&dpr=1.5#rlfi=hd:;si:;mv:[[-8.680767830060892,115.32323661386715],[-8.75440818261155,115.0279790455078]]'
            page.goto(page_url, timeout=120000)

            # Auto scroll untuk memuat lebih banyak hasil
            # auto_scroll(page)

            transports = page.locator('//div[@class="cXedhc"]').all()

            transport_list = []
            for transport in transports:
                transport_dict = {}
                transport_dict['Nama Kuliner'] = transport.locator('//span[@class="OSrXXb"]').inner_text()
                transport_dict['Lokasi'] = transport.locator('//span[@class="TripRoute_location_name__1Tz5d"]').inner_text()
                # transport_dict['Ke'] = transport.locator('//div[@class="TripRoute_location_name__1Tz5d"]').inner_text()
                # transport_dict['Jam berangkat'] = transport.locator('//div[@data-testid="flight_card_segment_departure_time_0"]').inner_text()
                # transport_dict['Jam sampai'] = transport.locator('//div[@data-testid="flight_card_segment_destination_time_0"]').inner_text()
                # transport_dict['Harga'] = transport.locator('//span[@class="Text_text__3e9I4.Text_variant_alert__nSDvB.Text_size_h3__gskfv.Text_weight_bold__Ftpx2"]').inner_text()
                # Jika ada atribut lain yang ingin Anda ambil, tambahkan di sini

                transport_list.append(transport_dict)

            # Menggabungkan data dari halaman saat ini ke list yang berisi semua data transportasi
            all_transport_list.extend(transport_list)

            # Menunggu sebentar sebelum navigasi ke halaman berikutnya
            time.sleep(5)

        df = pd.DataFrame(all_transport_list)

        # Menghapus baris yang merupakan duplikat
        df.drop_duplicates(inplace=True)

        df.to_excel('transport-bali-final.xlsx', index=False)
        df.to_csv('transport-bali-final.csv', index=False)

        browser.close()

if __name__ == '__main__':
    main()
