# Fully Working Project

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import sqlite3
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

# ==================== Database Setup (Enhanced Self-Repairing) ====================
def init_database():
    conn = sqlite3.connect('pos_database.db')
    cursor = conn.cursor()

    # --- COMPREHENSIVE AUTO-FIX for database issues ---
    try:
        # Check if sales table exists and has correct structure
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(sales)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            # Check for ANY problematic column names
            problematic_columns = ['order-number', 'user-name', 'sale-date']
            needs_repair = any(col in column_names for col in problematic_columns)
            
            # Also check if correct column 'order_number' exists
            if 'order_number' not in column_names or needs_repair:
                print("⚙️ Detected invalid database structure — repairing...")
                
                # Backup data if table has valid structure partially
                backup_data = []
                if 'id' in column_names:
                    try:
                        # Try to backup existing data
                        cursor.execute("SELECT * FROM sales")
                        backup_data = cursor.fetchall()
                        print(f"📦 Backed up {len(backup_data)} sales records")
                    except sqlite3.Error:
                        print("⚠️ Could not backup data, creating fresh table")
                
                # Drop problematic tables
                cursor.execute("DROP TABLE IF EXISTS sale_items")
                cursor.execute("DROP TABLE IF EXISTS sales")
                conn.commit()
                print("🧹 Old tables removed successfully.")
        
    except sqlite3.Error as e:
        print(f"⚠️ Database check error: {e}")
        # If any error, rebuild from scratch
        cursor.execute("DROP TABLE IF EXISTS sale_items")
        cursor.execute("DROP TABLE IF EXISTS sales")
        conn.commit()

    # --- PRODUCTS TABLE ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            qty INTEGER NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            image TEXT
        )
    ''')

    # --- SALES TABLE (Correct version with underscore) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            user_name TEXT NOT NULL,
            sale_date TEXT NOT NULL,
            total REAL NOT NULL,
            tax REAL NOT NULL,
            payable REAL NOT NULL
        )
    ''')

    # --- SALE ITEMS TABLE ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            qty INTEGER NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales (id)
        )
    ''')

    # --- INSERT DEFAULT PRODUCTS IF EMPTY ---
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        initial_products = [
            ("89450000937", "Coke", 35, 49, "SoftDrink", "coke.png"),
            ("89450000938", "Pepsi", 35, 49, "SoftDrink", "pepsi.png"),
            ("89450000939", "7 Up", 35, 49, "SoftDrink", "7up.png"),
            ("89400000012", "Grilled Chicken", 7687, 150, "Food", "grilled_chicken.png"),
            ("89234500012", "Chicken Burger", 7, 49, "Burger", "chicken_burger.png"),
            ("89234500013", "Veg Burger", 7, 49, "Burger", "veg_burger.png"),
            ("89400000027", "Coffee", 247, 249, "Drink", "coffee.png"),
            ("89400000028", "Milk", 247, 249, "Drink", "milk.png"),
            ("89400000017", "Chicken Biryani", 376, 125, "Food", "chicken_biryani.png"),
            ("89400000014", "Lemon", 36, 55, "CoolDrink", "lemon.png"),
            ("89400000015", "Pineapple", 100, 35, "CoolDrink", "pineapple.png"),
            ("89400000021", "Strawberry 400gm", 50, 125, "Fruit", "strawberry.png"),
            ("89400000024", "Apple 400gm", 24, 49, "Fruit", "apple.png"),
            ("89400000036", "Grapes 1kg", 207, 99, "Fruit", "grapes.png")
        ]
        cursor.executemany('''
            INSERT INTO products (barcode, name, qty, price, category, image)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', initial_products)
        print("✅ Default products inserted.")

    conn.commit()
    conn.close()
    print("✅ Database initialized and verified successfully.")


