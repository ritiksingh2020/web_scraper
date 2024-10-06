from celery import Celery
from scrapper_tools.scraper import Scraper

# Initialize Celery app with Redis as the broker
app = Celery('tasks',
              broker='redis://localhost:6379/0',
              backend='redis://localhost:6379/1' )

@app.task
def scrape_products_task(page: int, proxy: str = None):
    scraper = Scraper(page=page, proxy=proxy)
    scraped_data = scraper.scrape()
    return f"Scraped {len(scraped_data)} products"
