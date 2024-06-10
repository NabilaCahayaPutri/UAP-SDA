import csv

class Product:
    def __init__(self, product_id, name, category, price, stock):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.product_id}: {self.name} ({self.category}) - ${self.price} - Stock: {self.stock}"

class Store:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def display_products(self):
        for product in self.products:
            print(product)

    def update_product(self, product_id, name, category, price, stock):
        for product in self.products:
            if product.product_id == product_id:
                product.name = name
                product.category = category
                product.price = price
                product.stock = stock
                print(f"Product ID {product_id} updated.")
                return
        print(f"Product ID {product_id} not found.")

    def delete_product(self, product_id):
        self.products = [product for product in self.products if product.product_id != product_id]
        print(f"Product ID {product_id} deleted.")

    def import_from_csv(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_product(Product(row['ID'], row['Name'], row['Category'], row['Price'], row['Stock']))

    def sort_products_by_name(self):
        self.products.sort(key=lambda product: product.name)

    def sort_products_by_price(self):
        self.products.sort(key=lambda product: product.price)

    def search_products_by_name(self, name):
        results = [product for product in self.products if name.lower() in product.name.lower()]
        return results

    def search_products_by_category(self, category):
        results = [product for product in self.products if category.lower() in product.category.lower()]
        return results

def main():
    store = Store()
    
    while True:
        print("\nSistem Manajemen Toko Online")
        print("1. Add Product")
        print("2. Display Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Import Products from CSV")
        print("6. Sort Products by Name")
        print("7. Sort Products by Price")
        print("8. Search Product by Name")
        print("9. Search Product by Category")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            product_id = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            category = input("Enter Product Category: ")
            price = float(input("Enter Product Price: "))
            stock = int(input("Enter Product Stock: "))
            store.add_product(Product(product_id, name, category, price, stock))
        
        elif choice == '2':
            store.display_products()
        
        elif choice == '3':
            product_id = input("Enter Product ID to Update: ")
            name = input("Enter New Name: ")
            category = input("Enter New Category: ")
            price = float(input("Enter New Price: "))
            stock = int(input("Enter New Stock: "))
            store.update_product(product_id, name, category, price, stock)
        
        elif choice == '4':
            product_id = input("Enter Product ID to Delete: ")
            store.delete_product(product_id)
        
        elif choice == '5':
            filename = input("Enter CSV Filename: ")
            store.import_from_csv(filename)
        
        elif choice == '6':
            store.sort_products_by_name()
            print("Products sorted by name.")
        
        elif choice == '7':
            store.sort_products_by_price()
            print("Products sorted by price.")
        
        elif choice == '8':
            name = input("Enter Name to Search: ")
            results = store.search_products_by_name(name)
            for product in results:
                print(product)
        
        elif choice == '9':
            category = input("Enter Category to Search: ")
            results = store.search_products_by_category(category)
            for product in results:
                print(product)
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
