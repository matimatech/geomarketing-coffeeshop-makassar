import time
import pandas as pd

from playwright.sync_api import sync_playwright

RESTOS = ["MyCoffee"]

max_scrolls = 10
scroll_pause = 2

with sync_playwright() as p:
    data = []

    for resto in RESTOS:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.google.com/maps")
        page.wait_for_timeout(1000)

        query = f"{resto}"
        search = page.locator('#ucc-1')
        search.fill(query)
        page.wait_for_timeout(1000)

        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)

        scrollabel_selector = 'div[role="main"]'
        if page.locator("div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd").count() > 0:
            page.locator("a.hfpxzc").first.click()
            scrollabel_selector = 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde'
        page.get_by_role("tab", name=f"Ulasan untuk {resto}").click()

        page.wait_for_selector(scrollabel_selector, timeout=50000)

        last_height = 0
        review_data = []
        before = 0
        after = 0
        while True:
            before = len(review_data)
            more_button = page.query_selector_all('button:has-text("Lainnya")')
            for btn in more_button:
                if btn.is_visible():
                    btn.click()

            page.evaluate("""
                const feed = document.querySelector('div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde');
                if (feed) {
                          feed.scrollTo(0, feed.scrollHeight);
                    }
            """)
            time.sleep(2) 

            review_elements = page.locator('.jftiEf.fontBodyMedium').all()
            
            for review in review_elements:
                text_element = review.locator('span.wiI7pd')
                if text_element.count() > 0:
                    text_element = text_element.inner_text()
                else:
                    text_element = ""

                name = review.locator('.d4r55').inner_text()
                rating = review.locator(".kvMYJc").get_attribute('aria-label')

                entry = {"nama": name, "reviews": text_element, "rating": rating}
                if entry not in review_data:
                    review_data.append(entry)
                    after = len(review_data)
                    print(len(review_data))

            if before == after:
                break

        df = pd.DataFrame(review_data)
        print(df)
        print(f"Saved {len(df)} records to reviews_{resto}.csv")
        df.to_csv(f"dataset/reviews_{resto}.csv", index=False)

    browser.close()

