from fastapi import Depends, FastAPI

from scrapper_tools.authentication import get_token
from scrapper_tools.scraper import Scraper
from scrapper_tools.worker import scrape_products_task, scrape_products
from scrapper_tools.worker import app as celery_app


app = FastAPI()


@app.get("/")
async def health_check():
    return{
        "status": "ok"
    }

@app.post("/scrape")
def start_scrape(pages_limit: int = 5, proxy: str = None, token: str = Depends(get_token)):
    task = scrape_products.delay(pages_limit, proxy)
    return {"scraping task has started with task_ids": task.id}


@app.get("/scrape/status/{task_id}")
def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {"status": "Pending..."}
    elif task.state == "SUCCESS":
        response = {"status": "Task completed successfully", "result": task.result}
    elif task.state == "FAILURE":
        response = {"status": "Task failed", "error": str(task.result)}
    else:
        response = {"status": str(task.state)}
    return response
