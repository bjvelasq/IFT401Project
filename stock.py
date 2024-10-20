# stock.py

class Stock:
    def __init__(self, stock_code: str, stock_name: str, price: float, high_price: float, low_price: float, quantity_available: int):
        self.stock_code = stock_code
        self.stock_Name = stock_name
        self.price = price
        self.high_price = high_price
        self.low_price = low_price
        self.quantity_available = quantity_available

    def display_stock_info(self):
        print(f"Stock Code: {self.stock_code}")
        print(f"Stock Name: {self.stock_Name}")
        print(f"Price: {self.price}")
        print(f"High Price: {self.high_price}")
        print(f"Low Price: {self.low_price}")
        print(f"Quantity Available: {self.quantity_available}")
