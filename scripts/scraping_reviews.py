import time
import re
import pandas as pd

from playwright.sync_api import sync_playwright
# from playwright_stealth import stealth_sync


PROVINCES = ["Aceh", "Bali", "Banten"]

max_scrolls = 10
scroll_pause = 2

with sync_playwright() as p:
    data = []


    for city in PROVINCES:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.google.com/maps")
        # time.sleep(5)
        page.wait_for_timeout(1000)
        # for city in PROVINCES:
        query = f"Mie Gacoan {city}"

        search = page.locator('#ucc-1')

        search.fill(query)
        page.wait_for_timeout(1000)

        # search.press("Enter")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)

        page.wait_for_selector('div[role="feed"]', timeout=50000)

        while True:
            # Paksa scroll elemen daftar ke paling bawah
            page.evaluate("""
                const feed = document.querySelector('div[role="feed"]');
                if (feed) { feed.scrollTo(0, feed.scrollHeight); }
            """)
            time.sleep(2) # Jeda agar tidak terdeteksi sebagai bot
                # Cek apakah sudah sampai akhir daftar
            end_text_visible = page.evaluate("""
                () => {
                    const xpath = "//*[contains(text(), 'Anda telah mencapai akhir daftar') or contains(text(), 'reached the end of the list')]";
                    const textNodes = document.evaluate(xpath, document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
                    return textNodes.snapshotLength > 0;
                }
            """)
            
            if end_text_visible:
                break
            links = page.query_selector_all('a[href*="maps/place"]')
            for link in links:
                name = link.get_attribute("aria-label")
                href = link.get_attribute("href")
                if name and href:
                    data.append({
                        "name": name,
                        "url": href,
                        # "province": province
            })
    df = pd.DataFrame(data)
    df.to_csv("../data/data_gacoan.csv", index=False)
    print(f"Saved {len(df)} records to maps_data_playwright.csv")

    browser.close()

