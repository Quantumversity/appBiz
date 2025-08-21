import asyncio
from playwright.async_api import async_playwright

async def scrape_dynamic(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless=False to see the browser
        page = await browser.new_page()

        # Load page
        await page.goto(url, timeout=60000)

        # Wait for product list to render
        await page.wait_for_selector("#landmark-product-listing li", timeout=60000)

        # Select all product list items
        products = await page.query_selector_all("#landmark-product-listing li")

        results = []
        for product in products:
            # Title
            title_el = await product.query_selector("h4, h3")
            title = await title_el.inner_text() if title_el else "N/A"

            # Price
            price_el = await product.query_selector('[data-automation="product-price"], .screenReaderOnly_3anTj')
            price = await price_el.inner_text() if price_el else "N/A"

            # Link
            link_el = await product.query_selector("a")
            link = await link_el.get_attribute("href") if link_el else "N/A"
            if link and link.startswith("/"):
                link = f"https://www.bestbuy.ca{link}"

            results.append({
                "title": title.strip(),
                "price": price.strip(),
                "link": link
            })

        await browser.close()
        return results

if __name__ == "__main__":
    url = input("Enter the URL to crawl: ").strip()
    data = asyncio.run(scrape_dynamic(url))
    for item in data:
        print(f"{item['title']} - {item['price']} \n{item['link']}\n")
