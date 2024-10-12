import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
import hashlib

# Connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price REAL NOT NULL,
                        category TEXT,
                        sales INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Hash passwords for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User authentication logic
def login():
    def verify_login():
        username = username_entry.get()
        password = hash_password(password_entry.get())
        
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        
        if user:
            login_window.destroy()
            inventory_gui()
        else:
            messagebox.showerror("Error", "Invalid username or password")
        conn.close()

    login_window = Tk()
    login_window.title("Login")
    
    Label(login_window, text="Username").grid(row=0, column=0)
    Label(login_window, text="Password").grid(row=1, column=0)
    
    username_entry = Entry(login_window)
    password_entry = Entry(login_window, show='*')
    
    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)
    
    Button(login_window, text="Login", command=verify_login).grid(row=2, column=0, columnspan=2)
    Button(login_window, text="Register", command=register).grid(row=3, column=0, columnspan=2)
    
    login_window.mainloop()

# Register new users
def register():
    def save_user():
        username = new_username_entry.get()
        password = hash_password(new_password_entry.get())
        
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "User registered successfully")
        register_window.destroy()

    register_window = Tk()
    register_window.title("Register")
    
    Label(register_window, text="Username").grid(row=0, column=0)
    Label(register_window, text="Password").grid(row=1, column=0)
    
    new_username_entry = Entry(register_window)
    new_password_entry = Entry(register_window, show='*')
    
    new_username_entry.grid(row=0, column=1)
    new_password_entry.grid(row=1, column=1)
    
    Button(register_window, text="Register", command=save_user).grid(row=2, column=0, columnspan=2)
    
    register_window.mainloop()

# Main inventory management GUI
def inventory_gui():
    root = Tk()
    root.title('Inventory Management System')

    # Treeview to show inventory
    tree = ttk.Treeview(root, columns=('ID', 'Name', 'Quantity', 'Price', 'Category', 'Sales'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Quantity', text='Quantity')
    tree.heading('Price', text='Price')
    tree.heading('Category', text='Category')
    tree.heading('Sales', text='Sales')
    tree.pack()

    # Load inventory data
    def load_inventory():
        for i in tree.get_children():
            tree.delete(i)
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert('', END, values=row)
        conn.close()

    # Add product
    def add_product():
        def save_product():
            name = name_entry.get()
            quantity = int(quantity_entry.get())
            price = float(price_entry.get())
            category = category_entry.get()

            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, quantity, price, category) VALUES (?, ?, ?, ?)",
                           (name, quantity, price, category))
            conn.commit()
            conn.close()
            load_inventory()
            add_window.destroy()

        add_window = Toplevel(root)
        add_window.title("Add Product")
        
        Label(add_window, text="Name").grid(row=0, column=0)
        Label(add_window, text="Quantity").grid(row=1, column=0)
        Label(add_window, text="Price").grid(row=2, column=0)
        Label(add_window, text="Category").grid(row=3, column=0)

        name_entry = Entry(add_window)
        quantity_entry = Entry(add_window)
        price_entry = Entry(add_window)
        category_entry = Entry(add_window)

        name_entry.grid(row=0, column=1)
        quantity_entry.grid(row=1, column=1)
        price_entry.grid(row=2, column=1)
        category_entry.grid(row=3, column=1)

        Button(add_window, text="Save", command=save_product).grid(row=4, column=0, columnspan=2)

    # Edit product
    def edit_product():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to edit")
            return
        product_id = tree.item(selected_item)['values'][0]

        def save_edit():
            name = name_entry.get()
            quantity = int(quantity_entry.get())
            price = float(price_entry.get())
            category = category_entry.get()

            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET name = ?, quantity = ?, price = ?, category = ? WHERE id = ?",
                           (name, quantity, price, category, product_id))
            conn.commit()
            conn.close()
            load_inventory()
            edit_window.destroy()

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        conn.close()

        edit_window = Toplevel(root)
        edit_window.title("Edit Product")
        
        Label(edit_window, text="Name").grid(row=0, column=0)
        Label(edit_window, text="Quantity").grid(row=1, column=0)
        Label(edit_window, text="Price").grid(row=2, column=0)
        Label(edit_window, text="Category").grid(row=3, column=0)

        name_entry = Entry(edit_window)
        name_entry.insert(0, product[1])
        quantity_entry = Entry(edit_window)
        quantity_entry.insert(0, product[2])
        price_entry = Entry(edit_window)
        price_entry.insert(0, product[3])
        category_entry = Entry(edit_window)
        category_entry.insert(0, product[4])

        name_entry.grid(row=0, column=1)
        quantity_entry.grid(row=1, column=1)
        price_entry.grid(row=2, column=1)
        category_entry.grid(row=3, column=1)

        Button(edit_window, text="Save", command=save_edit).grid(row=4, column=0, columnspan=2)

    # Delete product
    def delete_product():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product to delete")
            return
        product_id = tree.item(selected_item)['values'][0]

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
        load_inventory()

    # Low stock alert
    def generate_low_stock_alert():
        low_stock_window = Toplevel(root)
        low_stock_window.title("Low Stock Alerts")

        tree_low_stock = ttk.Treeview(low_stock_window, columns=('ID', 'Name', 'Quantity'), show='headings')
        tree_low_stock.heading('ID', text='ID')
        tree_low_stock.heading('Name', text='Name')
        tree_low_stock.heading('Quantity', text='Quantity')
        tree_low_stock.pack()

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE quantity < 5")  # Assuming threshold is 5
        rows = cursor.fetchall()
        for row in rows:
            tree_low_stock.insert('', END, values=row[:3])  # Only show id, name, and quantity
        conn.close()

    # Sales report (dummy implementation)
    def generate_sales_report():
        messagebox.showinfo("Sales Report", "Sales summary is not implemented yet.")

    # Add buttons for actions
    Button(root, text="Add Product", command=add_product).pack(side=LEFT)
    Button(root, text="Edit Product", command=edit_product).pack(side=LEFT)
    Button(root, text="Delete Product", command=delete_product).pack(side=LEFT)
    Button(root, text="Low Stock Alerts", command=generate_low_stock_alert).pack(side=LEFT)
    Button(root, text="Sales Report", command=generate_sales_report).pack(side=LEFT)

    load_inventory()
    root.mainloop()

# Run the application
if __name__ == "__main__":
    connect_db()
    login()
