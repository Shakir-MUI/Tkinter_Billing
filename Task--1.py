import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

# ==================== Database Setup ====================
def init_database():
    conn = sqlite3.connect('pos_database.db')
    cursor = conn.cursor()
    
    # Create products table
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
    
    # Create sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT NOT NULL,
            total REAL NOT NULL,
            tax REAL NOT NULL,
            payable REAL NOT NULL
        )
    ''')
    
    # Create sale_items table
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
    
    # Check if products table is empty
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        # Insert initial products
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
    
    conn.commit()
    conn.close()

# ==================== POS Application ====================
class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart POS Billing System")
        self.root.geometry("1200x650")
        self.root.config(bg="#E9E9E9")

        self.cart = []
        init_database()

        # ==================== LEFT: BILL AREA ====================
        left_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="white")
        left_frame.place(x=10, y=10, width=700, height=630)

        # Barcode entry
        barcode_frame = tk.Frame(left_frame, bg="white")
        barcode_frame.pack(fill=tk.X, pady=5)
        tk.Label(barcode_frame, text="Insert Barcode:", bg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.barcode_entry = tk.Entry(barcode_frame, font=("Arial", 12), bd=2, relief=tk.SUNKEN)
        self.barcode_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.barcode_entry.bind('<Return>', lambda e: self.search_barcode())
        tk.Button(barcode_frame, text="Search", command=self.search_barcode, bg="#0078D7", fg="white").pack(side=tk.LEFT, padx=5)

        # Billing Table
        self.bill_table = ttk.Treeview(left_frame, columns=("name", "price", "qty", "total"), show="headings")
        self.bill_table.heading("name", text="Item")
        self.bill_table.heading("price", text="Price")
        self.bill_table.heading("qty", text="Qty")
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
        tk.Button(btn_frame, text="Payment", bg="green", fg="white", font=("Arial", 13, "bold"), width=13, command=self.make_payment).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear Cart", bg="orange", fg="white", font=("Arial", 13, "bold"), width=13, command=self.clear_cart).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Download Bill", bg="#0078D7", fg="white", font=("Arial", 13, "bold"), width=13, command=self.download_bill).pack(side=tk.RIGHT, padx=5)

        # ==================== RIGHT: PRODUCT & CATEGORY AREA ====================
        right_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="#F7F7F7")
        right_frame.place(x=720, y=10, width=470, height=630)

        # Search bar
        search_frame = tk.Frame(right_frame, bg="#F7F7F7")
        search_frame.pack(fill=tk.X, pady=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=25).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", bg="#0078D7", fg="white", command=self.search_item).pack(side=tk.LEFT)

        # Right side split — vertical categories
        split_frame = tk.Frame(right_frame, bg="#F7F7F7")
        split_frame.pack(fill=tk.BOTH, expand=True)

        # Category buttons (vertical)
        cat_frame = tk.Frame(split_frame, bg="#CFE2F3", width=120)
        cat_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add ALL button first
        tk.Button(cat_frame, text="ALL", width=13, height=2, bg="#90EE90", font=("Arial", 9, "bold"), 
                  command=lambda: self.load_items(None)).pack(pady=5, padx=5)
        
        categories = self.get_categories()
        for cat in categories:
            tk.Button(cat_frame, text=cat, width=13, height=2, bg="#E0EAF3", 
                      command=lambda c=cat: self.load_items(c)).pack(pady=5, padx=5)

        # Product display
        self.product_frame = tk.Frame(split_frame, bg="#FFFFFF")
        self.product_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.load_items()

    # ==================== DATABASE FUNCTIONS ====================
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.product_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
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



        # def _on_mousewheel(self, event):
#         """Handle mouse wheel scrolling"""
#         self.product_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
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

    # ==================== UI FUNCTIONS ====================
    def load_items(self, category=None):
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

            img_label = tk.Label(frame, image=photo)
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

    def make_payment(self):
        if not self.cart:
            messagebox.showwarning("Empty", "No items in cart!")
            return
        
        # Save sale to database
        total = sum(item["price"] * item["qty"] for item in self.cart)
        tax = total * 0.05
        payable = total + tax
        
        conn = sqlite3.connect('pos_database.db')
        cursor = conn.cursor()
        
        # Insert sale
        cursor.execute('''
            INSERT INTO sales (sale_date, total, tax, payable)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total, tax, payable))
        
        sale_id = cursor.lastrowid
        
        # Insert sale items
        for item in self.cart:
            cursor.execute('''
                INSERT INTO sale_items (sale_id, product_name, price, qty, total)
                VALUES (?, ?, ?, ?, ?)
            ''', (sale_id, item["name"], item["price"], item["qty"], item["price"] * item["qty"]))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Payment", "Payment Successful ✅")
        self.clear_cart()

    def download_bill(self):
        if not self.cart:
            messagebox.showwarning("Empty", "No items to download!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            filetypes=[("PDF File", "*.pdf"), ("Text File", "*.txt")]
        )
        
        if not file_path:
            return
        
        if file_path.endswith('.pdf'):
            self.generate_pdf_bill(file_path)
        else:
            self.generate_text_bill(file_path)

    def generate_pdf_bill(self, file_path):
        """Generate PDF bill using ReportLab"""
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph("<b>Smart POS Billing System</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Date and Time
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

    def generate_text_bill(self, file_path):
        """Generate text bill"""
        with open(file_path, "w") as f:
            f.write("======== Smart POS Bill ========\n")
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

    def search_barcode(self):
        code = self.barcode_entry.get().strip()
        if not code:
            return
        
        product = self.get_product_by_barcode(code)
        if product:
            product_id, barcode, name, qty, price, cat, image = product
            product_dict = {"barcode": barcode, "name": name, "price": price, "qty": qty}
            self.add_to_cart(product_dict)
            self.barcode_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Not Found", "Barcode not found!")

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
            tk.Label(frame, text=name, font=("Arial", 10, "bold"), bg="#FAFAFA").pack(side=tk.LEFT, padx=10)
            tk.Label(frame, text=f"₹{price} | Stock: {qty}", bg="#FAFAFA").pack(side=tk.LEFT, padx=10)
            product_dict = {"barcode": barcode, "name": name, "price": price, "qty": qty}
            tk.Button(frame, text="+", bg="lightgreen", command=lambda p=product_dict: self.add_to_cart(p)).pack(side=tk.RIGHT, padx=5)

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
# from datetime import datetime
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# from reportlab.lib.units import inch

# # ==================== Database Setup ====================
# def init_database():
#     conn = sqlite3.connect('pos_database.db')
#     cursor = conn.cursor()
    
#     # Create products table
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
    
#     # Create sales table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS sales (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             sale_date TEXT NOT NULL,
#             total REAL NOT NULL,
#             tax REAL NOT NULL,
#             payable REAL NOT NULL
#         )
#     ''')
    
#     # Create sale_items table
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
    
#     # Check if products table is empty
#     cursor.execute('SELECT COUNT(*) FROM products')
#     if cursor.fetchone()[0] == 0:
#         # Insert initial products
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
    
#     conn.commit()
#     conn.close()

# # ==================== POS Application ====================
# class POSApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Smart POS Billing System")
#         self.root.geometry("1200x650")
#         self.root.config(bg="#E9E9E9")

#         self.cart = []
#         init_database()

#         # ==================== LEFT: BILL AREA ====================
#         left_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="white")
#         left_frame.place(x=10, y=10, width=700, height=630)

#         # Barcode entry
#         barcode_frame = tk.Frame(left_frame, bg="white")
#         barcode_frame.pack(fill=tk.X, pady=5)
#         tk.Label(barcode_frame, text="Insert Barcode:", bg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
#         self.barcode_entry = tk.Entry(barcode_frame, font=("Arial", 12), bd=2, relief=tk.SUNKEN)
#         self.barcode_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
#         self.barcode_entry.bind('<Return>', lambda e: self.search_barcode())
#         tk.Button(barcode_frame, text="Search", command=self.search_barcode, bg="#0078D7", fg="white").pack(side=tk.LEFT, padx=5)

#         # Billing Table
#         self.bill_table = ttk.Treeview(left_frame, columns=("name", "price", "qty", "total"), show="headings")
#         self.bill_table.heading("name", text="Item")
#         self.bill_table.heading("price", text="Price")
#         self.bill_table.heading("qty", text="Qty")
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
#         tk.Button(btn_frame, text="Payment", bg="green", fg="white", font=("Arial", 13, "bold"), width=13, command=self.make_payment).pack(side=tk.LEFT, padx=5)
#         tk.Button(btn_frame, text="Clear Cart", bg="orange", fg="white", font=("Arial", 13, "bold"), width=13, command=self.clear_cart).pack(side=tk.LEFT, padx=5)
#         tk.Button(btn_frame, text="Download Bill", bg="#0078D7", fg="white", font=("Arial", 13, "bold"), width=13, command=self.download_bill).pack(side=tk.RIGHT, padx=5)

#         # ==================== RIGHT: PRODUCT & CATEGORY AREA ====================
#         right_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="#F7F7F7")
#         right_frame.place(x=720, y=10, width=470, height=630)

#         # Search bar
#         search_frame = tk.Frame(right_frame, bg="#F7F7F7")
#         search_frame.pack(fill=tk.X, pady=5)
#         self.search_var = tk.StringVar()
#         tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=25).pack(side=tk.LEFT, padx=5)
#         tk.Button(search_frame, text="Search", bg="#0078D7", fg="white", command=self.search_item).pack(side=tk.LEFT)

#         # Right side split — vertical categories
#         split_frame = tk.Frame(right_frame, bg="#F7F7F7")
#         split_frame.pack(fill=tk.BOTH, expand=True)

#         # Category buttons (vertical)
#         cat_frame = tk.Frame(split_frame, bg="#CFE2F3", width=120)
#         cat_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
#         # Add ALL button first
#         tk.Button(cat_frame, text="ALL", width=13, height=2, bg="#90EE90", font=("Arial", 9, "bold"), 
#                   command=lambda: self.load_items(None)).pack(pady=5, padx=5)
        
#         categories = self.get_categories()
#         for cat in categories:
#             tk.Button(cat_frame, text=cat, width=13, height=2, bg="#E0EAF3", 
#                       command=lambda c=cat: self.load_items(c)).pack(pady=5, padx=5)

#         # Product display with scrollbar
#         product_container = tk.Frame(split_frame, bg="#FFFFFF")
#         product_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
#         # Create canvas and scrollbar
#         self.product_canvas = tk.Canvas(product_container, bg="#FFFFFF", highlightthickness=0)
#         scrollbar = ttk.Scrollbar(product_container, orient="vertical", command=self.product_canvas.yview)
#         self.product_frame = tk.Frame(self.product_canvas, bg="#FFFFFF")
        
#         self.product_frame.bind(
#             "<Configure>",
#             lambda e: self.product_canvas.configure(scrollregion=self.product_canvas.bbox("all"))
#         )
        
#         self.product_canvas.create_window((0, 0), window=self.product_frame, anchor="nw")
#         self.product_canvas.configure(yscrollcommand=scrollbar.set)
        
#         self.product_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
#         # Bind mouse wheel to canvas
#         self.product_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
#         self.load_items()

#     # ==================== DATABASE FUNCTIONS ====================
#     def _on_mousewheel(self, event):
#         """Handle mouse wheel scrolling"""
#         self.product_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
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

#     # ==================== UI FUNCTIONS ====================
#     def load_items(self, category=None):
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

#             img_label = tk.Label(frame, image=photo)
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

#     def make_payment(self):
#         if not self.cart:
#             messagebox.showwarning("Empty", "No items in cart!")
#             return
        
#         # Save sale to database
#         total = sum(item["price"] * item["qty"] for item in self.cart)
#         tax = total * 0.05
#         payable = total + tax
        
#         conn = sqlite3.connect('pos_database.db')
#         cursor = conn.cursor()
        
#         # Insert sale
#         cursor.execute('''
#             INSERT INTO sales (sale_date, total, tax, payable)
#             VALUES (?, ?, ?, ?)
#         ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total, tax, payable))
        
#         sale_id = cursor.lastrowid
        
#         # Insert sale items
#         for item in self.cart:
#             cursor.execute('''
#                 INSERT INTO sale_items (sale_id, product_name, price, qty, total)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (sale_id, item["name"], item["price"], item["qty"], item["price"] * item["qty"]))
        
#         conn.commit()
#         conn.close()
        
#         messagebox.showinfo("Payment", "Payment Successful ✅")
#         self.clear_cart()

#     def download_bill(self):
#         if not self.cart:
#             messagebox.showwarning("Empty", "No items to download!")
#             return
        
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".pdf", 
#             filetypes=[("PDF File", "*.pdf"), ("Text File", "*.txt")]
#         )
        
#         if not file_path:
#             return
        
#         if file_path.endswith('.pdf'):
#             self.generate_pdf_bill(file_path)
#         else:
#             self.generate_text_bill(file_path)

#     def generate_pdf_bill(self, file_path):
#         """Generate PDF bill using ReportLab"""
#         doc = SimpleDocTemplate(file_path, pagesize=letter)
#         elements = []
#         styles = getSampleStyleSheet()
        
#         # Title
#         title = Paragraph("<b>Smart POS Billing System</b>", styles['Title'])
#         elements.append(title)
#         elements.append(Spacer(1, 0.2*inch))
        
#         # Date and Time
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

#     def generate_text_bill(self, file_path):
#         """Generate text bill"""
#         with open(file_path, "w") as f:
#             f.write("======== Smart POS Bill ========\n")
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

#     def search_barcode(self):
#         code = self.barcode_entry.get().strip()
#         if not code:
#             return
        
#         product = self.get_product_by_barcode(code)
#         if product:
#             product_id, barcode, name, qty, price, cat, image = product
#             product_dict = {"barcode": barcode, "name": name, "price": price, "qty": qty}
#             self.add_to_cart(product_dict)
#             self.barcode_entry.delete(0, tk.END)
#         else:
#             messagebox.showinfo("Not Found", "Barcode not found!")

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
#             tk.Label(frame, text=name, font=("Arial", 10, "bold"), bg="#FAFAFA").pack(side=tk.LEFT, padx=10)
#             tk.Label(frame, text=f"₹{price} | Stock: {qty}", bg="#FAFAFA").pack(side=tk.LEFT, padx=10)
#             product_dict = {"barcode": barcode, "name": name, "price": price, "qty": qty}
#             tk.Button(frame, text="+", bg="lightgreen", command=lambda p=product_dict: self.add_to_cart(p)).pack(side=tk.RIGHT, padx=5)

# # ==================== Run App ====================
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = POSApp(root)
#     root.mainloop()