# ==================== POS Application ====================
class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Billing System")
        self.root.geometry("1200x650")
        self.root.config(bg="#E9E9E9")

        self.cart = []
        self.order_number = self.generate_order_number()
        init_database()

        # ==================== LEFT: BILL AREA ====================
        left_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="white")
        left_frame.place(x=10, y=10, width=700, height=630)

        # Load Bill entry (replaced barcode)
        load_frame = tk.Frame(left_frame, bg="white")
        load_frame.pack(fill=tk.X, pady=5)
        tk.Label(load_frame, text="Load Bill (Order #):", bg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.load_entry = tk.Entry(load_frame, font=("Arial", 12), bd=2, relief=tk.SUNKEN)
        self.load_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.load_entry.bind('<Return>', lambda e: self.load_bill())
        tk.Button(load_frame, text="Load", command=self.load_bill, bg="#0078D7", fg="white").pack(side=tk.LEFT, padx=5)

        # User info display
        info_frame = tk.Frame(left_frame, bg="#F0F0F0", bd=2, relief=tk.RIDGE)
        info_frame.pack(fill=tk.X, pady=5, padx=5)
        tk.Label(info_frame, text="Current Order #:", bg="#F0F0F0", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.order_lbl = tk.Label(info_frame, text=self.order_number, bg="#F0F0F0", font=("Arial", 10), fg="blue")
        self.order_lbl.pack(side=tk.LEFT, padx=5)

        # Billing Table
        self.bill_table = ttk.Treeview(left_frame, columns=("name", "price", "qty", "total"), show="headings")
        self.bill_table.heading("name", text="Item")
        self.bill_table.heading("price", text="Price")
        self.bill_table.heading("qty", text="Quantity")
        self.bill_table.heading("total", text="Total")
        self.bill_table.column("name", width=250)
        self.bill_table.column("price", width=100)
        self.bill_table.column("qty", width=80)
        self.bill_table.column("total", width=100)
        self.bill_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind double-click on qty column
        self.bill_table.bind('<Double-Button-1>', self.edit_quantity)

        # Total section
        totals_frame = tk.Frame(left_frame, bg="white", bd=2, relief=tk.RIDGE)
        totals_frame.pack(fill=tk.X, pady=5)
        self.total_lbl = tk.Label(totals_frame, text="Total: ₹0", font=("Arial", 12, "bold"), bg="white")
        self.total_lbl.pack(side=tk.LEFT, padx=10)
        self.tax_lbl = tk.Label(totals_frame, text="Tax: ₹0", font=("Arial", 12, "bold"), bg="white")
        self.tax_lbl.pack(side=tk.LEFT, padx=10)
        self.pay_lbl = tk.Label(totals_frame, text="Payable: ₹0", font=("Arial", 12, "bold"), bg="white")
        self.pay_lbl.pack(side=tk.LEFT, padx=10)

        # Buttons
        btn_frame = tk.Frame(left_frame, bg="white")
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="Payment", bg="green", fg="white", font=("Arial", 13, "bold"), width=10, command=self.make_payment).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear Cart", bg="orange", fg="white", font=("Arial", 13, "bold"), width=10, command=self.clear_cart).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="View Bill", bg="purple", fg="white", font=("Arial", 13, "bold"), width=10, command=self.view_bill).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Download Bill", bg="#0078D7", fg="white", font=("Arial", 13, "bold"), width=10, command=self.download_bill).pack(side=tk.RIGHT, padx=5)

        # ==================== RIGHT: PRODUCT & CATEGORY AREA ====================
        right_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="#F7F7F7")
        right_frame.place(x=720, y=10, width=470, height=630)

        # User Name field
        user_frame = tk.Frame(right_frame, bg="#F7F7F7")
        user_frame.pack(fill=tk.X, pady=5)
        tk.Label(user_frame, text="User Name:", bg="#F7F7F7", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.user_name_var = tk.StringVar()
        tk.Entry(user_frame, textvariable=self.user_name_var, font=("Arial", 12), width=20).pack(side=tk.LEFT, padx=5)

        # Search bar
        search_frame = tk.Frame(right_frame, bg="#F7F7F7")
        search_frame.pack(fill=tk.X, pady=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=25).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", bg="#0078D7", fg="white", command=self.search_item).pack(side=tk.LEFT)

        # Right side split — vertical categories
        split_frame = tk.Frame(right_frame, bg="#F7F7F7")
        split_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Category buttons (vertical) - LEFT SIDE
        cat_frame = tk.Frame(split_frame, bg="#CFE2F3", width=120)
        cat_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        
        # Add ALL button first
        tk.Button(cat_frame, text="ALL", width=13, height=2, bg="#90EE90", font=("Arial", 9, "bold"), 
                  command=lambda: self.load_items(None)).pack(pady=5, padx=5)
        
        categories = self.get_categories()
        for cat in categories:
            tk.Button(cat_frame, text=cat, width=13, height=2, bg="#E0EAF3", 
                      command=lambda c=cat: self.load_items(c)).pack(pady=5, padx=5)

        # Product display with scrollbar - RIGHT SIDE
        product_container = tk.Frame(split_frame, bg="#FFFFFF")
        product_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Create canvas and scrollbar
        self.product_canvas = tk.Canvas(product_container, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(product_container, orient="vertical", command=self.product_canvas.yview)
        self.product_frame = tk.Frame(self.product_canvas, bg="#FFFFFF")
        
        # Configure scrollbar
        self.product_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create window in canvas
        self.canvas_frame = self.product_canvas.create_window((0, 0), window=self.product_frame, anchor="nw")
        
        # Bind configure event to update scroll region
        self.product_frame.bind("<Configure>", self.on_frame_configure)
        self.product_canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind mouse wheel events
        self.product_canvas.bind("<Enter>", self.bind_mousewheel)
        self.product_canvas.bind("<Leave>", self.unbind_mousewheel)
        
        self.load_items()

    # ==================== UTILITY FUNCTIONS ====================
    def generate_order_number(self):
        """Generate a unique 8-digit order number"""
        return str(random.randint(10000000, 99999999))

    # ==================== SCROLL FUNCTIONS ====================
    def on_frame_configure(self, event=None):
        """Update scroll region when frame size changes"""
        self.product_canvas.configure(scrollregion=self.product_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Update canvas window width when canvas is resized"""
        canvas_width = event.width
        self.product_canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def bind_mousewheel(self, event):
        """Bind mousewheel when mouse enters canvas"""
        self.product_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    
    def unbind_mousewheel(self, event):
        """Unbind mousewheel when mouse leaves canvas"""
        self.product_canvas.unbind_all("<MouseWheel>")
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.product_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # ==================== DATABASE FUNCTIONS ====================
    def get_categories(self):
        conn = sqlite3.connect('pos_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT category FROM products ORDER BY category')
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories

    def get_products(self, category=None):
        conn = sqlite3.connect('pos_database.db')
        cursor = conn.cursor()
        if category:
            cursor.execute('SELECT * FROM products WHERE category = ?', (category,))
        else:
            cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()
        return products

    def get_product_by_barcode(self, barcode):
        conn = sqlite3.connect('pos_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE barcode = ?', (barcode,))
        product = cursor.fetchone()
        conn.close()
        return product

    def update_product_qty(self, barcode, new_qty):
        conn = sqlite3.connect('pos_database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET qty = ? WHERE barcode = ?', (new_qty, barcode))
        conn.commit()
        conn.close()

    def get_sale_by_order_number(self, order_number):
        """Retrieve sale and its items by order number"""
        conn = sqlite3.connect('pos_database.db')
        cursor = conn.cursor()
        
        # Get sale info
        cursor.execute('SELECT * FROM sales WHERE order_number = ?', (order_number,))
        sale = cursor.fetchone()
        
        if sale:
            sale_id = sale[0]
            # Get sale items
            cursor.execute('SELECT * FROM sale_items WHERE sale_id = ?', (sale_id,))
            items = cursor.fetchall()
            conn.close()
            return sale, items
        
        conn.close()
        return None, None

    # ==================== UI FUNCTIONS ====================
    def load_items(self, category=None):
        # Clear existing items
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        products = self.get_products(category)

        for product in products:
            product_id, barcode, name, qty, price, cat, image = product
            frame = tk.Frame(self.product_frame, bd=2, relief=tk.RIDGE, bg="#FAFAFA")
            frame.pack(fill=tk.X, pady=3, padx=5)

            # Load image safely
            try:
                img_path = os.path.join(os.path.dirname(__file__), "images", image)
                img = Image.open(img_path).resize((60, 60))
                photo = ImageTk.PhotoImage(img)
            except Exception as e:
                img = Image.new("RGB", (60, 60), "gray")
                photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(frame, image=photo, bg="#FAFAFA")
            img_label.image = photo
            img_label.pack(side=tk.LEFT, padx=5)

            # Info
            info_frame = tk.Frame(frame, bg="#FAFAFA")
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Label(info_frame, text=name, font=("Arial", 10, "bold"), bg="#FAFAFA").pack(anchor="w")
            tk.Label(info_frame, text=f"₹{price} | Stock: {qty}", bg="#FAFAFA").pack(anchor="w")

            # Add button
            product_dict = {"barcode": barcode, "name": name, "price": price, "qty": qty}
            tk.Button(frame, text="+", bg="lightgreen", command=lambda p=product_dict: self.add_to_cart(p)).pack(side=tk.RIGHT, padx=3)
            tk.Button(frame, text="-", bg="lightcoral", command=lambda p=product_dict: self.remove_from_cart(p)).pack(side=tk.RIGHT, padx=3)
        
        # Update scroll region after loading items
        self.product_frame.update_idletasks()
        self.product_canvas.configure(scrollregion=self.product_canvas.bbox("all"))

    def add_to_cart(self, product):
        for item in self.cart:
            if item["name"] == product["name"]:
                item["qty"] += 1
                break
        else:
            self.cart.append({"barcode": product["barcode"], "name": product["name"], "price": product["price"], "qty": 1})
        self.update_bill()

    def remove_from_cart(self, product):
        for item in self.cart:
            if item["name"] == product["name"]:
                item["qty"] -= 1
                if item["qty"] <= 0:
                    self.cart.remove(item)
                break
        self.update_bill()

    def edit_quantity(self, event):
        """Edit quantity when double-clicking on qty column"""
        region = self.bill_table.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        column = self.bill_table.identify_column(event.x)
        row_id = self.bill_table.identify_row(event.y)
        
        # Check if qty column (column #3)
        if column == '#3' and row_id:
            # Get current values
            item_values = self.bill_table.item(row_id)['values']
            item_name = item_values[0]
            
            # Create entry widget for editing
            x, y, width, height = self.bill_table.bbox(row_id, column)
            
            entry = tk.Entry(self.bill_table, width=10)
            entry.place(x=x, y=y, width=width, height=height)
            entry.insert(0, item_values[2])
            entry.focus()
            entry.select_range(0, tk.END)
            
            def save_edit(event=None):
                new_qty = entry.get()
                entry.destroy()
                try:
                    new_qty = int(new_qty)
                    if new_qty > 0:
                        # Update cart
                        for item in self.cart:
                            if item["name"] == item_name:
                                item["qty"] = new_qty
                                break
                        self.update_bill()
                    elif new_qty == 0:
                        # Remove item
                        self.cart = [item for item in self.cart if item["name"] != item_name]
                        self.update_bill()
                    else:
                        messagebox.showwarning("Invalid", "Quantity must be positive!")
                except ValueError:
                    messagebox.showwarning("Invalid", "Please enter a valid number!")
            
            entry.bind('<Return>', save_edit)
            entry.bind('<FocusOut>', save_edit)

    def update_bill(self):
        for row in self.bill_table.get_children():
            self.bill_table.delete(row)

        total = 0
        for item in self.cart:
            total_item = item["price"] * item["qty"]
            total += total_item
            self.bill_table.insert("", "end", values=(item["name"], item["price"], item["qty"], total_item))

        tax = total * 0.05
        payable = total + tax
        self.total_lbl.config(text=f"Total: ₹{total:.2f}")
        self.tax_lbl.config(text=f"Tax: ₹{tax:.2f}")
        self.pay_lbl.config(text=f"Payable: ₹{payable:.2f}")

    def clear_cart(self):
        self.cart.clear()
        self.update_bill()
        # Generate new order number for next purchase
        self.order_number = self.generate_order_number()
        self.order_lbl.config(text=self.order_number)

    def make_payment(self):
        if not self.cart:
            messagebox.showwarning("Empty", "No items in cart!")
            return
        
        user_name = self.user_name_var.get().strip()
        if not user_name:
            messagebox.showwarning("User Name Required", "Please enter user name!")
            return

        # Calculate totals
        total = sum(item["price"] * item["qty"] for item in self.cart)
        tax = total * 0.05
        payable = total + tax

        conn = None
        try:
            conn = sqlite3.connect('pos_database.db')
            cursor = conn.cursor()

            # Verify table structure first
            cursor.execute("PRAGMA table_info(sales)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'order_number' not in columns:
                messagebox.showerror("Database Error", 
                    "Database structure is invalid. Please restart the application to repair the database.")
                return

            # Ensure unique order number (regenerate if duplicate)
            max_attempts = 10
            attempt = 0
            while attempt < max_attempts:
                cursor.execute("SELECT 1 FROM sales WHERE order_number = ?", (self.order_number,))
                if cursor.fetchone() is None:
                    break
                self.order_number = self.generate_order_number()
                self.order_lbl.config(text=self.order_number)
                attempt += 1
            
            if attempt >= max_attempts:
                messagebox.showerror("Error", "Could not generate unique order number. Please try again.")
                return

            # Insert sale with correct column names (underscores)
            cursor.execute('''
                INSERT INTO sales (order_number, user_name, sale_date, total, tax, payable)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.order_number, user_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  total, tax, payable))
            
            sale_id = cursor.lastrowid

            # Insert sale items
            for item in self.cart:
                cursor.execute('''
                    INSERT INTO sale_items (sale_id, product_name, price, qty, total)
                    VALUES (?, ?, ?, ?, ?)
                ''', (sale_id, item["name"], item["price"], item["qty"], item["price"] * item["qty"]))

            conn.commit()
            messagebox.showinfo("Payment", f"Payment Successful ✅\nOrder #: {self.order_number}")
            self.clear_cart()

        except sqlite3.Error as e:
            error_msg = str(e)
            if 'no such column' in error_msg.lower():
                messagebox.showerror("Database Error", 
                    f"Database structure error detected.\n\nPlease close and restart the application.\n\nTechnical details: {error_msg}")
            else:
                messagebox.showerror("Database Error", f"An error occurred while processing payment:\n{error_msg}")

        finally:
            if conn:
                conn.close()

    def view_bill(self):
        """View current cart as a bill"""
        if not self.cart:
            messagebox.showwarning("Empty", "No items in cart to view!")
            return
        
        user_name = self.user_name_var.get().strip()
        if not user_name:
            messagebox.showwarning("User Name Required", "Please enter user name!")
            return
        
        # Create bill window
        bill_window = tk.Toplevel(self.root)
        bill_window.title("Bill Preview")
        bill_window.geometry("500x600")
        bill_window.config(bg="white")
        
        # Bill content
        content_frame = tk.Frame(bill_window, bg="white", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        tk.Label(content_frame, text="Smart POS Billing System", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
        # Order and user info
        info_frame = tk.Frame(content_frame, bg="white")
        info_frame.pack(fill=tk.X, pady=10)
        tk.Label(info_frame, text=f"Order #: {self.order_number}", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"User Name: {user_name}", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", font=("Arial", 11), bg="white").pack(anchor="w")
        
        tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
        # Items table
        items_frame = tk.Frame(content_frame, bg="white")
        items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Header
        header_frame = tk.Frame(items_frame, bg="#E0E0E0")
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Item", width=20, font=("Arial", 10, "bold"), bg="#E0E0E0", anchor="w").pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="Price", width=8, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
        tk.Label(header_frame, text="Qty", width=5, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
        tk.Label(header_frame, text="Total", width=8, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
        
        # Items
        for item in self.cart:
            item_frame = tk.Frame(items_frame, bg="white")
            item_frame.pack(fill=tk.X, pady=2)
            tk.Label(item_frame, text=item["name"], width=20, font=("Arial", 10), bg="white", anchor="w").pack(side=tk.LEFT, padx=5)
            tk.Label(item_frame, text=f"₹{item['price']:.2f}", width=8, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
            tk.Label(item_frame, text=str(item["qty"]), width=5, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
            tk.Label(item_frame, text=f"₹{item['price'] * item['qty']:.2f}", width=8, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
        
        tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
        # Totals
        total = sum(item["price"] * item["qty"] for item in self.cart)
        tax = total * 0.05
        payable = total + tax
        
        totals_frame = tk.Frame(content_frame, bg="white")
        totals_frame.pack(fill=tk.X, pady=10)
        tk.Label(totals_frame, text=f"Subtotal: ₹{total:.2f}", font=("Arial", 11, "bold"), bg="white").pack(anchor="e")
        tk.Label(totals_frame, text=f"Tax (5%): ₹{tax:.2f}", font=("Arial", 11, "bold"), bg="white").pack(anchor="e")
        tk.Label(totals_frame, text=f"Total Payable: ₹{payable:.2f}", font=("Arial", 13, "bold"), bg="white", fg="green").pack(anchor="e")
        
        tk.Label(content_frame, text="=" * 50, bg="white").pack()
        tk.Label(content_frame, text="Thank you for your business!", font=("Arial", 10, "italic"), bg="white").pack(pady=10)

    def load_bill(self):
        """Load a previous bill by order number"""
        order_number = self.load_entry.get().strip()
        if not order_number:
            messagebox.showwarning("Order Number Required", "Please enter order number!")
            return
        
        sale, items = self.get_sale_by_order_number(order_number)
        
        if not sale:
            messagebox.showinfo("Not Found", "Order number not found!")
            return
        
        # Create bill window
        bill_window = tk.Toplevel(self.root)
        bill_window.title(f"Bill - Order #{order_number}")
        bill_window.geometry("500x600")
        bill_window.config(bg="white")
        
        # Bill content
        content_frame = tk.Frame(bill_window, bg="white", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        tk.Label(content_frame, text="Smart POS Billing System", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
        # Order and user info
        sale_id, order_num, user_name, sale_date, total, tax, payable = sale
        info_frame = tk.Frame(content_frame, bg="white")
        info_frame.pack(fill=tk.X, pady=10)
        tk.Label(info_frame, text=f"Order #: {order_num}", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"User Name: {user_name}", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        tk.Label(info_frame, text=f"Date: {sale_date}", font=("Arial", 11), bg="white").pack(anchor="w")
        
        tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
        # Items table
        items_frame = tk.Frame(content_frame, bg="white")
        items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Header
        header_frame = tk.Frame(items_frame, bg="#E0E0E0")
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Item", width=20, font=("Arial", 10, "bold"), bg="#E0E0E0", anchor="w").pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="Price", width=8, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
        tk.Label(header_frame, text="Qty", width=5, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
        tk.Label(header_frame, text="Total", width=8, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
        
        # Items
        for item in items:
            item_id, sale_id_fk, product_name, price, qty, item_total = item
            item_frame = tk.Frame(items_frame, bg="white")
            item_frame.pack(fill=tk.X, pady=2)
            tk.Label(item_frame, text=product_name, width=20, font=("Arial", 10), bg="white", anchor="w").pack(side=tk.LEFT, padx=5)
            tk.Label(item_frame, text=f"₹{price:.2f}", width=8, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
            tk.Label(item_frame, text=str(qty), width=5, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
            tk.Label(item_frame, text=f"₹{item_total:.2f}", width=8, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
        
        tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
        # Totals
        totals_frame = tk.Frame(content_frame, bg="white")
        totals_frame.pack(fill=tk.X, pady=10)
        tk.Label(totals_frame, text=f"Subtotal: ₹{total:.2f}", font=("Arial", 11, "bold"), bg="white").pack(anchor="e")
        tk.Label(totals_frame, text=f"Tax (5%): ₹{tax:.2f}", font=("Arial", 11, "bold"), bg="white").pack(anchor="e")
        tk.Label(totals_frame, text=f"Total Payable: ₹{payable:.2f}", font=("Arial", 13, "bold"), bg="white", fg="green").pack(anchor="e")
        
        tk.Label(content_frame, text="=" * 50, bg="white").pack()
        tk.Label(content_frame, text="Thank you for your business!", font=("Arial", 10, "italic"), bg="white").pack(pady=10)
        
        self.load_entry.delete(0, tk.END)

    def download_bill(self):
        if not self.cart:
            messagebox.showwarning("Empty", "No items to download!")
            return
        
        user_name = self.user_name_var.get().strip()
        if not user_name:
            messagebox.showwarning("User Name Required", "Please enter user name!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            filetypes=[("PDF File", "*.pdf"), ("Text File", "*.txt")]
        )
        
        if not file_path:
            return
        
        if file_path.endswith('.pdf'):
            self.generate_pdf_bill(file_path, user_name)
        else:
            self.generate_text_bill(file_path, user_name)

    def generate_pdf_bill(self, file_path, user_name):
        """Generate PDF bill using ReportLab"""
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph("<b>Smart POS Billing System</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Order and User info
        order_info = Paragraph(f"<b>Order Number:</b> {self.order_number}", styles['Normal'])
        elements.append(order_info)
        user_info = Paragraph(f"<b>User Name:</b> {user_name}", styles['Normal'])
        elements.append(user_info)
        date_text = Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        elements.append(date_text)
        elements.append(Spacer(1, 0.3*inch))
        
        # Table data
        data = [['Item', 'Price', 'Qty', 'Total']]
        total = 0
        
        for item in self.cart:
            total_item = item["price"] * item["qty"]
            total += total_item
            data.append([
                item["name"],
                f"₹{item['price']:.2f}",
                str(item["qty"]),
                f"₹{total_item:.2f}"
            ])
        
        # Create table
        table = Table(data, colWidths=[3*inch, 1.5*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Totals
        tax = total * 0.05
        payable = total + tax
        
        totals_data = [
            ['', '', 'Subtotal:', f"₹{total:.2f}"],
            ['', '', 'Tax (5%):', f"₹{tax:.2f}"],
            ['', '', 'Total Payable:', f"₹{payable:.2f}"]
        ]
        
        totals_table = Table(totals_data, colWidths=[3*inch, 1.5*inch, 1*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (2, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (2, 0), (-1, -1), 11),
            ('LINEABOVE', (2, 0), (-1, 0), 1, colors.black),
            ('LINEABOVE', (2, 2), (-1, 2), 2, colors.black),
        ]))
        
        elements.append(totals_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer = Paragraph("<i>Thank you for your business!</i>", styles['Normal'])
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        messagebox.showinfo("Downloaded", "PDF Bill saved successfully ✅")

    def generate_text_bill(self, file_path, user_name):
        """Generate text bill"""
        with open(file_path, "w") as f:
            f.write("======== Smart POS Bill ========\n")
            f.write(f"Order Number: {self.order_number}\n")
            f.write(f"User Name: {user_name}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("----------------------------------\n")
            f.write("{:<20}{:<10}{:<10}{:<10}\n".format("Item", "Price", "Qty", "Total"))
            f.write("----------------------------------\n")
            total = 0
            for item in self.cart:
                total_item = item["price"] * item["qty"]
                total += total_item
                f.write(f"{item['name']:<20}{item['price']:<10}{item['qty']:<10}{total_item:<10}\n")
            f.write("----------------------------------\n")
            f.write(f"Total: ₹{total:.2f}\nTax: ₹{total*0.05:.2f}\nPayable: ₹{total*1.05:.2f}\n")
            f.write("==================================\n")
        messagebox.showinfo("Downloaded", "Bill saved successfully ✅")

    def search_item(self):
        query = self.search_var.get().lower()
        if query:
            conn = sqlite3.connect('pos_database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE LOWER(name) LIKE ?', (f'%{query}%',))
            filtered = cursor.fetchall()
            conn.close()
            
            if filtered:
                self.show_filtered_items(filtered)
            else:
                messagebox.showinfo("Not Found", "No matching items found.")
        else:
            self.load_items()

    def show_filtered_items(self, filtered):
        for widget in self.product_frame.winfo_children():
            widget.destroy()
        
        for product in filtered:
            product_id, barcode, name, qty, price, cat, image = product
            frame = tk.Frame(self.product_frame, bd=2, relief=tk.RIDGE, bg="#FAFAFA")
            frame.pack(fill=tk.X, pady=3, padx=5)
            
            # Load image safely
            try:
                img_path = os.path.join(os.path.dirname(__file__), "images", image)
                img = Image.open(img_path).resize((60, 60))
                photo = ImageTk.PhotoImage(img)
            except Exception as e:
                img = Image.new("RGB", (60, 60), "gray")
                photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(frame, image=photo, bg="#FAFAFA")
            img_label.image = photo
            img_label.pack(side=tk.LEFT, padx=5)
            
            # Info
            info_frame = tk.Frame(frame, bg="#FAFAFA")
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Label(info_frame, text=name, font=("Arial", 10, "bold"), bg="#FAFAFA").pack(anchor="w")
            tk.Label(info_frame, text=f"₹{price} | Stock: {qty}", bg="#FAFAFA").pack(anchor="w")
            
            product_dict = {"barcode": barcode, "name": name, "price": price, "qty": qty}
            tk.Button(frame, text="+", bg="lightgreen", command=lambda p=product_dict: self.add_to_cart(p)).pack(side=tk.RIGHT, padx=5)
        
        # Update scroll region after loading filtered items
        self.product_frame.update_idletasks()
        self.product_canvas.configure(scrollregion=self.product_canvas.bbox("all"))

# ==================== Run App ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()









# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from PIL import Image, ImageTk
# import os
# import sqlite3
# import random
# from datetime import datetime
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# from reportlab.lib.units import inch

# # ==================== Database Setup (Self-Repairing) ====================
# def init_database():

#     conn = sqlite3.connect('pos_database.db')
#     cursor = conn.cursor()

#     # --- AUTO-FIX for old column issue in 'sales' table ---
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'")
#     if cursor.fetchone():
#         cursor.execute("PRAGMA table_info(sales)")
#         existing_columns = [col[1] for col in cursor.fetchall()]

#         # If wrong column 'order-number' exists → drop table safely
#         if 'order-number' in existing_columns:
#             print("⚙️ Detected invalid column 'order-number' — repairing...")
#             cursor.execute("DROP TABLE IF EXISTS sales")
#             conn.commit()
#             print("🧹 Old 'sales' table removed successfully.")

#     # --- PRODUCTS TABLE ---
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS products (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             barcode TEXT UNIQUE NOT NULL,
#             name TEXT NOT NULL,
#             qty INTEGER NOT NULL,
#             price REAL NOT NULL,
#             category TEXT NOT NULL,
#             image TEXT
#         )
#     ''')

#     # --- SALES TABLE (Correct version) ---
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS sales (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             order_number TEXT UNIQUE NOT NULL,
#             user_name TEXT NOT NULL,
#             sale_date TEXT NOT NULL,
#             total REAL NOT NULL,
#             tax REAL NOT NULL,
#             payable REAL NOT NULL
#         )
#     ''')

#     # --- SALE ITEMS TABLE ---
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS sale_items (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             sale_id INTEGER NOT NULL,
#             product_name TEXT NOT NULL,
#             price REAL NOT NULL,
#             qty INTEGER NOT NULL,
#             total REAL NOT NULL,
#             FOREIGN KEY (sale_id) REFERENCES sales (id)
#         )
#     ''')

#     # --- INSERT DEFAULT PRODUCTS IF EMPTY ---
#     cursor.execute('SELECT COUNT(*) FROM products')
#     if cursor.fetchone()[0] == 0:
#         initial_products = [
#             ("89450000937", "Coke", 35, 49, "SoftDrink", "coke.png"),
#             ("89450000938", "Pepsi", 35, 49, "SoftDrink", "pepsi.png"),
#             ("89450000939", "7 Up", 35, 49, "SoftDrink", "7up.png"),
#             ("89400000012", "Grilled Chicken", 7687, 150, "Food", "grilled_chicken.png"),
#             ("89234500012", "Chicken Burger", 7, 49, "Burger", "chicken_burger.png"),
#             ("89234500013", "Veg Burger", 7, 49, "Burger", "veg_burger.png"),
#             ("89400000027", "Coffee", 247, 249, "Drink", "coffee.png"),
#             ("89400000028", "Milk", 247, 249, "Drink", "milk.png"),
#             ("89400000017", "Chicken Biryani", 376, 125, "Food", "chicken_biryani.png"),
#             ("89400000014", "Lemon", 36, 55, "CoolDrink", "lemon.png"),
#             ("89400000015", "Pineapple", 100, 35, "CoolDrink", "pineapple.png"),
#             ("89400000021", "Strawberry 400gm", 50, 125, "Fruit", "strawberry.png"),
#             ("89400000024", "Apple 400gm", 24, 49, "Fruit", "apple.png"),
#             ("89400000036", "Grapes 1kg", 207, 99, "Fruit", "grapes.png")
#         ]
#         cursor.executemany('''
#             INSERT INTO products (barcode, name, qty, price, category, image)
#             VALUES (?, ?, ?, ?, ?, ?)
#         ''', initial_products)
#         print("✅ Default products inserted.")

#     conn.commit()
#     conn.close()
#     print("✅ Database initialized and verified successfully.")



# # ==================== POS Application ====================
# class POSApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Smart POS Billing System")
#         self.root.geometry("1200x650")
#         self.root.config(bg="#E9E9E9")

#         self.cart = []
#         self.order_number = self.generate_order_number()
#         init_database()

#         # ==================== LEFT: BILL AREA ====================
#         left_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="white")
#         left_frame.place(x=10, y=10, width=700, height=630)

#         # Load Bill entry (replaced barcode)
#         load_frame = tk.Frame(left_frame, bg="white")
#         load_frame.pack(fill=tk.X, pady=5)
#         tk.Label(load_frame, text="Load Bill (Order #):", bg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
#         self.load_entry = tk.Entry(load_frame, font=("Arial", 12), bd=2, relief=tk.SUNKEN)
#         self.load_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
#         self.load_entry.bind('<Return>', lambda e: self.load_bill())
#         tk.Button(load_frame, text="Load", command=self.load_bill, bg="#0078D7", fg="white").pack(side=tk.LEFT, padx=5)

#         # User info display
#         info_frame = tk.Frame(left_frame, bg="#F0F0F0", bd=2, relief=tk.RIDGE)
#         info_frame.pack(fill=tk.X, pady=5, padx=5)
#         tk.Label(info_frame, text="Current Order #:", bg="#F0F0F0", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
#         self.order_lbl = tk.Label(info_frame, text=self.order_number, bg="#F0F0F0", font=("Arial", 10), fg="blue")
#         self.order_lbl.pack(side=tk.LEFT, padx=5)

#         # Billing Table
#         self.bill_table = ttk.Treeview(left_frame, columns=("name", "price", "qty", "total"), show="headings")
#         self.bill_table.heading("name", text="Item")
#         self.bill_table.heading("price", text="Price")
#         self.bill_table.heading("qty", text="Quantity")
#         self.bill_table.heading("total", text="Total")
#         self.bill_table.column("name", width=250)
#         self.bill_table.column("price", width=100)
#         self.bill_table.column("qty", width=80)
#         self.bill_table.column("total", width=100)
#         self.bill_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # Bind double-click on qty column
#         self.bill_table.bind('<Double-Button-1>', self.edit_quantity)

#         # Total section
#         totals_frame = tk.Frame(left_frame, bg="white", bd=2, relief=tk.RIDGE)
#         totals_frame.pack(fill=tk.X, pady=5)
#         self.total_lbl = tk.Label(totals_frame, text="Total: ₹0", font=("Arial", 12, "bold"), bg="white")
#         self.total_lbl.pack(side=tk.LEFT, padx=10)
#         self.tax_lbl = tk.Label(totals_frame, text="Tax: ₹0", font=("Arial", 12, "bold"), bg="white")
#         self.tax_lbl.pack(side=tk.LEFT, padx=10)
#         self.pay_lbl = tk.Label(totals_frame, text="Payable: ₹0", font=("Arial", 12, "bold"), bg="white")
#         self.pay_lbl.pack(side=tk.LEFT, padx=10)

#         # Buttons
#         btn_frame = tk.Frame(left_frame, bg="white")
#         btn_frame.pack(fill=tk.X, pady=5)
#         tk.Button(btn_frame, text="Payment", bg="green", fg="white", font=("Arial", 13, "bold"), width=10, command=self.make_payment).pack(side=tk.LEFT, padx=5)
#         tk.Button(btn_frame, text="Clear Cart", bg="orange", fg="white", font=("Arial", 13, "bold"), width=10, command=self.clear_cart).pack(side=tk.LEFT, padx=5)
#         tk.Button(btn_frame, text="View Bill", bg="purple", fg="white", font=("Arial", 13, "bold"), width=10, command=self.view_bill).pack(side=tk.LEFT, padx=5)
#         tk.Button(btn_frame, text="Download Bill", bg="#0078D7", fg="white", font=("Arial", 13, "bold"), width=10, command=self.download_bill).pack(side=tk.RIGHT, padx=5)

#         # ==================== RIGHT: PRODUCT & CATEGORY AREA ====================
#         right_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="#F7F7F7")
#         right_frame.place(x=720, y=10, width=470, height=630)

#         # User Name field
#         user_frame = tk.Frame(right_frame, bg="#F7F7F7")
#         user_frame.pack(fill=tk.X, pady=5)
#         tk.Label(user_frame, text="User Name:", bg="#F7F7F7", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
#         self.user_name_var = tk.StringVar()
#         tk.Entry(user_frame, textvariable=self.user_name_var, font=("Arial", 12), width=20).pack(side=tk.LEFT, padx=5)

#         # Search bar
#         search_frame = tk.Frame(right_frame, bg="#F7F7F7")
#         search_frame.pack(fill=tk.X, pady=5)
#         self.search_var = tk.StringVar()
#         tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=25).pack(side=tk.LEFT, padx=5)
#         tk.Button(search_frame, text="Search", bg="#0078D7", fg="white", command=self.search_item).pack(side=tk.LEFT)

#         # Right side split — vertical categories
#         split_frame = tk.Frame(right_frame, bg="#F7F7F7")
#         split_frame.pack(fill=tk.BOTH, expand=True, pady=5)

#         # Category buttons (vertical) - LEFT SIDE
#         cat_frame = tk.Frame(split_frame, bg="#CFE2F3", width=120)
#         cat_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        
#         # Add ALL button first
#         tk.Button(cat_frame, text="ALL", width=13, height=2, bg="#90EE90", font=("Arial", 9, "bold"), 
#                   command=lambda: self.load_items(None)).pack(pady=5, padx=5)
        
#         categories = self.get_categories()
#         for cat in categories:
#             tk.Button(cat_frame, text=cat, width=13, height=2, bg="#E0EAF3", 
#                       command=lambda c=cat: self.load_items(c)).pack(pady=5, padx=5)

#         # Product display with scrollbar - RIGHT SIDE
#         product_container = tk.Frame(split_frame, bg="#FFFFFF")
#         product_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
#         # Create canvas and scrollbar
#         self.product_canvas = tk.Canvas(product_container, bg="#FFFFFF", highlightthickness=0)
#         scrollbar = ttk.Scrollbar(product_container, orient="vertical", command=self.product_canvas.yview)
#         self.product_frame = tk.Frame(self.product_canvas, bg="#FFFFFF")
        
#         # Configure scrollbar
#         self.product_canvas.configure(yscrollcommand=scrollbar.set)
        
#         # Pack scrollbar and canvas
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#         self.product_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
#         # Create window in canvas
#         self.canvas_frame = self.product_canvas.create_window((0, 0), window=self.product_frame, anchor="nw")
        
#         # Bind configure event to update scroll region
#         self.product_frame.bind("<Configure>", self.on_frame_configure)
#         self.product_canvas.bind("<Configure>", self.on_canvas_configure)
        
#         # Bind mouse wheel events
#         self.product_canvas.bind("<Enter>", self.bind_mousewheel)
#         self.product_canvas.bind("<Leave>", self.unbind_mousewheel)
        
#         self.load_items()

#     # ==================== UTILITY FUNCTIONS ====================
#     def generate_order_number(self):
#         """Generate a unique 8-digit order number"""
#         return str(random.randint(10000000, 99999999))

#     # ==================== SCROLL FUNCTIONS ====================
#     def on_frame_configure(self, event=None):
#         """Update scroll region when frame size changes"""
#         self.product_canvas.configure(scrollregion=self.product_canvas.bbox("all"))
    
#     def on_canvas_configure(self, event):
#         """Update canvas window width when canvas is resized"""
#         canvas_width = event.width
#         self.product_canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
#     def bind_mousewheel(self, event):
#         """Bind mousewheel when mouse enters canvas"""
#         self.product_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    
#     def unbind_mousewheel(self, event):
#         """Unbind mousewheel when mouse leaves canvas"""
#         self.product_canvas.unbind_all("<MouseWheel>")
    
#     def on_mousewheel(self, event):
#         """Handle mouse wheel scrolling"""
#         self.product_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

#     # ==================== DATABASE FUNCTIONS ====================
#     def get_categories(self):
#         conn = sqlite3.connect('pos_database.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT DISTINCT category FROM products ORDER BY category')
#         categories = [row[0] for row in cursor.fetchall()]
#         conn.close()
#         return categories

#     def get_products(self, category=None):
#         conn = sqlite3.connect('pos_database.db')
#         cursor = conn.cursor()
#         if category:
#             cursor.execute('SELECT * FROM products WHERE category = ?', (category,))
#         else:
#             cursor.execute('SELECT * FROM products')
#         products = cursor.fetchall()
#         conn.close()
#         return products

#     def get_product_by_barcode(self, barcode):
#         conn = sqlite3.connect('pos_database.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM products WHERE barcode = ?', (barcode,))
#         product = cursor.fetchone()
#         conn.close()
#         return product

#     def update_product_qty(self, barcode, new_qty):
#         conn = sqlite3.connect('pos_database.db')
#         cursor = conn.cursor()
#         cursor.execute('UPDATE products SET qty = ? WHERE barcode = ?', (new_qty, barcode))
#         conn.commit()
#         conn.close()

#     def get_sale_by_order_number(self, order_number):
#         """Retrieve sale and its items by order number"""
#         conn = sqlite3.connect('pos_database.db')
#         cursor = conn.cursor()
        
#         # Get sale info
#         cursor.execute('SELECT * FROM sales WHERE order_number = ?', (order_number,))
#         sale = cursor.fetchone()
        
#         if sale:
#             sale_id = sale[0]
#             # Get sale items
#             cursor.execute('SELECT * FROM sale_items WHERE sale_id = ?', (sale_id,))
#             items = cursor.fetchall()
#             conn.close()
#             return sale, items
        
#         conn.close()
#         return None, None

#     # ==================== UI FUNCTIONS ====================
#     def load_items(self, category=None):
#         # Clear existing items
#         for widget in self.product_frame.winfo_children():
#             widget.destroy()

#         products = self.get_products(category)

#         for product in products:
#             product_id, barcode, name, qty, price, cat, image = product
#             frame = tk.Frame(self.product_frame, bd=2, relief=tk.RIDGE, bg="#FAFAFA")
#             frame.pack(fill=tk.X, pady=3, padx=5)

#             # Load image safely
#             try:
#                 img_path = os.path.join(os.path.dirname(__file__), "images", image)
#                 img = Image.open(img_path).resize((60, 60))
#                 photo = ImageTk.PhotoImage(img)
#             except Exception as e:
#                 img = Image.new("RGB", (60, 60), "gray")
#                 photo = ImageTk.PhotoImage(img)

#             img_label = tk.Label(frame, image=photo, bg="#FAFAFA")
#             img_label.image = photo
#             img_label.pack(side=tk.LEFT, padx=5)

#             # Info
#             info_frame = tk.Frame(frame, bg="#FAFAFA")
#             info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
#             tk.Label(info_frame, text=name, font=("Arial", 10, "bold"), bg="#FAFAFA").pack(anchor="w")
#             tk.Label(info_frame, text=f"₹{price} | Stock: {qty}", bg="#FAFAFA").pack(anchor="w")

#             # Add button
#             product_dict = {"barcode": barcode, "name": name, "price": price, "qty": qty}
#             tk.Button(frame, text="+", bg="lightgreen", command=lambda p=product_dict: self.add_to_cart(p)).pack(side=tk.RIGHT, padx=3)
#             tk.Button(frame, text="-", bg="lightcoral", command=lambda p=product_dict: self.remove_from_cart(p)).pack(side=tk.RIGHT, padx=3)
        
#         # Update scroll region after loading items
#         self.product_frame.update_idletasks()
#         self.product_canvas.configure(scrollregion=self.product_canvas.bbox("all"))

#     def add_to_cart(self, product):
#         for item in self.cart:
#             if item["name"] == product["name"]:
#                 item["qty"] += 1
#                 break
#         else:
#             self.cart.append({"barcode": product["barcode"], "name": product["name"], "price": product["price"], "qty": 1})
#         self.update_bill()

#     def remove_from_cart(self, product):
#         for item in self.cart:
#             if item["name"] == product["name"]:
#                 item["qty"] -= 1
#                 if item["qty"] <= 0:
#                     self.cart.remove(item)
#                 break
#         self.update_bill()

#     def edit_quantity(self, event):
#         """Edit quantity when double-clicking on qty column"""
#         region = self.bill_table.identify_region(event.x, event.y)
#         if region != "cell":
#             return
        
#         column = self.bill_table.identify_column(event.x)
#         row_id = self.bill_table.identify_row(event.y)
        
#         # Check if qty column (column #3)
#         if column == '#3' and row_id:
#             # Get current values
#             item_values = self.bill_table.item(row_id)['values']
#             item_name = item_values[0]
            
#             # Create entry widget for editing
#             x, y, width, height = self.bill_table.bbox(row_id, column)
            
#             entry = tk.Entry(self.bill_table, width=10)
#             entry.place(x=x, y=y, width=width, height=height)
#             entry.insert(0, item_values[2])
#             entry.focus()
#             entry.select_range(0, tk.END)
            
#             def save_edit(event=None):
#                 new_qty = entry.get()
#                 entry.destroy()
#                 try:
#                     new_qty = int(new_qty)
#                     if new_qty > 0:
#                         # Update cart
#                         for item in self.cart:
#                             if item["name"] == item_name:
#                                 item["qty"] = new_qty
#                                 break
#                         self.update_bill()
#                     elif new_qty == 0:
#                         # Remove item
#                         self.cart = [item for item in self.cart if item["name"] != item_name]
#                         self.update_bill()
#                     else:
#                         messagebox.showwarning("Invalid", "Quantity must be positive!")
#                 except ValueError:
#                     messagebox.showwarning("Invalid", "Please enter a valid number!")
            
#             entry.bind('<Return>', save_edit)
#             entry.bind('<FocusOut>', save_edit)

#     def update_bill(self):
#         for row in self.bill_table.get_children():
#             self.bill_table.delete(row)

#         total = 0
#         for item in self.cart:
#             total_item = item["price"] * item["qty"]
#             total += total_item
#             self.bill_table.insert("", "end", values=(item["name"], item["price"], item["qty"], total_item))

#         tax = total * 0.05
#         payable = total + tax
#         self.total_lbl.config(text=f"Total: ₹{total:.2f}")
#         self.tax_lbl.config(text=f"Tax: ₹{tax:.2f}")
#         self.pay_lbl.config(text=f"Payable: ₹{payable:.2f}")

#     def clear_cart(self):
#         self.cart.clear()
#         self.update_bill()
#         # Generate new order number for next purchase
#         self.order_number = self.generate_order_number()
#         self.order_lbl.config(text=self.order_number)

#     def make_payment(self):
#         if not self.cart:
#             messagebox.showwarning("Empty", "No items in cart!")
#             return
        
#         user_name = self.user_name_var.get().strip()
#         if not user_name:
#             messagebox.showwarning("User Name Required", "Please enter user name!")
#             return

#         # Calculate totals
#         total = sum(item["price"] * item["qty"] for item in self.cart)
#         tax = total * 0.05
#         payable = total + tax

#         conn = sqlite3.connect('pos_database.db')
#         cursor = conn.cursor()

#         try:
#             # Ensure unique order number (regenerate if duplicate)
#             while True:
#                 cursor.execute("SELECT 1 FROM sales WHERE order_number = ?", (self.order_number,))
#                 if cursor.fetchone() is None:
#                     break
#                 self.order_number = self.generate_order_number()
#                 self.order_lbl.config(text=self.order_number)

#             # Insert sale
#             cursor.execute('''
#                 INSERT INTO sales (order_number, user_name, sale_date, total, tax, payable)
#                 VALUES (?, ?, ?, ?, ?, ?)
#             ''', (self.order_number, user_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                   total, tax, payable))
            
#             sale_id = cursor.lastrowid

#             # Insert sale items
#             for item in self.cart:
#                 cursor.execute('''
#                     INSERT INTO sale_items (sale_id, product_name, price, qty, total)
#                     VALUES (?, ?, ?, ?, ?)
#                 ''', (sale_id, item["name"], item["price"], item["qty"], item["price"] * item["qty"]))

#             conn.commit()
#             messagebox.showinfo("Payment", f"Payment Successful ✅\nOrder #: {self.order_number}")
#             self.clear_cart()

#         except sqlite3.Error as e:
#             messagebox.showerror("Database Error", f"An error occurred while processing payment:\n{e}")

#         finally:
#             conn.close()


#     def view_bill(self):
#         """View current cart as a bill"""
#         if not self.cart:
#             messagebox.showwarning("Empty", "No items in cart to view!")
#             return
        
#         user_name = self.user_name_var.get().strip()
#         if not user_name:
#             messagebox.showwarning("User Name Required", "Please enter user name!")
#             return
        
#         # Create bill window
#         bill_window = tk.Toplevel(self.root)
#         bill_window.title("Bill Preview")
#         bill_window.geometry("500x600")
#         bill_window.config(bg="white")
        
#         # Bill content
#         content_frame = tk.Frame(bill_window, bg="white", padx=20, pady=20)
#         content_frame.pack(fill=tk.BOTH, expand=True)
        
#         # Header
#         tk.Label(content_frame, text="Smart POS Billing System", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
#         tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
#         # Order and user info
#         info_frame = tk.Frame(content_frame, bg="white")
#         info_frame.pack(fill=tk.X, pady=10)
#         tk.Label(info_frame, text=f"Order #: {self.order_number}", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
#         tk.Label(info_frame, text=f"User Name: {user_name}", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
#         tk.Label(info_frame, text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", font=("Arial", 11), bg="white").pack(anchor="w")
        
#         tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
#         # Items table
#         items_frame = tk.Frame(content_frame, bg="white")
#         items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
#         # Header
#         header_frame = tk.Frame(items_frame, bg="#E0E0E0")
#         header_frame.pack(fill=tk.X)
#         tk.Label(header_frame, text="Item", width=20, font=("Arial", 10, "bold"), bg="#E0E0E0", anchor="w").pack(side=tk.LEFT, padx=5)
#         tk.Label(header_frame, text="Price", width=8, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
#         tk.Label(header_frame, text="Qty", width=5, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
#         tk.Label(header_frame, text="Total", width=8, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
        
#         # Items
#         for item in self.cart:
#             item_frame = tk.Frame(items_frame, bg="white")
#             item_frame.pack(fill=tk.X, pady=2)
#             tk.Label(item_frame, text=item["name"], width=20, font=("Arial", 10), bg="white", anchor="w").pack(side=tk.LEFT, padx=5)
#             tk.Label(item_frame, text=f"₹{item['price']:.2f}", width=8, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
#             tk.Label(item_frame, text=str(item["qty"]), width=5, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
#             tk.Label(item_frame, text=f"₹{item['price'] * item['qty']:.2f}", width=8, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
        
#         tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
#         # Totals
#         total = sum(item["price"] * item["qty"] for item in self.cart)
#         tax = total * 0.05
#         payable = total + tax
        
#         totals_frame = tk.Frame(content_frame, bg="white")
#         totals_frame.pack(fill=tk.X, pady=10)
#         tk.Label(totals_frame, text=f"Subtotal: ₹{total:.2f}", font=("Arial", 11, "bold"), bg="white").pack(anchor="e")
#         tk.Label(totals_frame, text=f"Tax (5%): ₹{tax:.2f}", font=("Arial", 11, "bold"), bg="white").pack(anchor="e")
#         tk.Label(totals_frame, text=f"Total Payable: ₹{payable:.2f}", font=("Arial", 13, "bold"), bg="white", fg="green").pack(anchor="e")
        
#         tk.Label(content_frame, text="=" * 50, bg="white").pack()
#         tk.Label(content_frame, text="Thank you for your business!", font=("Arial", 10, "italic"), bg="white").pack(pady=10)

#     def load_bill(self):
#         """Load a previous bill by order number"""
#         order_number = self.load_entry.get().strip()
#         if not order_number:
#             messagebox.showwarning("Order Number Required", "Please enter order number!")
#             return
        
#         sale, items = self.get_sale_by_order_number(order_number)
        
#         if not sale:
#             messagebox.showinfo("Not Found", "Order number not found!")
#             return
        
#         # Create bill window
#         bill_window = tk.Toplevel(self.root)
#         bill_window.title(f"Bill - Order #{order_number}")
#         bill_window.geometry("500x600")
#         bill_window.config(bg="white")
        
#         # Bill content
#         content_frame = tk.Frame(bill_window, bg="white", padx=20, pady=20)
#         content_frame.pack(fill=tk.BOTH, expand=True)
        
#         # Header
#         tk.Label(content_frame, text="Smart POS Billing System", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
#         tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
#         # Order and user info
#         sale_id, order_num, user_name, sale_date, total, tax, payable = sale
#         info_frame = tk.Frame(content_frame, bg="white")
#         info_frame.pack(fill=tk.X, pady=10)
#         tk.Label(info_frame, text=f"Order #: {order_num}", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
#         tk.Label(info_frame, text=f"User Name: {user_name}", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
#         tk.Label(info_frame, text=f"Date: {sale_date}", font=("Arial", 11), bg="white").pack(anchor="w")
        
#         tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
#         # # Items table
#         # items_frame = tk.

#          # Items table
#         items_frame = tk.Frame(content_frame, bg="white")
#         items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
#         # Header
#         header_frame = tk.Frame(items_frame, bg="#E0E0E0")
#         header_frame.pack(fill=tk.X)
#         tk.Label(header_frame, text="Item", width=20, font=("Arial", 10, "bold"), bg="#E0E0E0", anchor="w").pack(side=tk.LEFT, padx=5)
#         tk.Label(header_frame, text="Price", width=8, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
#         tk.Label(header_frame, text="Qty", width=5, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
#         tk.Label(header_frame, text="Total", width=8, font=("Arial", 10, "bold"), bg="#E0E0E0").pack(side=tk.LEFT)
        
#         # Items
#         for item in items:
#             item_id, sale_id_fk, product_name, price, qty, item_total = item
#             item_frame = tk.Frame(items_frame, bg="white")
#             item_frame.pack(fill=tk.X, pady=2)
#             tk.Label(item_frame, text=product_name, width=20, font=("Arial", 10), bg="white", anchor="w").pack(side=tk.LEFT, padx=5)
#             tk.Label(item_frame, text=f"₹{price:.2f}", width=8, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
#             tk.Label(item_frame, text=str(qty), width=5, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
#             tk.Label(item_frame, text=f"₹{item_total:.2f}", width=8, font=("Arial", 10), bg="white").pack(side=tk.LEFT)
        
#         tk.Label(content_frame, text="=" * 50, bg="white").pack()
        
#         # Totals
#         totals_frame = tk.Frame(content_frame, bg="white")
#         totals_frame.pack(fill=tk.X, pady=10)
#         tk.Label(totals_frame, text=f"Subtotal: ₹{total:.2f}", font=("Arial", 11, "bold"), bg="white").pack(anchor="e")
#         tk.Label(totals_frame, text=f"Tax (5%): ₹{tax:.2f}", font=("Arial", 11, "bold"), bg="white").pack(anchor="e")
#         tk.Label(totals_frame, text=f"Total Payable: ₹{payable:.2f}", font=("Arial", 13, "bold"), bg="white", fg="green").pack(anchor="e")
        
#         tk.Label(content_frame, text="=" * 50, bg="white").pack()
#         tk.Label(content_frame, text="Thank you for your business!", font=("Arial", 10, "italic"), bg="white").pack(pady=10)
        
#         self.load_entry.delete(0, tk.END)

#     def download_bill(self):
#         if not self.cart:
#             messagebox.showwarning("Empty", "No items to download!")
#             return
        
#         user_name = self.user_name_var.get().strip()
#         if not user_name:
#             messagebox.showwarning("User Name Required", "Please enter user name!")
#             return
        
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".pdf", 
#             filetypes=[("PDF File", "*.pdf"), ("Text File", "*.txt")]
#         )
        
#         if not file_path:
#             return
        
#         if file_path.endswith('.pdf'):
#             self.generate_pdf_bill(file_path, user_name)
#         else:
#             self.generate_text_bill(file_path, user_name)

#     def generate_pdf_bill(self, file_path, user_name):
#         """Generate PDF bill using ReportLab"""
#         doc = SimpleDocTemplate(file_path, pagesize=letter)
#         elements = []
#         styles = getSampleStyleSheet()
        
#         # Title
#         title = Paragraph("<b>Smart POS Billing System</b>", styles['Title'])
#         elements.append(title)
#         elements.append(Spacer(1, 0.2*inch))
        
#         # Order and User info
#         order_info = Paragraph(f"<b>Order Number:</b> {self.order_number}", styles['Normal'])
#         elements.append(order_info)
#         user_info = Paragraph(f"<b>User Name:</b> {user_name}", styles['Normal'])
#         elements.append(user_info)
#         date_text = Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
#         elements.append(date_text)
#         elements.append(Spacer(1, 0.3*inch))
        
#         # Table data
#         data = [['Item', 'Price', 'Qty', 'Total']]
#         total = 0
        
#         for item in self.cart:
#             total_item = item["price"] * item["qty"]
#             total += total_item
#             data.append([
#                 item["name"],
#                 f"₹{item['price']:.2f}",
#                 str(item["qty"]),
#                 f"₹{total_item:.2f}"
#             ])
        
#         # Create table
#         table = Table(data, colWidths=[3*inch, 1.5*inch, 1*inch, 1.5*inch])
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('FONTSIZE', (0, 0), (-1, 0), 12),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#             ('FONTSIZE', (0, 1), (-1, -1), 10),
#         ]))
        
#         elements.append(table)
#         elements.append(Spacer(1, 0.3*inch))
        
#         # Totals
#         tax = total * 0.05
#         payable = total + tax
        
#         totals_data = [
#             ['', '', 'Subtotal:', f"₹{total:.2f}"],
#             ['', '', 'Tax (5%):', f"₹{tax:.2f}"],
#             ['', '', 'Total Payable:', f"₹{payable:.2f}"]
#         ]
        
#         totals_table = Table(totals_data, colWidths=[3*inch, 1.5*inch, 1*inch, 1.5*inch])
#         totals_table.setStyle(TableStyle([
#             ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
#             ('FONTNAME', (2, 0), (-1, -1), 'Helvetica-Bold'),
#             ('FONTSIZE', (2, 0), (-1, -1), 11),
#             ('LINEABOVE', (2, 0), (-1, 0), 1, colors.black),
#             ('LINEABOVE', (2, 2), (-1, 2), 2, colors.black),
#         ]))
        
#         elements.append(totals_table)
#         elements.append(Spacer(1, 0.5*inch))
        
#         # Footer
#         footer = Paragraph("<i>Thank you for your business!</i>", styles['Normal'])
#         elements.append(footer)
        
#         # Build PDF
#         doc.build(elements)
#         messagebox.showinfo("Downloaded", "PDF Bill saved successfully ✅")

#     def generate_text_bill(self, file_path, user_name):
#         """Generate text bill"""
#         with open(file_path, "w") as f:
#             f.write("======== Smart POS Bill ========\n")
#             f.write(f"Order Number: {self.order_number}\n")
#             f.write(f"User Name: {user_name}\n")
#             f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
#             f.write("----------------------------------\n")
#             f.write("{:<20}{:<10}{:<10}{:<10}\n".format("Item", "Price", "Qty", "Total"))
#             f.write("----------------------------------\n")
#             total = 0
#             for item in self.cart:
#                 total_item = item["price"] * item["qty"]
#                 total += total_item
#                 f.write(f"{item['name']:<20}{item['price']:<10}{item['qty']:<10}{total_item:<10}\n")
#             f.write("----------------------------------\n")
#             f.write(f"Total: ₹{total:.2f}\nTax: ₹{total*0.05:.2f}\nPayable: ₹{total*1.05:.2f}\n")
#             f.write("==================================\n")
#         messagebox.showinfo("Downloaded", "Bill saved successfully ✅")

#     def search_item(self):
#         query = self.search_var.get().lower()
#         if query:
#             conn = sqlite3.connect('pos_database.db')
#             cursor = conn.cursor()
#             cursor.execute('SELECT * FROM products WHERE LOWER(name) LIKE ?', (f'%{query}%',))
#             filtered = cursor.fetchall()
#             conn.close()
            
#             if filtered:
#                 self.show_filtered_items(filtered)
#             else:
#                 messagebox.showinfo("Not Found", "No matching items found.")
#         else:
#             self.load_items()

#     def show_filtered_items(self, filtered):
#         for widget in self.product_frame.winfo_children():
#             widget.destroy()
        
#         for product in filtered:
#             product_id, barcode, name, qty, price, cat, image = product
#             frame = tk.Frame(self.product_frame, bd=2, relief=tk.RIDGE, bg="#FAFAFA")
#             frame.pack(fill=tk.X, pady=3, padx=5)
            
#             # Load image safely
#             try:
#                 img_path = os.path.join(os.path.dirname(__file__), "images", image)
#                 img = Image.open(img_path).resize((60, 60))
#                 photo = ImageTk.PhotoImage(img)
#             except Exception as e:
#                 img = Image.new("RGB", (60, 60), "gray")
#                 photo = ImageTk.PhotoImage(img)

#             img_label = tk.Label(frame, image=photo, bg="#FAFAFA")
#             img_label.image = photo
#             img_label.pack(side=tk.LEFT, padx=5)
            
#             # Info
#             info_frame = tk.Frame(frame, bg="#FAFAFA")
#             info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
#             tk.Label(info_frame, text=name, font=("Arial", 10, "bold"), bg="#FAFAFA").pack(anchor="w")
#             tk.Label(info_frame, text=f"₹{price} | Stock: {qty}", bg="#FAFAFA").pack(anchor="w")
            
#             product_dict = {"barcode": barcode, "name": name, "price": price, "qty": qty}
#             tk.Button(frame, text="+", bg="lightgreen", command=lambda p=product_dict: self.add_to_cart(p)).pack(side=tk.RIGHT, padx=5)
        
#         # Update scroll region after loading filtered items
#         self.product_frame.update_idletasks()
#         self.product_canvas.configure(scrollregion=self.product_canvas.bbox("all"))

# # ==================== Run App ====================
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = POSApp(root)
#     root.mainloop()