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
        checkin_date = '2024-05-20'
        checkout_date = '2024-05-21'
        room = '3'
        total_pages = 10  # Jumlah halaman yang ingin Anda crawl

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        all_hotels_list = []  # Inisialisasi list untuk semua hotel dari semua halaman

        for page_number in range(1, total_pages + 1):
            page_url = f'https://www.booking.com/searchresults.id.html?ss=Yogyakarta%2C+Yogyakarta+Province%2C+Indonesia&ssne=Malang&ssne_untouched=Malang&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaGiIAQGYARK4ARfIAQzYAQHoAQH4AQuIAgGoAgO4Arrxg7AGwAIB0gIkMmJmYWM3NjYtMmVkMi00MjYxLTkwNzItMjUzYjc1OWUyMGY52AIG4AIB&sid=2475069a57f9b30bb3b96640eb607471&aid=304142&lang=id&sb=1&src_elem=sb&src=index&dest_id=-2703546&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=e4f91d1d39560098&ac_meta=GhAwYTBiMWQyNWRiMjcwMDU2IAAoATICZW46A1lvZ0AASgBQAA%3D%3D&checkin={checkin_date}&checkout={checkout_date}&group_adults=1&no_rooms={room}&group_children=0'
            page.goto(page_url, timeout=240000)

            # Auto scroll untuk memuat lebih banyak hasil
            auto_scroll(page)

            hotels = page.locator('//div[@data-testid="property-card"]').all()

            hotels_list = []
            for hotel in hotels:
                hotel_dict = {}
                hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
                hotel_dict['harga'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
                hotel_dict['rating'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
                # hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
                # hotel_dict['reviews count'] = \
                # hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

                hotels_list.append(hotel_dict)

            # Menggabungkan data dari halaman saat ini ke list yang berisi semua hotel
            all_hotels_list.extend(hotels_list)

            # Menunggu sebentar sebelum navigasi ke halaman berikutnya
            time.sleep(5)

        df = pd.DataFrame(all_hotels_list)

        # Menghapus baris yang merupakan duplikat
        df.drop_duplicates(inplace=True)

        df.to_excel('hotel-Yogya-test.xlsx', index=False)
        df.to_csv('hotel-Yogya-test.csv', index=False)

        browser.close()

if __name__ == '__main__':
    main()
