import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class Product:
    def _init_(self, id, name, category, price, stock):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

class ProductManager:
    def _init_(self):
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

class ProductManagerGUI:
    def _init_(self, root, product_manager):
        self.root = root
        self.product_manager = product_manager
        self.root.title("Online Store of Team Six")

        # Menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        product_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Product", menu=product_menu)
        product_menu.add_command(label="View Products", command=self.view_products)
        product_menu.add_command(label="Add Product", command=self.add_product)
        product_menu.add_command(label="Edit Product", command=self.edit_product)
        product_menu.add_command(label="Delete Product", command=self.delete_product)
        product_menu.add_command(label="Search Product", command=self.search_product)
        product_menu.add_separator()
        product_menu.add_command(label="Exit", command=root.quit)

        self.tree = ttk.Treeview(root, columns=('ID', 'Name', 'Category', 'Price', 'Stock'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Price', text='Price')
        self.tree.heading('Stock', text='Stock')
        self.tree.pack(fill=tk.BOTH, expand=True)

    def view_products(self):
        if not self.product_manager.read_products():
            result = messagebox.askyesno("Import CSV", "No products found. Do you want to import a CSV file?")
            if result:
                file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
                if file_path:
                    self.product_manager.import_csv(file_path)
                else:
                    return

        for i in self.tree.get_children():
            self.tree.delete(i)
        for product in self.product_manager.read_products():
            self.tree.insert("", "end", values=(product.id, product.name, product.category, f"Rp {product.price:,.2f}", product.stock))

    def add_product(self):
        self.create_product_window("Add Product")

    def edit_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "No product selected")
            return
        item = self.tree.item(selected_item)
        product_id = item['values'][0]
        product = self.product_manager.search_product(product_id)
        self.create_product_window("Edit Product", product)

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "No product selected")
            return
        item = self.tree.item(selected_item)
        product_id = item['values'][0]
        self.product_manager.delete_product(product_id)
        self.view_products()

    def search_product(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Product")
        search_window.geometry("300x100")

        tk.Label(search_window, text="Product ID:").pack(pady=5)
        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=5)
        search_button = tk.Button(search_window, text="Search", command=lambda: self.perform_search(search_entry.get()))
        search_button.pack(pady=5)

    def perform_search(self, product_id):
        product = self.product_manager.search_product(product_id)
        if product:
            messagebox.showinfo("Search Result", f"ID: {product.id}\nName: {product.name}\nCategory: {product.category}\nPrice: Rp {product.price:,.2f}\nStock: {product.stock}")
        else:
            messagebox.showerror("Search Error", "Product not found")

    def create_product_window(self, title, product=None):
        product_window = tk.Toplevel(self.root)
        product_window.title(title)
        product_window.geometry("300x380")

        tk.Label(product_window, text="ID:").pack(pady=5)
        id_entry = tk.Entry(product_window)
        id_entry.pack(pady=5)
        if product:
            id_entry.insert(0, product.id)
            id_entry.config(state='disabled')

        tk.Label(product_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(product_window)
        name_entry.pack(pady=5)
        if product:
            name_entry.insert(0, product.name)

        tk.Label(product_window, text="Category:").pack(pady=5)
        category_entry = tk.Entry(product_window)
        category_entry.pack(pady=5)
        if product:
            category_entry.insert(0, product.category)

        tk.Label(product_window, text="Price:").pack(pady=5)
        price_entry = tk.Entry(product_window)
        price_entry.pack(pady=5)
        if product:
            price_entry.insert(0, product.price)

        tk.Label(product_window, text="Stock:").pack(pady=5)
        stock_entry = tk.Entry(product_window)
        stock_entry.pack(pady=5)
        if product:
            stock_entry.insert(0, product.stock)

        action_button = tk.Button(product_window, text=title, command=lambda: self.save_product(product_window, id_entry.get(), name_entry.get(), category_entry.get(), price_entry.get(), stock_entry.get()))
        action_button.pack(pady=20)

    def save_product(self, window, id, name, category, price, stock):
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Input Error", "Price must be a float and Stock must be an integer")
            return
        if window.title() == "Add Product":
            self.product_manager.create_product(id, name, category, price, stock)
        elif window.title() == "Edit Product":
            self.product_manager.update_product(id, name, category, price, stock)
        window.destroy()
        self.view_products()

if __name__ == "__main__":
    product_manager = ProductManager()
    root = tk.Tk()
    gui = ProductManagerGUI(root, product_manager)
    root.mainloop()
