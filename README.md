# Scraper Tool with Celery Integration

This project is a Python-based scraping tool that uses **FastAPI** for API integration and **Celery** for task management. The tool scrapes product information from a specified website and stores it in a local database. It also uses **Redis** as a broker for asynchronous task handling with Celery, enabling efficient scraping of multiple pages in parallel.

## Features

- **Scraping**: Extracts product information (name, price, image) from the given website.
- **Asynchronous Task Management**: Uses Celery to manage and distribute scraping tasks across multiple pages.
- **Retry Mechanism**: Automatically retries failed requests with exponential backoff.
- **Caching**: Uses Redis to cache previously scraped product data to prevent redundant data processing.
- **Logging**: A centralized logger to track events, errors, and results.

## Technologies Used

- **Python**: Main programming language.
- **FastAPI**: For exposing API endpoints.
- **Celery**: For managing asynchronous scraping tasks.
- **Redis**: Broker for Celery and caching.
- **httpx**: For making HTTP requests.
- **BeautifulSoup**: For parsing HTML and extracting data.



## Getting Started

### Prerequisites

- **Python 3.10+**
- **Redis** (for Celery broker and caching)

To install Redis locally, you can use Docker:

```sh
docker run -d -p 6379:6379 redis
```

### Installation

1. **Clone the Repository**

   ```sh
   git clone <repository-url>
   cd project_root
   ```

2. **Create a Virtual Environment**

   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

### Running the Application



#### 1. Start the FastAPI Application

```sh
python entrypoint.py
```

The API documentation will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

#### 2. Start the Celery Worker

```sh
python entrypoint.py worker
```

#### 3. you can use  below postman collection

```sh
https://drive.google.com/file/d/1G7c6SfEwrNV4YZthiMmsdlqhcrVUQEhB/view?usp=sharing
```


### Logging

The project uses a centralized logging mechanism defined in `logger_config.py`. The logs capture information about:

- Successful operations (e.g., scraping results).
- Errors and retries during scraping.
- Task initiation and completion.

### Project Features Explained

#### **Scraper**
- The `Scraper` class handles scraping product data from the specified website. It extracts product details like title, price, and image URL.
- Products are only updated if there is a change in the price.

#### **Celery Integration**
- Celery is used to distribute the scraping process into multiple asynchronous tasks.
- The `scrape_products_task` function scrapes individual pages, while the `scrape_products` function creates and manages tasks across multiple pages.
- The `notify_user` function is executed once all tasks are complete, summarizing the scraping results.

### Customizing the Project

- **Broker Configuration**: Update the Redis URL in `celery_app.py` to point to your Redis instance.
- **Proxy Settings**: Provide the `proxy` argument to the `Scraper` to use a proxy for requests.

### Contributing

Feel free to open issues, suggest features, or submit pull requests to improve the project. All contributions are welcome!



### Contact

For any inquiries, please contact [ritiksingh2020@gmail.com](mailto:ritiksingh2020@gmail.com).
