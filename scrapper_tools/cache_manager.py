import redis
import json
from logger_config import get_logger

class CacheManager:
    def __init__(self, host='localhost', port=6379, db=2):
        # Get a logger for this class
        self.logger = get_logger(__name__)

        # Connect to Redis
        try:
            self.cache = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
            self.logger.info("Connected to Redis successfully.")
        except Exception as e:
            self.logger.error("Failed to connect to Redis: %s", e)
            raise e

    def get_product(self, product_title: str):
        try:
            # Get the product from Redis
            product_data = self.cache.get(product_title)
            if product_data:
                # Deserialize JSON to dictionary
                return json.loads(product_data)
            return None
        except Exception as e:
            self.logger.error("Exception in get_product: %s", e)
            raise e

    def update_product(self, product):
        try:
            # Serialize the product dictionary to JSON and store in Redis
            product_title = product["product_title"]
            self.cache.set(product_title, json.dumps(product))
            self.logger.info("Product updated in cache: %s", product_title)
        except Exception as e:
            self.logger.error("Exception in update_product: %s", e)
            raise e
