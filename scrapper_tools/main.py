from fastapi import Depends, FastAPI

from scrapper_tools.authentication import get_token
from scrapper_tools.scraper import Scraper


app = FastAPI()


@app.get("/")
async def health_check():
    return{
        "status": "ok"
    }

@app.post("/scrape")
def start_scrape(pages_limit: int = 5, proxy: str = None, token: str = Depends(get_token)):
    scraper = Scraper(pages_limit=pages_limit, proxy=proxy)
    scraped_data = scraper.scrape()
    return {"message": f"Scraped {len(scraped_data)} products"}
