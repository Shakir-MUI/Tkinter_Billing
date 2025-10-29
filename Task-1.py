# import tkinter as tk
# from tkinter import ttk, messagebox
# from PIL import Image, ImageTk

# # ------------------------------------------------
# # Tkinter Window Setup
# # ------------------------------------------------
# root = tk.Tk()
# root.title("POS Billing System")
# root.geometry("1200x600")
# root.config(bg="#f3f3f3")

# # ------------------------------------------------
# # Left Frame (Billing Area)
# # ------------------------------------------------
# left_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
# left_frame.place(x=10, y=10, width=550, height=580)

# title_lbl = tk.Label(left_frame, text="Insert Barcode", font=("Arial", 13, "bold"), bg="white")
# title_lbl.pack(anchor="nw", padx=10, pady=5)

# # Treeview for items
# columns = ("Items", "Price", "Qty", "Total", "Tax", "Comment")
# tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
# for col in columns:
#     tree.heading(col, text=col)
#     tree.column(col, width=80, anchor="center")
# tree.pack(padx=10, pady=10)

# # Billing summary frame
# bill_frame = tk.Frame(left_frame, bg="white")
# bill_frame.pack(fill="both", expand=True, padx=10)

# labels = [
#     ("Total", "00"),
#     ("Discount", "00"),
#     ("Sub Total", "00"),
#     ("Tax", "00"),
#     ("Total Payable", "00"),
# ]
# bill_vars = {}

# for i, (label, value) in enumerate(labels):
#     tk.Label(bill_frame, text=label, font=("Arial", 10, "bold"), bg="white").grid(row=i, column=0, sticky="w", pady=2)
#     var = tk.StringVar(value=value)
#     bill_vars[label] = var
#     tk.Label(bill_frame, textvariable=var, font=("Arial", 10), bg="white").grid(row=i, column=1, sticky="e")

# # Buttons
# bottom_frame = tk.Frame(left_frame, bg="white")
# bottom_frame.pack(side="bottom", fill="x", pady=10)

# tk.Button(bottom_frame, text="Payment", bg="green", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="left", padx=20)
# tk.Button(bottom_frame, text="Suspend", bg="orange", fg="white", font=("Arial", 12, "bold"), width=15).pack(side="right", padx=20)

# # ------------------------------------------------
# # Right Frame (Categories & Items)
# # ------------------------------------------------
# right_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
# right_frame.place(x=570, y=10, width=620, height=580)

# # Search Bar
# search_frame = tk.Frame(right_frame, bg="white")
# search_frame.pack(fill="x", pady=5)
# tk.Label(search_frame, text="Search:", font=("Arial", 12, "bold"), bg="white").pack(side="left", padx=5)
# search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
# search_entry.pack(side="left", padx=5)

# # Category Buttons
# cat_frame = tk.Frame(right_frame, bg="white")
# cat_frame.pack(fill="x", pady=10)

# categories = ["SoftDrink", "Food", "Burger", "CoolDrink", "Cigarettes", "Fruit", "Drink", "Soft_Drink", "Coffee"]

# for cat in categories:
#     tk.Button(cat_frame, text=cat, width=10, height=1, bg="#d1f0d1", font=("Arial", 10, "bold")).pack(side="left", padx=4, pady=4)

# # ------------------------------------------------
# # Item List with Images
# # ------------------------------------------------
# item_frame = tk.Frame(right_frame, bg="white")
# item_frame.pack(fill="both", expand=True, padx=10, pady=10)

# canvas = tk.Canvas(item_frame, bg="white")
# scrollbar = ttk.Scrollbar(item_frame, orient="vertical", command=canvas.yview)
# scroll_frame = tk.Frame(canvas, bg="white")

# scroll_frame.bind(
#     "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
# )

# canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
# canvas.configure(yscrollcommand=scrollbar.set)
# canvas.pack(side="left", fill="both", expand=True)
# scrollbar.pack(side="right", fill="y")

# # Sample product data
# products = [
#     ("Milk 370ml", "milk.png", 54.9),
#     ("Grapes 1B", "grapes.png", 2.99),
#     ("Mr. Chicken SM", "chicken.png", 15),
#     ("Apple 400gm", "apple.png", 24),
#     ("Coffee Milk", "coffee.png", 2.49),
#     ("Strawberry 400gm", "strawberry.png", 125),
#     ("Mountain Dew 770ml", "dew.png", 5),
#     ("Water 500ml", "water.png", 100),
#     ("Chicken Bhona", "chicken2.png", 125),
# ]

# # Load product cards
# images = []  # keep reference to avoid garbage collection
# for name, img_file, price in products:
#     try:
#         img = Image.open(img_file)
#         img = img.resize((70, 70))
#         photo = ImageTk.PhotoImage(img)
#     except:
#         # fallback placeholder
#         img = Image.new("RGB", (70, 70), "gray")
#         photo = ImageTk.PhotoImage(img)
#     images.append(photo)

#     frame = tk.Frame(scroll_frame, bg="#f8f8f8", bd=1, relief="solid", padx=10, pady=5)
#     frame.pack(fill="x", pady=5)

#     tk.Label(frame, image=photo, bg="#f8f8f8").pack(side="left", padx=5)
#     tk.Label(frame, text=f"{name}\nPrice: ₹{price}", font=("Arial", 11), bg="#f8f8f8", justify="left").pack(side="left", padx=10)

# root.mainloop()










# import tkinter as tk
# from tkinter import ttk, messagebox
# from PIL import Image, ImageTk

# # Sample Product Data
# products = {
#     "SoftDrink": [
#         {"name": "Mountain Dew 770ml", "price": 55},
#         {"name": "Pepsi 500ml", "price": 40},
#     ],
#     "Food": [
#         {"name": "Chicken Bhuna", "price": 125},
#         {"name": "Mr. Chicken SM", "price": 150},
#     ],
#     "Fruit": [
#         {"name": "Apple", "price": 22},
#         {"name": "Grapes", "price": 99},
#     ]
# }

# class POSApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Point of Sale System")
#         self.root.geometry("1100x600")
#         self.cart = []

#         # ===== LEFT BILLING FRAME =====
#         left_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="white")
#         left_frame.place(x=10, y=10, width=650, height=580)

#         title = tk.Label(left_frame, text="BILLING SYSTEM", font=("Arial", 16, "bold"), bg="white")
#         title.pack(side=tk.TOP, fill=tk.X)

#         # Treeview for Bill Items
#         self.bill_table = ttk.Treeview(left_frame, columns=("name", "price", "qty", "total"), show="headings")
#         self.bill_table.heading("name", text="Item")
#         self.bill_table.heading("price", text="Price")
#         self.bill_table.heading("qty", text="Qty")
#         self.bill_table.heading("total", text="Total")
#         self.bill_table.pack(fill=tk.BOTH, expand=1)

#         # Billing Summary
#         summary_frame = tk.Frame(left_frame, bg="white", bd=2, relief=tk.RIDGE)
#         summary_frame.pack(fill=tk.X)

#         self.total_lbl = tk.Label(summary_frame, text="Total: 0", font=("Arial", 12, "bold"), bg="white")
#         self.total_lbl.pack(side=tk.LEFT, padx=10, pady=5)

#         self.tax_lbl = tk.Label(summary_frame, text="Tax (5%): 0", font=("Arial", 12, "bold"), bg="white")
#         self.tax_lbl.pack(side=tk.LEFT, padx=10)

#         self.grand_lbl = tk.Label(summary_frame, text="Grand Total: 0", font=("Arial", 12, "bold"), bg="white")
#         self.grand_lbl.pack(side=tk.LEFT, padx=10)

#         btn_frame = tk.Frame(left_frame, bg="white")
#         btn_frame.pack(fill=tk.X, pady=10)

#         tk.Button(btn_frame, text="Payment", bg="green", fg="white", font=("Arial", 12, "bold"),
#                   command=self.make_payment).pack(side=tk.LEFT, padx=20)
#         tk.Button(btn_frame, text="Suspend", bg="orange", fg="white", font=("Arial", 12, "bold"),
#                   command=self.clear_cart).pack(side=tk.RIGHT, padx=20)

#         # ===== RIGHT PRODUCT FRAME =====
#         right_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE)
#         right_frame.place(x=670, y=10, width=420, height=580)

#         tk.Label(right_frame, text="Select Category:", font=("Arial", 13, "bold")).pack(pady=5)
#         self.category_var = tk.StringVar(value="SoftDrink")
#         category_menu = ttk.Combobox(right_frame, textvariable=self.category_var, values=list(products.keys()), state="readonly")
#         category_menu.pack(pady=5)
#         category_menu.bind("<<ComboboxSelected>>", self.load_items)

#         self.items_frame = tk.Frame(right_frame)
#         self.items_frame.pack(fill=tk.BOTH, expand=1)

#         self.load_items()

#     def load_items(self, event=None):
#         for widget in self.items_frame.winfo_children():
#             widget.destroy()

#         category = self.category_var.get()
#         for item in products[category]:
#             btn = tk.Button(self.items_frame, text=f"{item['name']}\n₹{item['price']}",
#                             width=25, height=2, bg="#cdeefc",
#                             command=lambda i=item: self.add_to_cart(i))
#             btn.pack(pady=3)

#     def add_to_cart(self, item):
#         for i in self.cart:
#             if i['name'] == item['name']:
#                 i['qty'] += 1
#                 break
#         else:
#             self.cart.append({"name": item['name'], "price": item['price'], "qty": 1})

#         self.update_bill()

#     def update_bill(self):
#         for row in self.bill_table.get_children():
#             self.bill_table.delete(row)

#         total = 0
#         for item in self.cart:
#             item_total = item['price'] * item['qty']
#             total += item_total
#             self.bill_table.insert("", "end", values=(item['name'], item['price'], item['qty'], item_total))

#         tax = total * 0.05
#         grand = total + tax
#         self.total_lbl.config(text=f"Total: ₹{total}")
#         self.tax_lbl.config(text=f"Tax (5%): ₹{tax:.2f}")
#         self.grand_lbl.config(text=f"Grand Total: ₹{grand:.2f}")

