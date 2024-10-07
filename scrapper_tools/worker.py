import logging
from celery import Celery, group, chord
from scrapper_tools.scraper import Scraper
from logger_config import get_logger

# Initialize Celery app with Redis as the broker
app = Celery('tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1')

# Set up logger
logger = get_logger(__name__)

@app.task
def scrape_products_task(page: int, proxy: str = None):
    try:
        scraper = Scraper(page=page, proxy=proxy)
        scraped_data = scraper.scrape()
        logger.info(f"Scraped page {page} successfully, found {len(scraped_data)} products.")
        return {"page": page, "data": scraped_data}
    except Exception as e:
        logger.error(f"Error in scrape_products_task on page {page}: {e}")
        raise e

@app.task
def notify_user(results):
    try:
        total_scraped_products = sum(len(page["data"]) for page in results)
        logger.info("All pages have been scraped.")
        logger.info(f"Total products scraped: {total_scraped_products}")
    except Exception as e:
        logger.error(f"Error in notify_user: {e}")
        raise e

@app.task
def scrape_products(page_number: int, proxy: str = None):
    try:
        # Create a group of scraping tasks for all the pages
        tasks = [scrape_products_task.s(page, proxy) for page in range(1, page_number + 1)]
        
        # Use a chord to wait for all tasks to complete before calling notify_user
        chord(tasks)(notify_user.s())
        logger.info(f"Started scraping tasks for {page_number} pages.")
    except Exception as e:
        logger.error(f"Error in scrape_products: {e}")
        raise e
