import sys
from uvicorn import Server, Config
from scrapper_tools.main import app
from celery import Celery
from scrapper_tools.worker import app as celery_app

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "server"

    if mode == "server":
        # Start FastAPI server
        config = Config(app=app, host="0.0.0.0", port=8000, reload=True)
        server = Server(config=config)
        server.run()
    elif mode == "worker":
        # Start Celery worker
        celery_app.worker_main(argv=['worker', '--loglevel=info'])
