# MINI PROJECT - INVENTORY MANAGEMENT SYSTEM using sqlite3

import sqlite3
from datetime import datetime

def draw_table(headers, rows):
    col_widths = [len(h) for h in headers]

    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def line():
        total_width = sum(col_widths) + (3 * len(col_widths)) + 1
        return "-" *total_width

    def format_row(row):
        return "| " + " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + "|"

    print(line())
    print(format_row(headers))
    print(line())

    for row in rows:
        print(format_row(row))
    print(line())


# ========== DATABASE SETUP ==========
conn = sqlite3.connect('Inventory.db')
cursor = conn.cursor()

# Create Users Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name VARCHAR(20) UNIQUE NOT NULL,
        password VARCHAR(20) NOT NULL,
        contact TEXT,
        role VARCHAR(20) NOT NULL)
    ''')

# Create Categories Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE)
    ''')

# Create Products Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL,
        status TEXT,
        stock_quantity INTEGER,
        supplier_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY(supplier_id) REFERENCES Users(user_id),
        FOREIGN KEY(category_id) REFERENCES Categories(category_id)
        )
    ''')

# Create Transactions (Sales and Purchases) Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales(
        sales_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('IN','OUT')),
        quantity_change INTEGER NOT NULL,
        date_time TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(product_id) REFERENCES Products(product_id),
        FOREIGN KEY(user_id) REFERENCES Users(user_id)
        )
    ''')

conn.commit()
conn.close()

# ========== USER AUTHENTICATION ==========
def register_user():
    try:
        print('\n---------User Registration ---------')
        conn = sqlite3.connect('Inventory.db')
        cursor = conn.cursor()

        user_name = input('Enter username: ')
        password = input('Enter password: ')
        contact = input('Enter contact number: ')
        role = input('Enter role (Admin/Supplier): ')

        cursor.execute('SELECT * FROM Users WHERE user_name = ?', (user_name,))
        if cursor.fetchone():
            print('⚠️ Username already exists!')
            return

        cursor.execute('INSERT INTO Users(user_name,password,contact,role) VALUES(?,?,?,?)',
                       (user_name, password, contact, role))
        conn.commit()
        conn.close()
        print("------------------------------------------------------")
        print('\n✅ User registered successfully!')

    except Exception as e:
        print("------------------------------------------------------")
        print('❌ Error:', e)

def login_user():
    try:
        conn = sqlite3.connect('Inventory.db')
        cursor = conn.cursor()

        print('\n------ User Login ------')
        user_name = input('Enter username: ')
        password = input('Enter password: ')

        cursor.execute('SELECT * FROM Users WHERE user_name=? AND password=?', (user_name, password))
        user = cursor.fetchone()

        if user:
            print("------------------------------------------------------")
            print(f'\n✅ Login successful!! Welcome, {user_name} ({user[4]})')
            return user
        else:
            print("------------------------------------------------------")
            print('❌ Invalid credentials.')
            return None
    except Exception as e:
        print("------------------------------------------------------")
        print(f'Error: {e}')
        return None
    finally:
        if conn:
            conn.close()

def view_users(user):
    try:
        if user[4] != 'Admin':
            print("------------------------------------------------------")
            print('❌Only Admin can view all users.')
            return
    
        conn = sqlite3.connect('Inventory.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, user_name, role, contact FROM Users')
        rows = cursor.fetchall()
    except Exception as e:
        print("------------------------------------------------------")
        print(f'Error occured:{e}')
    conn.close()

    print('\n--------------- USERS ----------------') 
    draw_table(["ID","Username","Role","Contact"],rows)

# ========== CATEGORY OPERATIONS ==========
def add_category():
    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()
    name = input('Enter category name: ')
    try:
        cursor.execute('INSERT INTO Categories(category_name) VALUES(?)', (name,))
        conn.commit()
        print("------------------------------------------------------")
        print(f'\n✅ Category {name} added!')
    except sqlite3.IntegrityError:
        print("------------------------------------------------------")
        print('\n⚠️ Category already exists.')
    conn.close()

def view_categories():
    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Categories")
    rows = cursor.fetchall()
    conn.close()

    print("\n-------------- CATEGORIES ----------------")
    draw_table(["ID","Category Name"], rows)