#     def clear_cart(self):
#         self.cart.clear()
#         self.update_bill()

#     def make_payment(self):
#         if not self.cart:
#             messagebox.showwarning("Empty Cart", "Add items before payment!")
#             return
#         messagebox.showinfo("Payment", "Payment Successful!")
#         self.clear_cart()

# # Run App
# root = tk.Tk()
# app = POSApp(root)
# root.mainloop()



# import tkinter as tk
# from tkinter import ttk, messagebox
# from PIL import Image, ImageTk

# # ==================== Product Data ====================
# products = [
#     {"barcode": "89450000937", "name": "Milk 370ml", "qty": 35, "price": 49, "category": "SoftDrink", "image": "milk.png"},
#     {"barcode": "89400000012", "name": "Mr.Chicken SM", "qty": 7687, "price": 150, "category": "Food", "image": "chicken.png"},
#     {"barcode": "89234500012", "name": "Shopping Cart", "qty": 7, "price": 49, "category": "Burger", "image": "cart.png"},
#     {"barcode": "89400000027", "name": "Coffee, Milk", "qty": 247, "price": 249, "category": "Drink", "image": "coffee.png"},
#     {"barcode": "89400000017", "name": "Chicken Bhona", "qty": 376, "price": 125, "category": "Food", "image": "chicken_bhona.png"},
#     {"barcode": "89400000014", "name": "Mountain Dew 770ml", "qty": 36, "price": 55, "category": "CoolDrink", "image": "dew.png"},
#     {"barcode": "89400000015", "name": "Mountain Dew 355ml", "qty": 100, "price": 35, "category": "CoolDrink", "image": "dew_small.png"},
#     {"barcode": "89400000021", "name": "Strawberry 400gm", "qty": 50, "price": 125, "category": "Fruit", "image": "strawberry.png"},
#     {"barcode": "89400000024", "name": "Apple 400gm", "qty": 24, "price": 49, "category": "Fruit", "image": "apple.png"},
#     {"barcode": "89400000036", "name": "Grapes 1kg", "qty": 207, "price": 99, "category": "Fruit", "image": "grapes.png"}
# ]

# categories = ["SoftDrink", "Food", "Burger", "CoolDrink", "Fruit", "Drink", "Coffe"]

# # ==================== POS Application Class ====================
# class POSApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Point of Sale System")
#         self.root.geometry("1200x650")
#         self.root.config(bg="#E9E9E9")

#         self.cart = []
#         self.images = {}

#         # ==================== LEFT BILLING SECTION ====================
#         left_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="white")
#         left_frame.place(x=10, y=10, width=700, height=630)

#         # Barcode entry
#         barcode_frame = tk.Frame(left_frame, bg="white")
#         barcode_frame.pack(fill=tk.X, pady=5)
#         tk.Label(barcode_frame, text="Insert Barcode:", bg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
#         self.barcode_entry = tk.Entry(barcode_frame, font=("Arial", 12), bd=2, relief=tk.SUNKEN)
#         self.barcode_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
#         tk.Button(barcode_frame, text="Search", command=self.search_barcode, bg="#0078D7", fg="white").pack(side=tk.LEFT, padx=5)

#         # Billing Table
#         self.bill_table = ttk.Treeview(left_frame, columns=("name", "price", "qty", "total"), show="headings")
#         self.bill_table.heading("name", text="Items")
#         self.bill_table.heading("price", text="Price")
#         self.bill_table.heading("qty", text="Qty")
#         self.bill_table.heading("total", text="Total")
#         self.bill_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

#         # Totals section
#         totals_frame = tk.Frame(left_frame, bg="white", bd=2, relief=tk.RIDGE)
#         totals_frame.pack(fill=tk.X, pady=5)
#         self.total_lbl = tk.Label(totals_frame, text="Total: 0", font=("Arial", 12, "bold"), bg="white")
#         self.total_lbl.pack(side=tk.LEFT, padx=10)
#         self.tax_lbl = tk.Label(totals_frame, text="Tax: 0", font=("Arial", 12, "bold"), bg="white")
#         self.tax_lbl.pack(side=tk.LEFT, padx=10)
#         self.pay_lbl = tk.Label(totals_frame, text="Total Payable: 0", font=("Arial", 12, "bold"), bg="white")
#         self.pay_lbl.pack(side=tk.LEFT, padx=10)

#         # Buttons
#         btn_frame = tk.Frame(left_frame, bg="white")
#         btn_frame.pack(fill=tk.X, pady=5)
#         tk.Button(btn_frame, text="Payment", bg="green", fg="white", font=("Arial", 13, "bold"), width=15, command=self.make_payment).pack(side=tk.LEFT, padx=10)
#         tk.Button(btn_frame, text="Suspend", bg="orange", fg="white", font=("Arial", 13, "bold"), width=15, command=self.clear_cart).pack(side=tk.RIGHT, padx=10)

#         # ==================== RIGHT PRODUCT SECTION ====================
#         right_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE)
#         right_frame.place(x=720, y=10, width=470, height=630)

#         # Search bar
#         search_frame = tk.Frame(right_frame)
#         search_frame.pack(fill=tk.X, pady=5)
#         self.search_var = tk.StringVar()
#         tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=25).pack(side=tk.LEFT, padx=5)
#         tk.Button(search_frame, text="Search", bg="#0078D7", fg="white", command=self.search_item).pack(side=tk.LEFT)

#         # Categories
#         cat_frame = tk.Frame(right_frame)
#         cat_frame.pack(fill=tk.X, pady=5)
#         for cat in categories:
#             tk.Button(cat_frame, text=cat, width=10, height=2, bg="#CFE2F3", command=lambda c=cat: self.load_items(c)).pack(side=tk.LEFT, padx=8)

#         # Product List
#         self.product_frame = tk.Frame(right_frame)
#         self.product_frame.pack(fill=tk.BOTH, expand=True)
#         self.load_items()

#     # ==================== Functionalities ====================
#     def load_items(self, category=None):
#         for widget in self.product_frame.winfo_children():
#             widget.destroy()

#         filtered = [p for p in products if (category is None or p["category"] == category)]
#         for product in filtered:
#             frame = tk.Frame(self.product_frame, bd=2, relief=tk.RIDGE)
#             frame.pack(fill=tk.X, pady=3, padx=5)

#             # Product image
#             img_path = product["image"]
#             try:
#                 img = Image.open(img_path)
#                 img = img.resize((50, 50))
#                 photo = ImageTk.PhotoImage(img)
#             except:
#                 photo = None

#             if photo:
#                 img_label = tk.Label(frame, image=photo)
#                 img_label.image = photo
#                 img_label.pack(side=tk.LEFT, padx=5)

#             # Product details
#             details = tk.Frame(frame)
#             details.pack(side=tk.LEFT, fill=tk.X, expand=True)
#             tk.Label(details, text=product["name"], font=("Arial", 10, "bold")).pack(anchor="w")
#             tk.Label(details, text=f"Qty: {product['qty']}   Price: ₹{product['price']}", font=("Arial", 9)).pack(anchor="w")

#             # Add button
#             tk.Button(frame, text="Add", bg="lightgreen", command=lambda p=product: self.add_to_cart(p)).pack(side=tk.RIGHT, padx=5)

#     def add_to_cart(self, product):
#         for item in self.cart:
#             if item["name"] == product["name"]:
#                 item["qty"] += 1
#                 break
#         else:
#             self.cart.append({"name": product["name"], "price": product["price"], "qty": 1})
#         self.update_bill()

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
#         self.pay_lbl.config(text=f"Total Payable: ₹{payable:.2f}")

#     def clear_cart(self):
#         self.cart.clear()
#         self.update_bill()

#     def make_payment(self):
#         if not self.cart:
#             messagebox.showwarning("Empty Cart", "Add items before payment!")
#             return
#         messagebox.showinfo("Payment", "Payment Successful ✅")
#         self.clear_cart()

#     def search_item(self):
#         query = self.search_var.get().lower()
#         if query:
#             filtered = [p for p in products if query in p["name"].lower()]
#             if filtered:
#                 self.show_filtered_items(filtered)
#             else:
#                 messagebox.showinfo("Not Found", "No matching items found.")
#         else:
#             self.load_items()

#     def search_barcode(self):
#         code = self.barcode_entry.get().strip()
#         for product in products:
#             if product["barcode"] == code:
#                 self.add_to_cart(product)
#                 return
#         messagebox.showinfo("Not Found", "Barcode not found!")

#     def show_filtered_items(self, filtered):
#         for widget in self.product_frame.winfo_children():
#             widget.destroy()
#         for product in filtered:
#             frame = tk.Frame(self.product_frame, bd=2, relief=tk.RIDGE)
#             frame.pack(fill=tk.X, pady=3, padx=5)
#             tk.Label(frame, text=product["name"], font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
#             tk.Button(frame, text="Add", bg="lightgreen", command=lambda p=product: self.add_to_cart(p)).pack(side=tk.RIGHT, padx=5)

# # ==================== Run Application ====================
# root = tk.Tk()
# app = POSApp(root)
# root.mainloop()




# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from PIL import Image, ImageTk

# # ==================== Product Data ====================
# products = [
#     {"barcode": "89450000937", "name": "Milk 370ml", "qty": 35, "price": 49, "category": "SoftDrink", "image": "milk.png"},
#     {"barcode": "89400000012", "name": "Mr.Chicken SM", "qty": 7687, "price": 150, "category": "Food", "image": "chicken.png"},
#     {"barcode": "89234500012", "name": "Shopping Cart", "qty": 7, "price": 49, "category": "Burger", "image": "cart.png"},
#     {"barcode": "89400000027", "name": "Coffee, Milk", "qty": 247, "price": 249, "category": "Drink", "image": "coffee.png"},
#     {"barcode": "89400000017", "name": "Chicken Bhona", "qty": 376, "price": 125, "category": "Food", "image": "chicken_bhona.png"},
#     {"barcode": "89400000014", "name": "Mountain Dew 770ml", "qty": 36, "price": 55, "category": "CoolDrink", "image": "dew.png"},
#     {"barcode": "89400000015", "name": "Mountain Dew 355ml", "qty": 100, "price": 35, "category": "CoolDrink", "image": "dew_small.png"},
#     {"barcode": "89400000021", "name": "Strawberry 400gm", "qty": 50, "price": 125, "category": "Fruit", "image": "strawberry.png"},
#     {"barcode": "89400000024", "name": "Apple 400gm", "qty": 24, "price": 49, "category": "Fruit", "image": "apple.png"},
#     {"barcode": "89400000036", "name": "Grapes 1kg", "qty": 207, "price": 99, "category": "Fruit", "image": "grapes.png"}
# ]

