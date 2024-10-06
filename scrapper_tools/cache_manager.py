class CacheManager:
    def __init__(self):
        self.cache = {}

    def get_product(self, product_title: str):
        try:
            return self.cache.get(product_title)
        except Exception as e:
            print(e)
            raise e
    def update_product(self, product):
        try:
            self.cache[product["product_title"]] = product
        except Exception as e:
            print("Exception  on update_product", e)
            raise e