def delete_category(user):
    if user[4] != 'Admin':
        print("------------------------------------------------------")
        print('\n❌Only Admin can delete Categories.')
        return
    
    view_categories() 
    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()
    try:
        cat_id = int(input('Enter Category ID to delete: '))
    except ValueError:
        print("------------------------------------------------------")
        print(f'\n❌Invalid input! Category ID must be a number.')
        conn.close()
        return

    cursor.execute('SELECT category_name FROM Categories WHERE category_id = ?', (cat_id,))
    category_data = cursor.fetchone()
    
    if not category_data:
        print("------------------------------------------------------")
        print('\n⚠️ Category not found.')
        conn.close()
        return

    category_name = category_data[0] 
    cursor.execute('''DELETE FROM Categories WHERE category_id = ?''',
                    (cat_id,))
    conn.commit()
    conn.close()
    print("------------------------------------------------------")
    print(f'\n🗑️  Category "{category_name}" (ID: {cat_id}) deleted successfully!')
# ========== PRODUCT OPERATIONS ==========
def add_product():
    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()
    name = input('Enter product name: ')
    price = float(input('Enter price: '))
    quantity = int(input('Enter stock quantity: '))
    supplier_id = int(input('Enter supplier ID: '))
    category_id = int(input('Enter category ID: '))
    status = "Available" if quantity > 5 else "Limited stock"

    try:
        cursor.execute('''INSERT INTO Products(product_name, price, status, stock_quantity, supplier_id, category_id)
                          VALUES(?,?,?,?,?,?)''', (name, price, status, quantity, supplier_id, category_id))
        conn.commit()
        print("------------------------------------------------------")
        print('\n✅ Product {product_name} added successfully!')
    except sqlite3.IntegrityError:
        print("------------------------------------------------------")
        print('\n⚠️ Product {product_name} already exists.')
    conn.close()

def view_products(user):

    if user[4] != 'Admin':
        print("------------------------------------------------------")
        print('\n❌ Only Admin can view all products.')
        return
    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT product_id, product_name, price, stock_quantity, status FROM Products')
    rows = cursor.fetchall()
    conn.close()

    print("\n------------------- PRODUCTS ---------------------")
    draw_table(["ID","Product","Price","Qty","Status"], rows)