# categories = ["SoftDrink", "Food", "Burger", "CoolDrink", "Fruit", "Drink"]

# # ==================== POS Application Class ====================
# class POSApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Point of Sale System")
#         self.root.geometry("1200x650")
#         self.root.config(bg="#E9E9E9")

#         self.cart = []
#         self.images = {}

#         # ==================== LEFT BILLING SECTION ====================
#         left_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="white")
#         left_frame.place(x=10, y=10, width=700, height=630)

#         # Barcode entry
#         barcode_frame = tk.Frame(left_frame, bg="white")
#         barcode_frame.pack(fill=tk.X, pady=5)
#         tk.Label(barcode_frame, text="Insert Barcode:", bg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
#         self.barcode_entry = tk.Entry(barcode_frame, font=("Arial", 12), bd=2, relief=tk.SUNKEN)
#         self.barcode_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
#         tk.Button(barcode_frame, text="Search", command=self.search_barcode, bg="#0078D7", fg="white").pack(side=tk.LEFT, padx=5)

#         # Billing Table
#         self.bill_table = ttk.Treeview(left_frame, columns=("name", "price", "qty", "total"), show="headings")
#         self.bill_table.heading("name", text="Items")
#         self.bill_table.heading("price", text="Price")
#         self.bill_table.heading("qty", text="Qty")
#         self.bill_table.heading("total", text="Total")
#         self.bill_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

#         # Totals section
#         totals_frame = tk.Frame(left_frame, bg="white", bd=2, relief=tk.RIDGE)
#         totals_frame.pack(fill=tk.X, pady=5)
#         self.total_lbl = tk.Label(totals_frame, text="Total: ₹0.00", font=("Arial", 12, "bold"), bg="white")
#         self.total_lbl.pack(side=tk.LEFT, padx=10)
#         self.tax_lbl = tk.Label(totals_frame, text="Tax: ₹0.00", font=("Arial", 12, "bold"), bg="white")
#         self.tax_lbl.pack(side=tk.LEFT, padx=10)
#         self.pay_lbl = tk.Label(totals_frame, text="Total Payable: ₹0.00", font=("Arial", 12, "bold"), bg="white")
#         self.pay_lbl.pack(side=tk.LEFT, padx=10)

#         # Buttons
#         btn_frame = tk.Frame(left_frame, bg="white")
#         btn_frame.pack(fill=tk.X, pady=5)
#         tk.Button(btn_frame, text="Download Bill", bg="#4CAF50", fg="white", font=("Arial", 13, "bold"), width=15, command=self.download_bill).pack(side=tk.LEFT, padx=10)
#         tk.Button(btn_frame, text="Clear", bg="#FF9800", fg="white", font=("Arial", 13, "bold"), width=15, command=self.clear_cart).pack(side=tk.RIGHT, padx=10)

#         # ==================== RIGHT PRODUCT SECTION ====================
#         right_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE)
#         right_frame.place(x=720, y=10, width=470, height=630)

#         # Vertical layout: categories on right, items on left side of right_frame
#         container = tk.Frame(right_frame)
#         container.pack(fill=tk.BOTH, expand=True)

#         # Categories List
#         cat_frame = tk.Frame(container, bd=2, relief=tk.RIDGE, bg="#f4f4f4")
#         cat_frame.pack(side=tk.RIGHT, fill=tk.Y)
#         tk.Label(cat_frame, text="Categories", bg="#CFE2F3", font=("Arial", 12, "bold")).pack(fill=tk.X)
#         for cat in categories:
#             tk.Button(cat_frame, text=cat, width=15, bg="#CFE2F3", font=("Arial", 10, "bold"),
#                       command=lambda c=cat: self.load_items(c)).pack(pady=5)

#         # Product List
#         self.product_frame = tk.Frame(container)
#         self.product_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         self.load_items()  # Load all products initially

#     # ==================== Functionalities ====================
#     def load_items(self, category=None):
#         for widget in self.product_frame.winfo_children():
#             widget.destroy()

#         filtered = [p for p in products if (category is None or p["category"] == category)]
#         for product in filtered:
#             frame = tk.Frame(self.product_frame, bd=2, relief=tk.RIDGE)
#             frame.pack(fill=tk.X, pady=3, padx=5)

#             try:
#                 img = Image.open(product["image"])
#                 img = img.resize((60, 60))
#                 photo = ImageTk.PhotoImage(img)
#             except:
#                 photo = None

#             if photo:
#                 img_label = tk.Label(frame, image=photo)
#                 img_label.image = photo
#                 img_label.pack(side=tk.LEFT, padx=5)

#             # Product details
#             details = tk.Frame(frame)
#             details.pack(side=tk.LEFT, fill=tk.X, expand=True)
#             tk.Label(details, text=product["name"], font=("Arial", 11, "bold")).pack(anchor="w")
#             tk.Label(details, text=f"Price: ₹{product['price']}", font=("Arial", 10)).pack(anchor="w")

#             # Quantity buttons
#             qty_frame = tk.Frame(frame)
#             qty_frame.pack(side=tk.RIGHT, padx=10)
#             qty_var = tk.IntVar(value=1)
#             tk.Button(qty_frame, text="-", width=2, command=lambda v=qty_var: self.decrease_qty(v)).pack(side=tk.LEFT)
#             tk.Label(qty_frame, textvariable=qty_var, width=3).pack(side=tk.LEFT)
#             tk.Button(qty_frame, text="+", width=2, command=lambda v=qty_var: self.increase_qty(v)).pack(side=tk.LEFT)
#             tk.Button(qty_frame, text="Add", bg="lightgreen",
#                       command=lambda p=product, v=qty_var: self.add_to_cart(p, v.get())).pack(side=tk.LEFT, padx=5)

#     def increase_qty(self, var):
#         var.set(var.get() + 1)

#     def decrease_qty(self, var):
#         if var.get() > 1:
#             var.set(var.get() - 1)

#     def add_to_cart(self, product, qty):
#         for item in self.cart:
#             if item["name"] == product["name"]:
#                 item["qty"] += qty
#                 break
#         else:
#             self.cart.append({"name": product["name"], "price": product["price"], "qty": qty})
#         self.update_bill()

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
#         self.pay_lbl.config(text=f"Total Payable: ₹{payable:.2f}")

#     def clear_cart(self):
#         self.cart.clear()
#         self.update_bill()

#     def search_barcode(self):
#         code = self.barcode_entry.get().strip()
#         for product in products:
#             if product["barcode"] == code:
#                 self.add_to_cart(product, 1)
#                 return
#         messagebox.showinfo("Not Found", "Barcode not found!")

#     def download_bill(self):
#         if not self.cart:
#             messagebox.showwarning("Empty Cart", "Add items before downloading the bill!")
#             return
#         file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
#         if not file_path:
#             return
#         total = 0
#         with open(file_path, "w") as f:
#             f.write("===== POINT OF SALE BILL =====\n\n")
#             for item in self.cart:
#                 subtotal = item["price"] * item["qty"]
#                 total += subtotal
#                 f.write(f"{item['name']} - {item['qty']} x ₹{item['price']} = ₹{subtotal}\n")
#             tax = total * 0.05
#             payable = total + tax
#             f.write("\n-----------------------------\n")
#             f.write(f"Total: ₹{total:.2f}\nTax: ₹{tax:.2f}\nPayable: ₹{payable:.2f}\n")
#             f.write("-----------------------------\nThank you for shopping!\n")
#         messagebox.showinfo("Bill Downloaded", "Bill saved successfully!")

# # ==================== Run Application ====================
# root = tk.Tk()
# app = POSApp(root)
# root.mainloop()



# pos_with_db_pdf.py
# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from PIL import Image, ImageTk
# import sqlite3
# import os
# from datetime import datetime
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.units import mm
# from reportlab.pdfgen import canvas
# from reportlab.platypus import Table, TableStyle

# DB_FILE = "pos_system.db"
# IMAGE_FOLDER = "images"   # put your product images here

# SAMPLE_PRODUCTS = [
#     # (barcode, name, category, qty, price, image_path)
#     ("89450000937", "Coke", "SoftDrink", 35, 49.00, "coke.png"),
#     ("89450000937", "Pepsi", "SoftDrink", 35, 49.00, "pepsi.png"),
#     ("89450000937", "7 Up", "SoftDrink", 35, 49.00, "7up.png"),
#     ("89400000012", "Grilled Chicken", "Food", 7687, 150.00, "grilled_chicken.png"),
#     ("89234500012", "Chicken Burger", "Burger", 7, 99.00, "chicken_burger.png"),
#     ("89234500013", "Veg Burger", "Burger", 7, 89.00, "veg_burger.png"),
#     ("89400000027", "Coffee", "Drink", 247, 249.00, "coffee.png"),
#     ("89400000027", "Milk", "Drink", 247, 249.00, "milk.png"),
#     ("89400000017", "Chicken Biryani", "Food", 376, 125.00, "chicken_biryani.png"),
#     ("89400000014", "Lemon", "CoolDrink", 36, 55.00, "lemon.png"),
#     ("89400000015", "Pineapple", "CoolDrink", 100, 35.00, "pineapple.png"),
#     ("89400000021", "Strawberry 400g", "Fruit", 50, 125.00, "strawberry.png"),
#     ("89400000024", "Apple 400gm", "Fruit", 24, 49.00, "apple.png"),
#     ("89400000036", "Grapes 1kg", "Fruit", 207, 99.00, "grapes.png"),
# ]

