import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class Product:
    def __init__(self, id, name, category, price, stock):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

class ProductManager:
    def __init__(self):
        self.products = []
        self.csv_path = None

    def create_product(self, id, name, category, price, stock):
        new_product = Product(id, name, category, price, stock)
        self.products.append(new_product)
        self.save_to_csv()

    def read_products(self):
        return self.products

    def update_product(self, id, name=None, category=None, price=None, stock=None):
        for product in self.products:
            if product.id == id:
                if name is not None:
                    product.name = name
                if category is not None:
                    product.category = category
                if price is not None:
                    product.price = price
                if stock is not None:
                    product.stock = stock
                self.save_to_csv()
                return product
        return None

    def delete_product(self, id):
        for product in self.products:
            if product.id == id:
                self.products.remove(product)
                self.save_to_csv()
                return product
        return None

    def sort_products(self, key):
        self.products.sort(key=lambda x: getattr(x, key))

    def search_product(self, id):
        for product in self.products:
            if product.id == id:
                return product
        return None

    def import_csv(self, file_path):
        self.products.clear()
        self.csv_path = file_path
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    price = float(row['Price']) if row['Price'] else 0.0
                    stock = int(row['Stock']) if row['Stock'] else 0
                    self.create_product(row['ID'], row['Name'], row['Category'], price, stock)
                except ValueError as e:
                    print(f"Error importing row: {row}, Error: {e}")

    def save_to_csv(self):
        if self.csv_path:
            with open(self.csv_path, mode='w', newline='') as file:
                fieldnames = ['ID', 'Name', 'Category', 'Price', 'Stock']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for product in self.products:
                    writer.writerow({
                        'ID': product.id,
                        'Name': product.name,
                        'Category': product.category,
                        'Price': product.price,
                        'Stock': product.stock
                    })