def view_supplier_products(user):
    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT product_id,product_name,price,stock_quantity,status FROM Products WHERE supplier_id = ?
                   ''',(user[0],))

    products = cursor.fetchall()
    if not products:
        print("------------------------------------------------------")
        print('\n❌  No products found under your ID.')
    else:
        print('\n-------------Products(Supplier View)-------------')
        draw_table(["ID","Product","Price","Qty","Status"], products)
    conn.close()

def delete_product(user):
    if user[4] != 'Admin':
        print("------------------------------------------------------")
        print('\n❌Only Admin can delete products.')
        return
    print("------------------------------------------------------")
    print('\n 📦 Products Available for Deletion\n')
    view_products()

    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()
    try:
        prod_id = int(input('Enter product ID to delete: '))
    except ValueError:
        print("------------------------------------------------------")
        print('\n❌Invalid input. Product ID must be a number.')
        conn.close()
        return

    cursor.execute('SELECT product_name FROM Products WHERE product_id = ?', (prod_id,))
    product_data = cursor.fetchone()
   
    if not product_data:
        print("------------------------------------------------------")
        print('\n❌Product not found.')
        conn.close()
        return
    product_name = product_data[0] 
    cursor.execute('''DELETE FROM Products WHERE product_id = ?''',
                    (prod_id,))
    
    conn.commit()
    conn.close()
    print("------------------------------------------------------")
    print(f'\n🗑️  Product "{product_name}" (ID: {prod_id}) deleted successfully!')

# ========== STOCK ALERT SYSTEM ==========
def check_low_stock(user): #Alert user when stock ≤ 5
    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()

#Check if the user is a supplier 
    if user[4] == 'Supplier':
        cursor.execute('''SELECT product_name,stock_quantity FROM Products WHERE supplier_id = ? AND stock_quantity <= 5
                       ''',(user[0],))
    else:
        cursor.execute('SELECT product_name, stock_quantity FROM Products WHERE stock_quantity <= 5')
    
    low_stock = cursor.fetchall()
    conn.close()
    print("------------------------------------------------------")
    print(f"\n Low Stock Query Result: {low_stock}")

    if low_stock:
        print("\n⚠️ 🚨 LOW STOCK ALERT 🚨 ⚠️")

        headers = ["Product Name", "Quantity Left"]
        draw_table(headers, low_stock) 
        print("-----------------------------------------------")
        print("Please place orders for these items immediately.")
    else:
        print("\n✅ All stock levels are sufficient.")

# ========== INVENTORY MOVEMENTS ==========
def record_purchase(user):  #Add stock (IN transaction)
    
    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()

    product_id = int(input('Enter product ID: '))
    qty = int(input('Enter quantity purchased: '))

    cursor.execute('SELECT stock_quantity FROM Products WHERE product_id = ?', (product_id,))
    result = cursor.fetchone()
    if not result:
        print("------------------------------------------------------")
        print('❌ Invalid product ID.')
        return

    new_stock = result[0] + qty
    cursor.execute('UPDATE Products SET stock_quantity=?, status=? WHERE product_id=?',
                   (new_stock, "Available", product_id))

    cursor.execute('''INSERT INTO Sales(product_id, type, quantity_change, date_time, user_id)
                      VALUES(?,?,?,?,?)''', (product_id, 'IN', qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user[0]))
    conn.commit()
    conn.close()
    print("------------------------------------------------------")
    print('✅ Purchase recorded (Stock increased)!')
    check_low_stock(user)  # check after update

def record_sale(user):  #Reduce stock (OUT transaction)
   
    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()

    product_id = int(input('Enter product ID: '))
    qty = int(input('Enter quantity sold: '))

    cursor.execute('SELECT stock_quantity FROM Products WHERE product_id=?', (product_id,))
    result = cursor.fetchone()
    if not result:
        print("------------------------------------------------------")
        print('❌ Invalid product ID.')
        return

    stock = result[0]
    if stock < qty:
        print("------------------------------------------------------")
        print('⚠️ Not enough stock available.')
        return

    new_stock = stock - qty
    cursor.execute('UPDATE Products SET stock_quantity=?, status=? WHERE product_id=?',
                   (new_stock, "Available" if new_stock > 0 else "Out of Stock", product_id))

    cursor.execute('''INSERT INTO Sales(product_id, type, quantity_change, date_time, user_id)
                      VALUES(?,?,?,?,?)''', (product_id, 'OUT', qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user[0]))
    conn.commit()
    conn.close()
    print("------------------------------------------------------")
    print('✅ Sale recorded (Stock decreased)!')
    check_low_stock(user)  # check after update

def view_sales():
    conn = sqlite3.connect('Inventory.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT sales_id, product_id, type, quantity_change, date_time 
                  FROM Sales ORDER BY date_time DESC''')
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("------------------------------------------------------")
        print('⚠️ No sales transactions found in the database.')
        return
    print('\n-------------------- TRANSACTION HISTORY -----------------------')
    headers = ["Sale ID", "Product ID", "Type", "Qty Change", "Timestamp"]
    draw_table(headers, rows)

# ================= MAIN MENU ===================
def main():
    
    while True:
        print('\n============== Main Menu ==============')
        print('1. Register User')
        print('2. Login')
        print('3. Exit')
        
        choice = input('\nEnter choice: ')

        if choice == '1':
            register_user()
        elif choice == '2':
            user = login_user()
            if user:
                while True:
                    print('\n==============INVENTORY MENU =================\n')
                    print('1. View Users (Admin Only)')
                    print('2. Add Category')
                    print('3. View Categories')
                    print('4. Add Product')
                    print('5. View All Products')
                    print('6. View my Products(Supplier Only)')
                    print('7. Record Purchase (Stock IN)')
                    print('8. Record Sale (Stock OUT)')
                    print('9. View All Transactions')
                    print('10. Check Low Stock')
                    print('11. Delete Category (Admin Only)')
                    print('12. Delete Product (Admin Only)')
                    print('13. Logout')
                    print('\n==========================================')
                    sub = input('\nEnter choice: ')

                    if sub == '1': view_users(user)
                    elif sub == '2': add_category()
                    elif sub == '3': view_categories()
                    elif sub == '4': add_product()
                    elif sub == '5': view_products(user)
                    elif sub == '6': view_supplier_products(user)
                    elif sub == '7': record_purchase(user)
                    elif sub == '8': record_sale(user)
                    elif sub == '9': view_sales()
                    elif sub == '10': check_low_stock(user)
                    elif sub == '11': delete_category(user)
                    elif sub == '12': delete_product(user)
                    elif sub == '13': break
                    else: print('Invalid choice.')
        
        elif choice == '3':
            print('👋 Goodbye!')
            break
        else:
            print('Invalid option.')

main()
