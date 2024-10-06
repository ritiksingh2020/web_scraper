from uvicorn import Server, Config
from scrapper_tools.main import app


if __name__ == "__main__":
    config = Config(app=app, host="0.0.0.0", port=8000, reload=True)
    server = Server(config=config)
    server.run()