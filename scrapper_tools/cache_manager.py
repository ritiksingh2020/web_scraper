import redis
import json

class CacheManager:
    def __init__(self, host='localhost', port=6379, db=2):
        # Connect to Redis
        self.cache = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def get_product(self, product_title: str):
        try:
            # Get the product from Redis
            product_data = self.cache.get(product_title)
            if product_data:
                # Deserialize JSON to dictionary
                return json.loads(product_data)
            return None
        except Exception as e:
            print("Exception in get_product:", e)
            raise e

    def update_product(self, product):
        try:
            # Serialize the product dictionary to JSON and store in Redis
            product_title = product["product_title"]
            self.cache.set(product_title, json.dumps(product))
        except Exception as e:
            print("Exception in update_product:", e)
            raise e