# # ---------------------- Database helpers ----------------------
# def init_db():
#     first_time = not os.path.exists(DB_FILE)
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS products (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             barcode TEXT UNIQUE,
#             name TEXT,
#             category TEXT,
#             qty INTEGER,
#             price REAL,
#             image_path TEXT
#         )
#     """)
#     conn.commit()
#     if first_time:
#         # populate sample data (ignore duplicates)
#         for (barcode, name, category, qty, price, image) in SAMPLE_PRODUCTS:
#             try:
#                 c.execute("INSERT INTO products (barcode, name, category, qty, price, image_path) VALUES (?,?,?,?,?,?)",
#                           (barcode, name, category, qty, price, image))
#             except Exception:
#                 pass
#         conn.commit()
#     conn.close()

# def fetch_categories():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT DISTINCT category FROM products")
#     rows = [r[0] for r in c.fetchall()]
#     conn.close()
#     return rows

# def fetch_products_by_category(category=None):
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     if category:
#         c.execute("SELECT barcode,name,category,qty,price,image_path FROM products WHERE category=? ORDER BY name", (category,))
#     else:
#         c.execute("SELECT barcode,name,category,qty,price,image_path FROM products ORDER BY category,name")
#     rows = c.fetchall()
#     conn.close()
#     # return list of dicts
#     return [{"barcode":r[0],"name":r[1],"category":r[2],"qty":r[3],"price":r[4],"image":r[5]} for r in rows]

# def get_product_by_barcode(barcode):
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT barcode,name,category,qty,price,image_path FROM products WHERE barcode=?", (barcode,))
#     r = c.fetchone()
#     conn.close()
#     if r:
#         return {"barcode":r[0],"name":r[1],"category":r[2],"qty":r[3],"price":r[4],"image":r[5]}
#     return None

# # ---------------------- GUI Application ----------------------
# class POSApp:
#     def __init__(self, root):
#         self.root = root
#         root.title("POS System with SQLite & PDF")
#         root.geometry("1200x700")
#         root.configure(bg="#eaeaea")

#         self.cart = []  # list of dicts: {name, price, qty}
#         self.thumb_cache = {}

#         # Layout: left categories column, middle items area, right bill
#         self.left_col = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="#f7f7f7")
#         self.left_col.place(x=10, y=10, width=200, height=680)

#         self.mid_col = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="#ffffff")
#         self.mid_col.place(x=220, y=10, width=620, height=680)

#         self.right_col = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="#fdfdfd")
#         self.right_col.place(x=850, y=10, width=340, height=680)

#         self.build_left()
#         self.build_mid()
#         self.build_right()
#         self.load_categories()
#         self.load_items(None)  # show all

#     # ---------- Left: vertical categories ----------
#     def build_left(self):
#         tk.Label(self.left_col, text="Categories", bg="#cfe2f3", font=("Arial", 12, "bold")).pack(fill="x")
#         self.cat_container = tk.Frame(self.left_col, bg="#f7f7f7")
#         self.cat_container.pack(fill="both", expand=True, padx=5, pady=5)
#         # Search barcode at top
#         bar_frame = tk.Frame(self.left_col, bg="#f7f7f7")
#         bar_frame.pack(fill="x", padx=5, pady=5)
#         tk.Label(bar_frame, text="Barcode:", bg="#f7f7f7", font=("Arial",9)).pack(side="left")
#         self.barcode_entry = tk.Entry(bar_frame, width=12)
#         self.barcode_entry.pack(side="left", padx=5)
#         tk.Button(bar_frame, text="Add", command=self.search_barcode, width=6).pack(side="left")

#     def load_categories(self):
#         for w in self.cat_container.winfo_children():
#             w.destroy()
#         cats = fetch_categories()
#         # Add "All" button
#         tk.Button(self.cat_container, text="All", width=18, anchor="w",
#                   command=lambda c=None: self.load_items(c)).pack(pady=3)
#         for c in cats:
#             tk.Button(self.cat_container, text=c, width=18, anchor="w",
#                       command=lambda cat=c: self.load_items(cat)).pack(pady=3)

#     # ---------- Middle: items with images + qty + Add ----------
#     def build_mid(self):
#         top = tk.Frame(self.mid_col, bg="#ffffff")
#         top.pack(fill="x", padx=5, pady=5)
#         tk.Label(top, text="Items", bg="#ffffff", font=("Arial", 12, "bold")).pack(side="left")

#         # Canvas scroll area for items
#         self.items_canvas = tk.Canvas(self.mid_col, bg="#ffffff")
#         self.items_scroll_y = ttk.Scrollbar(self.mid_col, orient="vertical", command=self.items_canvas.yview)
#         self.items_frame = tk.Frame(self.items_canvas, bg="#ffffff")
#         self.items_frame.bind("<Configure>", lambda e: self.items_canvas.configure(scrollregion=self.items_canvas.bbox("all")))
#         self.items_canvas.create_window((0,0), window=self.items_frame, anchor="nw")
#         self.items_canvas.configure(yscrollcommand=self.items_scroll_y.set)
#         self.items_canvas.pack(side="left", fill="both", expand=True)
#         self.items_scroll_y.pack(side="right", fill="y")

#     def load_items(self, category=None):
#         # clear
#         for w in self.items_frame.winfo_children():
#             w.destroy()
#         prods = fetch_products_by_category(category)
#         for p in prods:
#             # card frame
#             card = tk.Frame(self.items_frame, bd=1, relief="solid", bg="#fafafa")
#             card.pack(fill="x", padx=6, pady=6)

#             # image
#             for product in products:
#                 try:
#                     img_path = os.path.join(os.path.dirname(__file__), "images", product["image"])
#                     img = Image.open(img_path)
#                     img = img.resize((70, 70))
#                     photo = ImageTk.PhotoImage(img)
#                 except Exception as e:
#                     print(f"Error loading {product['image']}: {e}")
#                     img = Image.new("RGB", (70, 70), "gray")
#                     photo = ImageTk.PhotoImage(img)


#             # details
#             d = tk.Frame(card, bg="#fafafa")
#             d.pack(side="left", fill="both", expand=True)
#             tk.Label(d, text=p["name"], bg="#fafafa", anchor="w", font=("Arial",10,"bold")).pack(fill="x")
#             tk.Label(d, text=f"Stock: {p['qty']}   Price: ₹{p['price']:.2f}", bg="#fafafa", anchor="w").pack(fill="x")

#             # qty chooser and add
#             controls = tk.Frame(card, bg="#fafafa")
#             controls.pack(side="right", padx=6)
#             qty_var = tk.IntVar(value=1)
#             tk.Button(controls, text="-", width=2, command=lambda v=qty_var: v.set(max(1,v.get()-1))).pack(side="left")
#             tk.Label(controls, textvariable=qty_var, width=3).pack(side="left")
#             tk.Button(controls, text="+", width=2, command=lambda v=qty_var: v.set(v.get()+1)).pack(side="left")
#             tk.Button(controls, text="Add", bg="#4CAF50", fg="white",
#                       command=lambda prod=p, v=qty_var: self.add_to_cart(prod, v.get())).pack(side="left", padx=5)

#     def get_thumb(self, image_name):
#         # caches thumbnails to avoid reloading
#         key = image_name
#         if key in self.thumb_cache:
#             return self.thumb_cache[key]
#         path = os.path.join(IMAGE_FOLDER, image_name) if image_name else None
#         try:
#             img = Image.open(path)
#             img.thumbnail((64,64))
#             photo = ImageTk.PhotoImage(img)
#         except Exception:
#             # placeholder
#             img = Image.new("RGB",(64,64),(200,200,200))
#             photo = ImageTk.PhotoImage(img)
#         self.thumb_cache[key] = photo
#         return photo

#     # ---------- Right: bill area ----------
#     def build_right(self):
#         header = tk.Frame(self.right_col, bg="#fdfdfd")
#         header.pack(fill="x")
#         tk.Label(header, text="Bill / Cart", font=("Arial",12,"bold"), bg="#fdfdfd").pack(side="left", padx=6)
#         tk.Button(header, text="+", width=3, command=self.increase_selected_qty).pack(side="right", padx=4)
#         tk.Button(header, text="-", width=3, command=self.decrease_selected_qty).pack(side="right")
#         # Treeview for cart
#         cols = ("name","price","qty","total")
#         self.cart_tree = ttk.Treeview(self.right_col, columns=cols, show="headings", height=18)
#         self.cart_tree.heading("name", text="Item")
#         self.cart_tree.heading("price", text="Price")
#         self.cart_tree.heading("qty", text="Qty")
#         self.cart_tree.heading("total", text="Total")
#         self.cart_tree.column("name", width=130)
#         self.cart_tree.column("price", width=60, anchor="e")
#         self.cart_tree.column("qty", width=40, anchor="center")
#         self.cart_tree.column("total", width=70, anchor="e")
#         self.cart_tree.pack(fill="both", padx=6, pady=6)
#         self.cart_tree.bind("<Double-1>", self.on_cart_double_click)

#         # totals area
#         totals = tk.Frame(self.right_col, bg="#fdfdfd")
#         totals.pack(fill="x", padx=6, pady=6)
#         tk.Label(totals, text="Total:", bg="#fdfdfd").grid(row=0,column=0, sticky="w")
#         self.lbl_total = tk.Label(totals, text="₹0.00", bg="#fdfdfd")
#         self.lbl_total.grid(row=0,column=1, sticky="e")
#         tk.Label(totals, text="Tax (5%):", bg="#fdfdfd").grid(row=1,column=0, sticky="w")
#         self.lbl_tax = tk.Label(totals, text="₹0.00", bg="#fdfdfd")
#         self.lbl_tax.grid(row=1,column=1, sticky="e")
#         tk.Label(totals, text="Grand Total:", bg="#fdfdfd", font=("Arial",10,"bold")).grid(row=2,column=0, sticky="w", pady=6)
#         self.lbl_grand = tk.Label(totals, text="₹0.00", bg="#fdfdfd", font=("Arial",10,"bold"))
#         self.lbl_grand.grid(row=2,column=1, sticky="e", pady=6)

#         # action buttons
#         actions = tk.Frame(self.right_col, bg="#fdfdfd")
#         actions.pack(fill="x", padx=6, pady=6)
#         tk.Button(actions, text="Download Bill (PDF)", bg="#4CAF50", fg="white", command=self.download_pdf).pack(side="left", expand=True, fill="x", padx=3)
#         tk.Button(actions, text="Clear Cart", bg="#FF9800", fg="white", command=self.clear_cart).pack(side="left", expand=True, fill="x", padx=3)
#         tk.Button(actions, text="Payment (Clear)", bg="#0078D7", fg="white", command=self.payment_clear).pack(side="left", expand=True, fill="x", padx=3)

#     # ---------- Cart management ----------
#     def add_to_cart(self, product, qty):
#         # product: dict with name, price
#         name = product["name"]
#         price = float(product["price"])
#         # if already in cart, increase qty
#         for it in self.cart:
#             if it["name"] == name:
#                 it["qty"] += qty
#                 break
#         else:
#             self.cart.append({"name": name, "price": price, "qty": qty})
#         self.refresh_cart()

#     def refresh_cart(self):
#         for row in self.cart_tree.get_children():
#             self.cart_tree.delete(row)
#         total = 0.0
#         for it in self.cart:
#             subtotal = it["price"] * it["qty"]
#             total += subtotal
#             self.cart_tree.insert("", "end", values=(it["name"], f"₹{it['price']:.2f}", it["qty"], f"₹{subtotal:.2f}"))
#         tax = total * 0.05
#         grand = total + tax
#         self.lbl_total.config(text=f"₹{total:.2f}")
#         self.lbl_tax.config(text=f"₹{tax:.2f}")
#         self.lbl_grand.config(text=f"₹{grand:.2f}")

#     def clear_cart(self):
#         self.cart = []
#         self.refresh_cart()

#     def payment_clear(self):
#         if not self.cart:
#             messagebox.showwarning("No items", "Cart is empty.")
#             return
#         messagebox.showinfo("Payment", "Payment successful. Cart cleared.")
#         self.clear_cart()

#     # change selected qty via + / -
#     def increase_selected_qty(self):
#         sel = self.cart_tree.selection()
#         if not sel:
#             return
#         idx = self.cart_tree.index(sel[0])
#         self.cart[idx]["qty"] += 1
#         self.refresh_cart()

#     def decrease_selected_qty(self):
#         sel = self.cart_tree.selection()
#         if not sel:
#             return
#         idx = self.cart_tree.index(sel[0])
#         if self.cart[idx]["qty"] > 1:
#             self.cart[idx]["qty"] -= 1
#         else:
#             # remove item if qty becomes 0
#             self.cart.pop(idx)
#         self.refresh_cart()

#     def on_cart_double_click(self, event):
#         # allow editing qty by double click on Qty cell
#         item_id = self.cart_tree.identify_row(event.y)
#         col = self.cart_tree.identify_column(event.x)
#         if not item_id:
#             return
#         idx = self.cart_tree.index(item_id)
#         if col == '#3':  # Qty column
#             self.open_qty_popup(idx)

#     def open_qty_popup(self, idx):
#         popup = tk.Toplevel(self.root)
#         popup.title("Edit Quantity")
#         popup.geometry("200x100")
#         tk.Label(popup, text=f"Edit qty for:\n{self.cart[idx]['name']}", wraplength=180).pack(pady=5)
#         var = tk.IntVar(value=self.cart[idx]["qty"])
#         ent = tk.Entry(popup, textvariable=var, width=6, justify="center")
#         ent.pack()
#         def save():
#             try:
#                 v = int(var.get())
#                 if v <= 0:
#                     self.cart.pop(idx)
#                 else:
#                     self.cart[idx]["qty"] = v
#                 self.refresh_cart()
#                 popup.destroy()
#             except Exception:
#                 messagebox.showerror("Invalid", "Enter valid integer quantity.")
#         tk.Button(popup, text="Save", command=save).pack(pady=5)

#     # ---------- Barcode search ----------
#     def search_barcode(self):
#         code = self.barcode_entry.get().strip()
#         if not code:
#             return
#         prod = get_product_by_barcode(code)
#         if not prod:
#             messagebox.showinfo("Not found", "Barcode not found in DB.")
#             return
#         # add 1 by default
#         self.add_to_cart(prod, 1)
#         self.barcode_entry.delete(0, tk.END)

#     # ---------- PDF generation ----------
#     def download_pdf(self):
#         if not self.cart:
#             messagebox.showwarning("Empty", "Add items before downloading bill.")
#             return
#         file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")], initialfile=f"Bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
#         if not file_path:
#             return
#         try:
#             self._generate_pdf(file_path)
#             messagebox.showinfo("Saved", f"Bill saved to:\n{file_path}")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to save PDF:\n{e}")

#     def _generate_pdf(self, file_path):
#         # create simple invoice using reportlab
#         c = canvas.Canvas(file_path, pagesize=A4)
#         width, height = A4

#         # Header
#         store_name = "My Store (POS)"
#         c.setFont("Helvetica-Bold", 16)
#         c.drawString(30*mm, (height - 20*mm), store_name)
#         c.setFont("Helvetica", 9)
#         c.drawString(30*mm, (height - 26*mm), f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

#         # Table data
#         table_data = [["Item", "Qty", "Unit (₹)", "Subtotal (₹)"]]
#         total = 0.0
#         for it in self.cart:
#             subtotal = it["price"] * it["qty"]
#             table_data.append([it["name"], str(it["qty"]), f"{it['price']:.2f}", f"{subtotal:.2f}"])
#             total += subtotal
#         tax = total * 0.05
#         grand = total + tax

#         # create the table
#         table = Table(table_data, colWidths=[80*mm,20*mm,30*mm,30*mm])
#         style = TableStyle([
#             ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
#             ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
#             ('ALIGN', (1,1), (-1,-1), 'CENTER'),
#             ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
#             ('FONT', (0,0), (-1,0), 'Helvetica-Bold')
#         ])
#         table.setStyle(style)
#         # draw table
#         table.wrapOn(c, width, height)
#         table.drawOn(c, 20*mm, height - 120*mm)

#         # totals
#         y = height - 120*mm - (len(table_data)+1)*6
#         c.setFont("Helvetica-Bold", 10)
#         c.drawRightString(170*mm, y - 10*mm, f"Total: ₹{total:.2f}")
#         c.drawRightString(170*mm, y - 16*mm, f"Tax (5%): ₹{tax:.2f}")
#         c.drawRightString(170*mm, y - 22*mm, f"Grand Total: ₹{grand:.2f}")

#         c.showPage()
#         c.save()

# # ---------------------- Run App ----------------------
# if __name__ == "__main__":
#     os.makedirs(IMAGE_FOLDER, exist_ok=True)  # ensure image folder exists
#     init_db()
#     root = tk.Tk()
#     app = POSApp(root)
#     root.mainloop()





import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os

# ==================== Product Data ====================
products = [
    {"barcode": "89450000937", "name": "Coke", "qty": 35, "price": 49, "category": "SoftDrink", "image": "coke.png"},
    {"barcode": "89450000938", "name": "Pepsi", "qty": 35, "price": 49, "category": "SoftDrink", "image": "pepsi.png"},
    {"barcode": "89450000939", "name": "7 Up", "qty": 35, "price": 49, "category": "SoftDrink", "image": "7up.png"},
    {"barcode": "89400000012", "name": "Grilled Chicken", "qty": 7687, "price": 150, "category": "Food", "image": "grilled_chicken.png"},
    {"barcode": "89234500012", "name": "Chicken Burger", "qty": 7, "price": 49, "category": "Burger", "image": "chicken_burger.png"},
    {"barcode": "89234500013", "name": "Veg Burger", "qty": 7, "price": 49, "category": "Burger", "image": "veg_burger.png"},
    {"barcode": "89400000027", "name": "Coffee", "qty": 247, "price": 249, "category": "Drink", "image": "coffee.png"},
    {"barcode": "89400000028", "name": "Milk", "qty": 247, "price": 249, "category": "Drink", "image": "milk.png"},
    {"barcode": "89400000017", "name": "Chicken Biryani", "qty": 376, "price": 125, "category": "Food", "image": "chicken_biryani.png"},
    {"barcode": "89400000014", "name": "Lemon", "qty": 36, "price": 55, "category": "CoolDrink", "image": "lemon.png"},
    {"barcode": "89400000015", "name": "Pineapple", "qty": 100, "price": 35, "category": "CoolDrink", "image": "pineapple.png"},
    {"barcode": "89400000021", "name": "Strawberry 400gm", "qty": 50, "price": 125, "category": "Fruit", "image": "strawberry.png"},
    {"barcode": "89400000024", "name": "Apple 400gm", "qty": 24, "price": 49, "category": "Fruit", "image": "apple.png"},
    {"barcode": "89400000036", "name": "Grapes 1kg", "qty": 207, "price": 99, "category": "Fruit", "image": "grapes.png"}
]

categories = ["SoftDrink", "Food", "Burger", "CoolDrink", "Fruit", "Drink"]

# ==================== POS Application ====================
class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart POS Billing System")
        self.root.geometry("1200x650")
        self.root.config(bg="#E9E9E9")

        self.cart = []

        # ==================== LEFT: BILL AREA ====================
        left_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE, bg="white")
        left_frame.place(x=10, y=10, width=700, height=630)

        # Barcode entry
        barcode_frame = tk.Frame(left_frame, bg="white")
        barcode_frame.pack(fill=tk.X, pady=5)
        tk.Label(barcode_frame, text="Insert Barcode:", bg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.barcode_entry = tk.Entry(barcode_frame, font=("Arial", 12), bd=2, relief=tk.SUNKEN)
        self.barcode_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(barcode_frame, text="Search", command=self.search_barcode, bg="#0078D7", fg="white").pack(side=tk.LEFT, padx=5)

        # Billing Table
        self.bill_table = ttk.Treeview(left_frame, columns=("name", "price", "qty", "total"), show="headings")
        self.bill_table.heading("name", text="Item")
        self.bill_table.heading("price", text="Price")
        self.bill_table.heading("qty", text="Qty")
        self.bill_table.heading("total", text="Total")
        self.bill_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

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
        for cat in categories:
            tk.Button(cat_frame, text=cat, width=13, height=2, bg="#E0EAF3", command=lambda c=cat: self.load_items(c)).pack(pady=5, padx=5)

        # Product display
        self.product_frame = tk.Frame(split_frame, bg="#FFFFFF")
        self.product_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.load_items()

    # ==================== FUNCTIONS ====================
    def load_items(self, category=None):
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        filtered = [p for p in products if category is None or p["category"] == category]

        for product in filtered:
            frame = tk.Frame(self.product_frame, bd=2, relief=tk.RIDGE, bg="#FAFAFA")
            frame.pack(fill=tk.X, pady=3, padx=5)

            # Load image safely
            try:
                img_path = os.path.join(os.path.dirname(__file__), "images", product["image"])
                img = Image.open(img_path).resize((60, 60))
                photo = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Image not found for {product['name']}: {e}")
                img = Image.new("RGB", (60, 60), "gray")
                photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(frame, image=photo)
            img_label.image = photo
            img_label.pack(side=tk.LEFT, padx=5)

            # Info
            info_frame = tk.Frame(frame, bg="#FAFAFA")
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Label(info_frame, text=product["name"], font=("Arial", 10, "bold"), bg="#FAFAFA").pack(anchor="w")
            tk.Label(info_frame, text=f"₹{product['price']} | Stock: {product['qty']}", bg="#FAFAFA").pack(anchor="w")

            # Add button
            tk.Button(frame, text="+", bg="lightgreen", command=lambda p=product: self.add_to_cart(p)).pack(side=tk.RIGHT, padx=3)
            tk.Button(frame, text="-", bg="lightcoral", command=lambda p=product: self.remove_from_cart(p)).pack(side=tk.RIGHT, padx=3)

    def add_to_cart(self, product):
        for item in self.cart:
            if item["name"] == product["name"]:
                item["qty"] += 1
                break
        else:
            self.cart.append({"name": product["name"], "price": product["price"], "qty": 1})
        self.update_bill()

    def remove_from_cart(self, product):
        for item in self.cart:
            if item["name"] == product["name"]:
                item["qty"] -= 1
                if item["qty"] <= 0:
                    self.cart.remove(item)
                break
        self.update_bill()

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
        messagebox.showinfo("Payment", "Payment Successful ✅")
        self.clear_cart()

    def download_bill(self):
        if not self.cart:
            messagebox.showwarning("Empty", "No items to download!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if not file_path:
            return
        with open(file_path, "w") as f:
            f.write("======== Smart POS Bill ========\n")
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
        for product in products:
            if product["barcode"] == code:
                self.add_to_cart(product)
                return
        messagebox.showinfo("Not Found", "Barcode not found!")

    def search_item(self):
        query = self.search_var.get().lower()
        if query:
            filtered = [p for p in products if query in p["name"].lower()]
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
            frame = tk.Frame(self.product_frame, bd=2, relief=tk.RIDGE, bg="#FAFAFA")
            frame.pack(fill=tk.X, pady=3, padx=5)
            tk.Label(frame, text=product["name"], font=("Arial", 10, "bold"), bg="#FAFAFA").pack(side=tk.LEFT, padx=10)
            tk.Button(frame, text="+", bg="lightgreen", command=lambda p=product: self.add_to_cart(p)).pack(side=tk.RIGHT, padx=5)

# ==================== Run App ====================
root = tk.Tk()
app = POSApp(root)
root.mainloop()




# # pos_system.py
# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from PIL import Image, ImageTk
# import sqlite3
# import os
# from datetime import datetime
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.units import mm
# from reportlab.pdfgen import canvas
# from reportlab.platypus import Table, TableStyle

# DB_FILE = "pos_system.db"
# IMAGE_FOLDER = "images"

# SAMPLE_PRODUCTS = [
#     ("89450000937", "Coke", "SoftDrink", 35, 49.00, "coke.png"),
#     ("89450000938", "Pepsi", "SoftDrink", 35, 49.00, "pepsi.png"),
#     ("89450000939", "7 Up", "SoftDrink", 35, 49.00, "7up.png"),
#     ("89400000012", "Grilled Chicken", "Food", 30, 150.00, "grilled_chicken.png"),
#     ("89234500012", "Chicken Burger", "Burger", 50, 99.00, "chicken_burger.png"),
#     ("89234500013", "Veg Burger", "Burger", 45, 89.00, "veg_burger.png"),
#     ("89400000027", "Coffee", "Drink", 100, 49.00, "coffee.png"),
#     ("89400000028", "Milk", "Drink", 200, 39.00, "milk.png"),
#     ("89400000017", "Chicken Biryani", "Food", 40, 125.00, "chicken_biryani.png"),
#     ("89400000021", "Strawberry 400g", "Fruit", 20, 125.00, "strawberry.png"),
#     ("89400000024", "Apple 400gm", "Fruit", 24, 49.00, "apple.png"),
# ]

# # ---------------------- Database Setup ----------------------
# def init_db():
#     first_time = not os.path.exists(DB_FILE)
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS products (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             barcode TEXT UNIQUE,
#             name TEXT,
#             category TEXT,
#             qty INTEGER,
#             price REAL,
#             image_path TEXT
#         )
#     """)
#     conn.commit()
#     if first_time:
#         for (barcode, name, category, qty, price, image) in SAMPLE_PRODUCTS:
#             try:
#                 c.execute("INSERT INTO products (barcode,name,category,qty,price,image_path) VALUES (?,?,?,?,?,?)",
#                           (barcode, name, category, qty, price, image))
#             except Exception:
#                 pass
#         conn.commit()
#     conn.close()

# def fetch_categories():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT DISTINCT category FROM products")
#     rows = [r[0] for r in c.fetchall()]
#     conn.close()
#     return rows

# def fetch_products_by_category(category=None):
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     if category:
#         c.execute("SELECT barcode,name,category,qty,price,image_path FROM products WHERE category=?", (category,))
#     else:
#         c.execute("SELECT barcode,name,category,qty,price,image_path FROM products")
#     rows = c.fetchall()
#     conn.close()
#     return [{"barcode":r[0],"name":r[1],"category":r[2],"qty":r[3],"price":r[4],"image":r[5]} for r in rows]

# def get_product_by_barcode(barcode):
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT barcode,name,category,qty,price,image_path FROM products WHERE barcode=?", (barcode,))
#     r = c.fetchone()
#     conn.close()
#     if r:
#         return {"barcode":r[0],"name":r[1],"category":r[2],"qty":r[3],"price":r[4],"image":r[5]}
#     return None

# # ---------------------- Main App ----------------------
# class POSApp:
#     def __init__(self, root):
#         self.root = root
#         root.title("POS Billing System")
#         root.geometry("1200x700")
#         root.configure(bg="#f0f0f0")

#         self.cart = []
#         self.thumb_cache = {}

#         # Layout Frames
#         self.left_col = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="#f7f7f7")
#         self.left_col.place(x=10, y=10, width=200, height=680)

#         self.mid_col = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="#ffffff")
#         self.mid_col.place(x=220, y=10, width=620, height=680)

#         self.right_col = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="#ffffff")
#         self.right_col.place(x=850, y=10, width=340, height=680)

#         self.build_left()
#         self.build_mid()
#         self.build_right()
#         self.load_categories()
#         self.load_items(None)

#     # ---------- Left ----------
#     def build_left(self):
#         tk.Label(self.left_col, text="Categories", bg="#cfe2f3", font=("Arial", 12, "bold")).pack(fill="x")
#         self.cat_container = tk.Frame(self.left_col, bg="#f7f7f7")
#         self.cat_container.pack(fill="both", expand=True, padx=5, pady=5)

#         # Barcode Search
#         bar_frame = tk.Frame(self.left_col, bg="#f7f7f7")
#         bar_frame.pack(fill="x", padx=5, pady=5)
#         tk.Label(bar_frame, text="Barcode:", bg="#f7f7f7").pack(side="left")
#         self.barcode_entry = tk.Entry(bar_frame, width=12)
#         self.barcode_entry.pack(side="left", padx=5)
#         tk.Button(bar_frame, text="Add", command=self.search_barcode).pack(side="left")

#     def load_categories(self):
#         for w in self.cat_container.winfo_children():
#             w.destroy()
#         tk.Button(self.cat_container, text="All", width=18, anchor="w",
#                   command=lambda: self.load_items(None)).pack(pady=3)
#         for c in fetch_categories():
#             tk.Button(self.cat_container, text=c, width=18, anchor="w",
#                       command=lambda cat=c: self.load_items(cat)).pack(pady=3)

#     # ---------- Middle ----------
#     def build_mid(self):
#         tk.Label(self.mid_col, text="Items", bg="#ffffff", font=("Arial", 12, "bold")).pack(fill="x", padx=5, pady=5)
#         self.items_canvas = tk.Canvas(self.mid_col, bg="#ffffff")
#         self.items_scroll_y = ttk.Scrollbar(self.mid_col, orient="vertical", command=self.items_canvas.yview)
#         self.items_frame = tk.Frame(self.items_canvas, bg="#ffffff")
#         self.items_frame.bind("<Configure>", lambda e: self.items_canvas.configure(scrollregion=self.items_canvas.bbox("all")))
#         self.items_canvas.create_window((0, 0), window=self.items_frame, anchor="nw")
#         self.items_canvas.configure(yscrollcommand=self.items_scroll_y.set)
#         self.items_canvas.pack(side="left", fill="both", expand=True)
#         self.items_scroll_y.pack(side="right", fill="y")

#     def load_items(self, category=None):
#         for w in self.items_frame.winfo_children():
#             w.destroy()
#         prods = fetch_products_by_category(category)
#         for p in prods:
#             card = tk.Frame(self.items_frame, bd=1, relief="solid", bg="#fafafa")
#             card.pack(fill="x", padx=6, pady=6)

#             # Image
#             img_path = os.path.join(IMAGE_FOLDER, p["image"])
#             try:
#                 img = Image.open(img_path)
#                 img = img.resize((70, 70))
#                 photo = ImageTk.PhotoImage(img)
#             except Exception:
#                 img = Image.new("RGB", (70, 70), "gray")
#                 photo = ImageTk.PhotoImage(img)
#             tk.Label(card, image=photo, bg="#fafafa").pack(side="left", padx=5)
#             self.thumb_cache[p["image"]] = photo

#             # Details
#             d = tk.Frame(card, bg="#fafafa")
#             d.pack(side="left", fill="both", expand=True)
#             tk.Label(d, text=p["name"], bg="#fafafa", anchor="w", font=("Arial",10,"bold")).pack(fill="x")
#             tk.Label(d, text=f"Price: ₹{p['price']:.2f}", bg="#fafafa", anchor="w").pack(fill="x")

#             controls = tk.Frame(card, bg="#fafafa")
#             controls.pack(side="right", padx=6)
#             qty_var = tk.IntVar(value=1)
#             tk.Button(controls, text="-", width=2, command=lambda v=qty_var: v.set(max(1,v.get()-1))).pack(side="left")
#             tk.Label(controls, textvariable=qty_var, width=3).pack(side="left")
#             tk.Button(controls, text="+", width=2, command=lambda v=qty_var: v.set(v.get()+1)).pack(side="left")
#             tk.Button(controls, text="Add", bg="#4CAF50", fg="white",
#                       command=lambda prod=p, v=qty_var: self.add_to_cart(prod, v.get())).pack(side="left", padx=5)

#     # ---------- Right ----------
#     def build_right(self):
#         tk.Label(self.right_col, text="Bill / Cart", font=("Arial",12,"bold"), bg="#ffffff").pack(pady=5)
#         cols = ("name","price","qty","total")
#         self.cart_tree = ttk.Treeview(self.right_col, columns=cols, show="headings", height=18)
#         for c, w in zip(cols, [130,60,40,70]):
#             self.cart_tree.heading(c, text=c.capitalize())
#             self.cart_tree.column(c, width=w, anchor="center")
#         self.cart_tree.pack(fill="both", padx=6, pady=6)
#         self.cart_tree.bind("<Double-1>", self.on_cart_double_click)

#         self.lbl_total = tk.Label(self.right_col, text="Total: ₹0.00", bg="#ffffff", font=("Arial",10,"bold"))
#         self.lbl_total.pack(pady=3)
#         tk.Button(self.right_col, text="Download Bill (PDF)", bg="#4CAF50", fg="white", command=self.download_pdf).pack(fill="x", padx=6, pady=3)
#         tk.Button(self.right_col, text="Clear Cart", bg="#FF9800", fg="white", command=self.clear_cart).pack(fill="x", padx=6, pady=3)

#     # ---------- Cart ----------
#     def add_to_cart(self, product, qty):
#         name, price = product["name"], float(product["price"])
#         for it in self.cart:
#             if it["name"] == name:
#                 it["qty"] += qty
#                 break
#         else:
#             self.cart.append({"name": name, "price": price, "qty": qty})
#         self.refresh_cart()

#     def refresh_cart(self):
#         for row in self.cart_tree.get_children():
#             self.cart_tree.delete(row)
#         total = 0
#         for it in self.cart:
#             subtotal = it["price"] * it["qty"]
#             total += subtotal
#             self.cart_tree.insert("", "end", values=(it["name"], f"₹{it['price']:.2f}", it["qty"], f"₹{subtotal:.2f}"))
#         self.lbl_total.config(text=f"Total: ₹{total:.2f}")

#     def clear_cart(self):
#         self.cart = []
#         self.refresh_cart()

#     # ---------- Edit Quantity ----------
#     def on_cart_double_click(self, event):
#         item_id = self.cart_tree.identify_row(event.y)
#         if not item_id:
#             return
#         idx = self.cart_tree.index(item_id)
#         popup = tk.Toplevel(self.root)
#         popup.title("Edit Quantity")
#         tk.Label(popup, text=f"Edit quantity for {self.cart[idx]['name']}").pack(pady=5)
#         var = tk.IntVar(value=self.cart[idx]["qty"])
#         ent = tk.Entry(popup, textvariable=var, width=5)
#         ent.pack()
#         tk.Button(popup, text="Save", command=lambda:self.save_qty(idx, var, popup)).pack(pady=5)

#     def save_qty(self, idx, var, popup):
#         try:
#             val = int(var.get())
#             if val <= 0:
#                 self.cart.pop(idx)
#             else:
#                 self.cart[idx]["qty"] = val
#             self.refresh_cart()
#             popup.destroy()
#         except:
#             messagebox.showerror("Invalid", "Enter valid quantity.")

#     # ---------- PDF ----------
#     def download_pdf(self):
#         if not self.cart:
#             messagebox.showwarning("Empty", "No items in cart.")
#             return
#         file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")],
#                                                 initialfile=f"Bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
#         if not file_path:
#             return
#         self.generate_pdf(file_path)
#         messagebox.showinfo("Success", f"Bill saved to:\n{file_path}")

#     def generate_pdf(self, path):
#         c = canvas.Canvas(path, pagesize=A4)
#         width, height = A4
#         c.setFont("Helvetica-Bold", 14)
#         c.drawString(30*mm, height - 20*mm, "Shop Billing System")
#         c.setFont("Helvetica", 9)
#         c.drawString(30*mm, height - 26*mm, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

#         data = [["Item", "Qty", "Price", "Total"]]
#         total = 0
#         for it in self.cart:
#             subtotal = it["price"] * it["qty"]
#             total += subtotal
#             data.append([it["name"], str(it["qty"]), f"{it['price']:.2f}", f"{subtotal:.2f}"])
#         tax = total * 0.05
#         grand = total + tax
#         data.append(["", "", "Tax (5%)", f"{tax:.2f}"])
#         data.append(["", "", "Grand Total", f"{grand:.2f}"])

#         table = Table(data, colWidths=[80*mm, 25*mm, 25*mm, 30*mm])
#         style = TableStyle([
#             ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
#             ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
#             ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
#             ('ALIGN', (1,1), (-1,-1), 'CENTER'),
#         ])
#         table.setStyle(style)
#         table.wrapOn(c, width, height)
#         table.drawOn(c, 25*mm, height - 120*mm)
#         c.save()

#     def search_barcode(self):
#         code = self.barcode_entry.get().strip()
#         if not code:
#             return
#         prod = get_product_by_barcode(code)
#         if not prod:
#             messagebox.showinfo("Not Found", "Barcode not found.")
#             return
#         self.add_to_cart(prod, 1)
#         self.barcode_entry.delete(0, tk.END)

# # ---------------------- Run ----------------------
# if __name__ == "__main__":
#     os.makedirs(IMAGE_FOLDER, exist_ok=True)
#     init_db()
#     root = tk.Tk()
#     app = POSApp(root)
#     root.mainloop()




# pos_system.py
# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# from PIL import Image, ImageTk
# import sqlite3
# import os
# from datetime import datetime
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.units import mm
# from reportlab.pdfgen import canvas
# from reportlab.platypus import Table, TableStyle

# DB_FILE = "pos_system.db"
# IMAGE_FOLDER = "images"

# SAMPLE_PRODUCTS = [
#     ("89450000937", "Coke", "SoftDrink", 35, 49.00, "coke.png"),
#     ("89450000938", "Pepsi", "SoftDrink", 35, 49.00, "pepsi.png"),
#     ("89450000939", "7 Up", "SoftDrink", 35, 49.00, "7up.png"),
#     ("89400000012", "Grilled Chicken", "Food", 30, 150.00, "grilled_chicken.png"),
#     ("89234500012", "Chicken Burger", "Burger", 50, 99.00, "chicken_burger.png"),
#     ("89234500013", "Veg Burger", "Burger", 45, 89.00, "veg_burger.png"),
#     ("89400000027", "Coffee", "Drink", 100, 49.00, "coffee.png"),
#     ("89400000028", "Milk", "Drink", 200, 39.00, "milk.png"),
#     ("89400000017", "Chicken Biryani", "Food", 40, 125.00, "chicken_biryani.png"),
#     ("89400000021", "Strawberry 400g", "Fruit", 20, 125.00, "strawberry.png"),
#     ("89400000024", "Apple 400gm", "Fruit", 24, 49.00, "apple.png"),
# ]

# # ---------------------- Database Setup ----------------------
# def init_db():
#     first_time = not os.path.exists(DB_FILE)
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS products (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             barcode TEXT UNIQUE,
#             name TEXT,
#             category TEXT,
#             qty INTEGER,
#             price REAL,
#             image_path TEXT
#         )
#     """)
#     conn.commit()
#     if first_time:
#         for (barcode, name, category, qty, price, image) in SAMPLE_PRODUCTS:
#             try:
#                 c.execute("INSERT INTO products (barcode,name,category,qty,price,image_path) VALUES (?,?,?,?,?,?)",
#                           (barcode, name, category, qty, price, image))
#             except Exception:
#                 pass
#         conn.commit()
#     conn.close()

# def fetch_categories():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT DISTINCT category FROM products")
#     rows = [r[0] for r in c.fetchall()]
#     conn.close()
#     return rows

# def fetch_products_by_category(category=None):
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     if category:
#         c.execute("SELECT barcode,name,category,qty,price,image_path FROM products WHERE category=?", (category,))
#     else:
#         c.execute("SELECT barcode,name,category,qty,price,image_path FROM products")
#     rows = c.fetchall()
#     conn.close()
#     return [{"barcode":r[0],"name":r[1],"category":r[2],"qty":r[3],"price":r[4],"image":r[5]} for r in rows]

# def get_product_by_barcode(barcode):
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT barcode,name,category,qty,price,image_path FROM products WHERE barcode=?", (barcode,))
#     r = c.fetchone()
#     conn.close()
#     if r:
#         return {"barcode":r[0],"name":r[1],"category":r[2],"qty":r[3],"price":r[4],"image":r[5]}
#     return None

# # ---------------------- Main App ----------------------
# class POSApp:
#     def __init__(self, root):
#         self.root = root
#         root.title("POS Billing System")
#         root.geometry("1200x700")
#         root.configure(bg="#f0f0f0")

#         self.cart = []
#         self.thumb_cache = {}

#         # Layout Frames
#         self.left_col = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="#f7f7f7")
#         self.left_col.place(x=10, y=10, width=200, height=680)

#         self.mid_col = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="#ffffff")
#         self.mid_col.place(x=220, y=10, width=620, height=680)

#         self.right_col = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="#ffffff")
#         self.right_col.place(x=850, y=10, width=340, height=680)

#         self.build_left()
#         self.build_mid()
#         self.build_right()
#         self.load_categories()
#         self.load_items(None)

#     # ---------- Left ----------
#     def build_left(self):
#         tk.Label(self.left_col, text="Categories", bg="#cfe2f3", font=("Arial", 12, "bold")).pack(fill="x")
#         self.cat_container = tk.Frame(self.left_col, bg="#f7f7f7")
#         self.cat_container.pack(fill="both", expand=True, padx=5, pady=5)

#         # Barcode Search
#         bar_frame = tk.Frame(self.left_col, bg="#f7f7f7")
#         bar_frame.pack(fill="x", padx=5, pady=5)
#         tk.Label(bar_frame, text="Barcode:", bg="#f7f7f7").pack(side="left")
#         self.barcode_entry = tk.Entry(bar_frame, width=12)
#         self.barcode_entry.pack(side="left", padx=5)
#         tk.Button(bar_frame, text="Add", command=self.search_barcode).pack(side="left")

#     def load_categories(self):
#         for w in self.cat_container.winfo_children():
#             w.destroy()
#         tk.Button(self.cat_container, text="All", width=18, anchor="w",
#                   command=lambda: self.load_items(None)).pack(pady=3)
#         for c in fetch_categories():
#             tk.Button(self.cat_container, text=c, width=18, anchor="w",
#                       command=lambda cat=c: self.load_items(cat)).pack(pady=3)

#     # ---------- Middle ----------
#     def build_mid(self):
#         tk.Label(self.mid_col, text="Items", bg="#ffffff", font=("Arial", 12, "bold")).pack(fill="x", padx=5, pady=5)
#         self.items_canvas = tk.Canvas(self.mid_col, bg="#ffffff")
#         self.items_scroll_y = ttk.Scrollbar(self.mid_col, orient="vertical", command=self.items_canvas.yview)
#         self.items_frame = tk.Frame(self.items_canvas, bg="#ffffff")
#         self.items_frame.bind("<Configure>", lambda e: self.items_canvas.configure(scrollregion=self.items_canvas.bbox("all")))
#         self.items_canvas.create_window((0, 0), window=self.items_frame, anchor="nw")
#         self.items_canvas.configure(yscrollcommand=self.items_scroll_y.set)
#         self.items_canvas.pack(side="left", fill="both", expand=True)
#         self.items_scroll_y.pack(side="right", fill="y")

#     def load_items(self, category=None):
#         for w in self.items_frame.winfo_children():
#             w.destroy()
#         prods = fetch_products_by_category(category)
#         for p in prods:
#             card = tk.Frame(self.items_frame, bd=1, relief="solid", bg="#fafafa")
#             card.pack(fill="x", padx=6, pady=6)

#             # ---------- Image ----------
#             img_path = os.path.join(IMAGE_FOLDER, p["image"])
#             try:
#                 img = Image.open(img_path)
#                 img = img.resize((70, 70), Image.ANTIALIAS)
#                 photo = ImageTk.PhotoImage(img)
#             except Exception:
#                 img = Image.new("RGB", (70, 70), "gray")
#                 photo = ImageTk.PhotoImage(img)

#             img_label = tk.Label(card, image=photo, bg="#fafafa")
#             img_label.image = photo  # Keep reference to prevent GC
#             img_label.pack(side="left", padx=5)
#             self.thumb_cache[p["image"]] = photo

#             # ---------- Details ----------
#             d = tk.Frame(card, bg="#fafafa")
#             d.pack(side="left", fill="both", expand=True)
#             tk.Label(d, text=p["name"], bg="#fafafa", anchor="w", font=("Arial",10,"bold")).pack(fill="x")
#             tk.Label(d, text=f"Price: ₹{p['price']:.2f}", bg="#fafafa", anchor="w").pack(fill="x")

#             # ---------- Controls ----------
#             controls = tk.Frame(card, bg="#fafafa")
#             controls.pack(side="right", padx=6)
#             qty_var = tk.IntVar(value=1)
#             tk.Button(controls, text="-", width=2, command=lambda v=qty_var: v.set(max(1,v.get()-1))).pack(side="left")
#             tk.Label(controls, textvariable=qty_var, width=3).pack(side="left")
#             tk.Button(controls, text="+", width=2, command=lambda v=qty_var: v.set(v.get()+1)).pack(side="left")
#             tk.Button(controls, text="Add", bg="#4CAF50", fg="white",
#                       command=lambda prod=p, v=qty_var: self.add_to_cart(prod, v.get())).pack(side="left", padx=5)

#     # ---------- Right ----------
#     def build_right(self):
#         tk.Label(self.right_col, text="Bill / Cart", font=("Arial",12,"bold"), bg="#ffffff").pack(pady=5)
#         cols = ("name","price","qty","total")
#         self.cart_tree = ttk.Treeview(self.right_col, columns=cols, show="headings", height=18)
#         for c, w in zip(cols, [130,60,40,70]):
#             self.cart_tree.heading(c, text=c.capitalize())
#             self.cart_tree.column(c, width=w, anchor="center")
#         self.cart_tree.pack(fill="both", padx=6, pady=6)
#         self.cart_tree.bind("<Double-1>", self.on_cart_double_click)

#         self.lbl_total = tk.Label(self.right_col, text="Total: ₹0.00", bg="#ffffff", font=("Arial",10,"bold"))
#         self.lbl_total.pack(pady=3)
#         tk.Button(self.right_col, text="Download Bill (PDF)", bg="#4CAF50", fg="white", command=self.download_pdf).pack(fill="x", padx=6, pady=3)
#         tk.Button(self.right_col, text="Clear Cart", bg="#FF9800", fg="white", command=self.clear_cart).pack(fill="x", padx=6, pady=3)

#     # ---------- Cart ----------
#     def add_to_cart(self, product, qty):
#         name, price = product["name"], float(product["price"])
#         for it in self.cart:
#             if it["name"] == name:
#                 it["qty"] += qty
#                 break
#         else:
#             self.cart.append({"name": name, "price": price, "qty": qty})
#         self.refresh_cart()

#     def refresh_cart(self):
#         for row in self.cart_tree.get_children():
#             self.cart_tree.delete(row)
#         total = 0
#         for it in self.cart:
#             subtotal = it["price"] * it["qty"]
#             total += subtotal
#             self.cart_tree.insert("", "end", values=(it["name"], f"₹{it['price']:.2f}", it["qty"], f"₹{subtotal:.2f}"))
#         self.lbl_total.config(text=f"Total: ₹{total:.2f}")

#     def clear_cart(self):
#         self.cart = []
#         self.refresh_cart()

#     # ---------- Edit Quantity ----------
#     def on_cart_double_click(self, event):
#         item_id = self.cart_tree.identify_row(event.y)
#         if not item_id:
#             return
#         idx = self.cart_tree.index(item_id)
#         popup = tk.Toplevel(self.root)
#         popup.title("Edit Quantity")
#         tk.Label(popup, text=f"Edit quantity for {self.cart[idx]['name']}").pack(pady=5)
#         var = tk.IntVar(value=self.cart[idx]["qty"])
#         ent = tk.Entry(popup, textvariable=var, width=5)
#         ent.pack()
#         tk.Button(popup, text="Save", command=lambda:self.save_qty(idx, var, popup)).pack(pady=5)

#     def save_qty(self, idx, var, popup):
#         try:
#             val = int(var.get())
#             if val <= 0:
#                 self.cart.pop(idx)
#             else:
#                 self.cart[idx]["qty"] = val
#             self.refresh_cart()
#             popup.destroy()
#         except:
#             messagebox.showerror("Invalid", "Enter valid quantity.")

#     # ---------- PDF ----------
#     def download_pdf(self):
#         if not self.cart:
#             messagebox.showwarning("Empty", "No items in cart.")
#             return
#         file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")],
#                                                 initialfile=f"Bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
#         if not file_path:
#             return
#         self.generate_pdf(file_path)
#         messagebox.showinfo("Success", f"Bill saved to:\n{file_path}")

#     def generate_pdf(self, path):
#         c = canvas.Canvas(path, pagesize=A4)
#         width, height = A4
#         c.setFont("Helvetica-Bold", 14)
#         c.drawString(30*mm, height - 20*mm, "Shop Billing System")
#         c.setFont("Helvetica", 9)
#         c.drawString(30*mm, height - 26*mm, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

#         data = [["Item", "Qty", "Price", "Total"]]
#         total = 0
#         for it in self.cart:
#             subtotal = it["price"] * it["qty"]
#             total += subtotal
#             data.append([it["name"], str(it["qty"]), f"{it['price']:.2f}", f"{subtotal:.2f}"])
#         tax = total * 0.05
#         grand = total + tax
#         data.append(["", "", "Tax (5%)", f"{tax:.2f}"])
#         data.append(["", "", "Grand Total", f"{grand:.2f}"])

#         table = Table(data, colWidths=[80*mm, 25*mm, 25*mm, 30*mm])
#         style = TableStyle([
#             ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
#             ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
#             ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
#             ('ALIGN', (1,1), (-1,-1), 'CENTER'),
#         ])
#         table.setStyle(style)
#         table.wrapOn(c, width, height)
#         table.drawOn(c, 25*mm, height - 120*mm)
#         c.save()

#     def search_barcode(self):
#         code = self.barcode_entry.get().strip()
#         if not code:
#             return
#         prod = get_product_by_barcode(code)
#         if not prod:
#             messagebox.showinfo("Not Found", "Barcode not found.")
#             return
#         self.add_to_cart(prod, 1)
#         self.barcode_entry.delete(0, tk.END)

# # ---------------------- Run ----------------------
# if __name__ == "__main__":
#     os.makedirs(IMAGE_FOLDER, exist_ok=True)
#     init_db()
#     root = tk.Tk()
#     app = POSApp(root)
#     root.mainloop()





