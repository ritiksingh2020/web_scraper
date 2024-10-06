import json
import threading

class Database:
    def __init__(self, filename='products.json'):
        self.filename = filename
        self.lock = threading.Lock()

    def save_product(self, products: list):
        with self.lock:
            try:
                # Read existing data from the file
                with open(self.filename, 'r') as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # If the file does not exist or is empty, initialize as an empty dictionary
                data = {}

            # Update the data with new products
            for product in products:
                data[product["product_title"]] = product

            # Save the updated data to the file
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
