import time
import httpx
from bs4 import BeautifulSoup
import json
import os
from scrapper_tools.cache_manager import CacheManager
from scrapper_tools.database import Database

class Scraper:
    def __init__(self, page: int,  proxy: str = None):
        self.page = page
        self.proxy = proxy
        self.session = httpx.Client(proxies={'http': proxy, 'https': proxy}) if proxy else httpx.Client()
        self.cache = CacheManager()
        self.db = Database()

    def scrape(self):
        scraped_products = []
        try:
            page_content = self._scrape_page(self.page)
            products = self._parse_page(page_content)
            for product in products:
                if self._has_changed(product):
                    scraped_products.append(product)
                    self.cache.update_product(product)
            self.db.save_product(scraped_products)
        except Exception as e:
            print(f"Error on page {self.page}: {e}")
        print(f"Scraped and saved  {len(scraped_products)} products.")
        return scraped_products

    def _scrape_page(self, page_num: int):
        retry_attempts = 3
        retry_delays = [5, 10, 15]  

        url = f"https://dentalstall.com/shop/page/{page_num}/"
        
        for attempt in range(retry_attempts):
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code in [301, 302, 307]:
                    # Follow redirect if needed
                    response = self.session.get(response.headers["Location"], timeout=10)
                response.raise_for_status()
                return response.text  # Successful response
            except Exception as e:
                print(f"Error in _scrape_page on page {page_num}, attempt {attempt + 1} of {retry_attempts}: {e}")

                # If not the last attempt, sleep before retrying
                if attempt < retry_attempts - 1:
                    time.sleep(retry_delays[attempt])
                else:
                    # If all attempts fail, raise the exception
                    raise e

    def _parse_page(self, html: str):
        try:
            soup = BeautifulSoup(html, "html.parser")
            products = []
            for product in soup.select(".product"):
                name = product.select_one(".woo-loop-product__title a").text.strip()
                price = float(product.select_one(".woocommerce-Price-amount bdi").text.replace("₹", "").replace(",", "").strip())
                image_url = product.select_one("img").get("data-lazy-src")
                image_path = self._download_image(image_url)
                products.append({
                "product_title": name,
                "product_price": price,
                "path_to_image": image_path
            })
            return products
        except Exception as e:
            print(f"Error in _parse_page: {e}")
            raise e

    def _download_image(self, image_url: str):
        try:
            image_content = self.session.get(image_url).content
            image_name = image_url.split("/")[-1]
            image_path = os.path.join("images", image_name)
            with open(image_path, "wb") as image_file:
                image_file.write(image_content)
            return image_path
        except Exception as e:
            print(f"Error in _download_image: {e}")
            raise e

    def _has_changed(self, product):
        try:
            cached_product = self.cache.get_product(product["product_title"])
            if cached_product is None:
                return True
            return cached_product["product_price"] != product["product_price"]
        except Exception as e:
            print(f"Error in _has_changed: {e}")
            raise e
