import json

class Database:
    def __init__(self, filename='products.json'):
        self.filename = filename

    def save_product(self, product):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(product)

        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
