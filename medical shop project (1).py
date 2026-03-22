import mysql.connector as ms
import datetime

# Database Connection
def connectDb():
    try:
        conn = ms.connect(
            host='localhost',
            user='root',
            passwd='mukti012',
            database='medical_inv',
            auth_plugin='mysql_native_password'
        )
        if conn.is_connected():
            return conn
    except ms.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

# Utility Functions
def drawLine(n=60):
    print("=" * n)

def today():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def reportTitle(title, n=60):
    drawLine(n)
    print(title.center(n))
    drawLine(n)

# Create Tables
def create_tables():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query1 = """
        CREATE TABLE IF NOT EXISTS Medicines (
            Medicine_ID INT AUTO_INCREMENT PRIMARY KEY,
            Medicine_Name VARCHAR(100),
            Manufacturer VARCHAR(100),
            Category VARCHAR(100),
            Price DECIMAL(10, 2),
            Quantity_In_Stock INT,
            Expiry_Date DATE
        )
        """
        query2 = """
        CREATE TABLE IF NOT EXISTS Purchase (
            Purchase_ID INT AUTO_INCREMENT PRIMARY KEY,
            Medicine_ID INT,
            Purchase_Date DATE,
            Quantity_Purchased INT,
            Purchase_Price DECIMAL(10, 2),
            Total_Amount DECIMAL(10, 2),
            FOREIGN KEY (Medicine_ID) REFERENCES Medicines(Medicine_ID)
        )
        """
        query3 = """
        CREATE TABLE IF NOT EXISTS Sales (
            Sale_ID INT AUTO_INCREMENT PRIMARY KEY,
            Medicine_ID INT,
            Sale_Date DATE,
            Quantity_Sold INT,
            Sale_Price DECIMAL(10, 2),
            Total_Sale_Amount DECIMAL(10, 2),
            FOREIGN KEY (Medicine_ID) REFERENCES Medicines(Medicine_ID)
        )
        """
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
        conn.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()

# Medicine Management
def addMedicine():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        reportTitle("ADD NEW MEDICINE")
        name = input('Name: ')
        manufacturer = input('Manufacturer: ')
        category = input('Category: ')
        price = float(input('Price: '))
        stock = int(input('Stock: '))
        expiry = input('Expiry (YYYY-MM-DD): ')
        sql = """INSERT INTO Medicines (Medicine_Name, Manufacturer, Category, Price, Quantity_In_Stock, Expiry_Date) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (name, manufacturer, category, price, stock, expiry))
        conn.commit()
        print("Medicine added successfully!")
    except Exception as e:
        print(f"Error adding medicine: {e}")
    finally:
        cursor.close()
        conn.close()

def viewMedicines():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        reportTitle("MEDICINE INVENTORY", 80)
        sql = "SELECT * FROM Medicines ORDER BY Medicine_Name"
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            print("%-5s %-20s %-15s %-12s %-8s %-10s %-10s" % (
                "ID", "Name", "Manufacturer", "Category", "Price", "Stock", "Expiry"))
            drawLine(80)
            for row in results:
                print("%-5d %-20s %-15s %-12s %-8.2f %-10d %s" % (
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        else:
            print("No medicines found.")
    except Exception as e:
        print(f"Error viewing medicines: {e}")
    finally:
        cursor.close()
        conn.close()

def updateMedicines():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        reportTitle("UPDATE MEDICINE")
        med_id = input("Enter Medicine ID: ")
        cursor.execute("SELECT * FROM Medicines WHERE Medicine_ID = %s", (med_id,))
        result = cursor.fetchone()
        if not result:
            print("Medicine not found!")
            return

        print("Current Details:")
        print(f"1. Name: {result[1]}")
        print(f"2. Price: {result[4]}")
        print(f"3. Stock: {result[5]}")
        choice = input("Enter the field to update (1-3): ")
        if choice == "1":
            new_value = input("Enter new name: ")
            sql = "UPDATE Medicines SET Medicine_Name = %s WHERE Medicine_ID = %s"
        elif choice == "2":
            new_value = float(input("Enter new price: "))
            sql = "UPDATE Medicines SET Price = %s WHERE Medicine_ID = %s"
        elif choice == "3":
            new_value = int(input("Enter new stock: "))
            sql = "UPDATE Medicines SET Quantity_In_Stock = %s WHERE Medicine_ID = %s"
        else:
            print("Invalid choice!")
            return
        cursor.execute(sql, (new_value, med_id))
        conn.commit()
        print("Medicine updated successfully!")
    except Exception as e:
        print(f"Error updating medicine: {e}")
    finally:
        cursor.close()
        conn.close()
        
def searchMedicine():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        reportTitle("SEARCH MEDICINE")
        print("1. By ID")
        print("2. By Name")
        choice = int(input("Enter choice: "))
        
        if choice == 1:
            med_id = input("Enter Medicine ID: ")
            sql = "SELECT * FROM Medicines WHERE Medicine_ID = %s"
            cursor.execute(sql, (med_id,))
        elif choice == 2:
            name = input("Enter Medicine Name: ")
            sql = "SELECT * FROM Medicines WHERE Medicine_Name LIKE %s"
            cursor.execute(sql, (f"%{name}%",))
        else:
            print("Invalid choice!")
            return
        
        result = cursor.fetchone()
        if result:
            print("\nMedicine Details:")
            print(f"ID: {result[0]}")
            print(f"Name: {result[1]}")
            print(f"Manufacturer: {result[2]}")
            print(f"Category: {result[3]}")
            print(f"Price: {result[4]}")
            print(f"Stock: {result[5]}")
            print(f"Expiry: {result[6]}")
        else:
            print("Medicine not found!")
    except Exception as e:
        print(f"Error searching medicine: {e}")
    finally:
        cursor.close()
        conn.close()

# Record Transactions
def recordPurchase():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        reportTitle("RECORD PURCHASE")
        med_id = input("Medicine ID: ")
        cursor.execute("SELECT * FROM Medicines WHERE Medicine_ID = %s", (med_id,))
        if not cursor.fetchone():
            print("Error: Medicine ID does not exist.")
            return

        quantity = int(input("Quantity Purchased: "))
        price = float(input("Purchase Price per Unit: "))
        total = quantity * price
        sql_insert = """INSERT INTO Purchase (Medicine_ID, Purchase_Date, Quantity_Purchased, 
                         Purchase_Price, Total_Amount) VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql_insert, (med_id, today(), quantity, price, total))

        sql_update = "UPDATE Medicines SET Quantity_In_Stock = Quantity_In_Stock + %s WHERE Medicine_ID = %s"
        cursor.execute(sql_update, (quantity, med_id))
        conn.commit()
        print("Purchase recorded successfully!")
    except Exception as e:
        print(f"Error recording purchase: {e}")
    finally:
        cursor.close()
        conn.close()

def recordSale():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        reportTitle("RECORD SALE")
        med_id = input("Medicine ID: ")
        cursor.execute("SELECT * FROM Medicines WHERE Medicine_ID = %s", (med_id,))
        result = cursor.fetchone()
        if not result:
            print("Error: Medicine ID does not exist.")
            return

        print(f"Available Stock: {result[5]}")
        print(f"Price: {result[4]}")
        quantity = int(input("Quantity to Sell: "))
        if quantity > result[5]:
            print("Insufficient stock!")
            return

        total = quantity * result[4]
        sql_insert = """INSERT INTO Sales (Medicine_ID, Sale_Date, Quantity_Sold, 
                         Sale_Price, Total_Sale_Amount) VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql_insert, (med_id, today(), quantity, result[4], total))

        sql_update = "UPDATE Medicines SET Quantity_In_Stock = Quantity_In_Stock - %s WHERE Medicine_ID = %s"
        cursor.execute(sql_update, (quantity, med_id))
        conn.commit()
        print("Sale recorded successfully!")
    except Exception as e:
        print(f"Error recording sale: {e}")
    finally:
        cursor.close()
        conn.close()
        
def dailySalesReport():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        reportTitle("DAILY SALES REPORT")
        date = input("Enter Date (YYYY-MM-DD) or press Enter for today: ") or today()
        
        sql = """SELECT m.Medicine_Name, s.Quantity_Sold, s.Sale_Price, s.Total_Sale_Amount 
                 FROM Sales s JOIN Medicines m ON s.Medicine_ID = m.Medicine_ID 
                 WHERE s.Sale_Date = %s"""
        cursor.execute(sql, (date,))
        results = cursor.fetchall()
        
        if results:
            print(f"\nSales for {date}")
            print("%-25s %-10s %-10s %-10s" % ("Medicine", "Quantity", "Price", "Total"))
            drawLine(80)
            total_sales = 0
            for row in results:
                print("%-25s %-10d %-10.2f %-10.2f" % (row[0], row[1], row[2], row[3]))
                total_sales += row[3]
            drawLine(80)
            print(f"Total Sales: Rs. {total_sales:.2f}")
        else:
            print(f"No sales recorded for {date}.")
    except Exception as e:
        print(f"Error generating daily sales report: {e}")
    finally:
        cursor.close()
        conn.close()
        
def dailyPurchaseReport():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        reportTitle("DAILY PURCHASE REPORT")
        date = input("Enter Date (YYYY-MM-DD) or press Enter for today: ") or today()
        
        sql = """SELECT m.Medicine_Name, p.Quantity_Purchased, p.Purchase_Price, p.Total_Amount 
                 FROM Purchase p JOIN Medicines m ON p.Medicine_ID = m.Medicine_ID 
                 WHERE p.Purchase_Date = %s"""
        cursor.execute(sql, (date,))
        results = cursor.fetchall()
        
        if results:
            print(f"\nPurchases for {date}")
            print("%-25s %-10s %-10s %-10s" % ("Medicine", "Quantity", "Price", "Total"))
            drawLine(80)
            total_purchases = 0
            for row in results:
                print("%-25s %-10d %-10.2f %-10.2f" % (row[0], row[1], row[2], row[3]))
                total_purchases += row[3]
            drawLine(80)
            print(f"Total Purchases: Rs. {total_purchases:.2f}")
        else:
            print(f"No purchases recorded for {date}.")
    except Exception as e:
        print(f"Error generating daily purchase report: {e}")
    finally:
        cursor.close()
        conn.close()

def expiringMedicinesReport():
    conn = connectDb()
    cursor = conn.cursor()
    reportTitle("EXPIRING MEDICINES REPORT", 80)
    days = int(input("Show medicines expiring in how many days? "))
    
    sql = """SELECT * FROM Medicines
             WHERE Expiry_Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
             ORDER BY Expiry_Date"""
    cursor.execute(sql, (days,))
    results = cursor.fetchall()
    
    if results:
        print("%-5s %-20s %-15s %-12s %-10s" %
              ("ID", "Name", "Category", "Stock", "Expiry"))
        drawLine(80)
        
        for row in results:
            print("%-5d %-20s %-15s %-12d %s" %
                  (row[0], row[1], row[3], row[5], row[6]))
    else:
        print(f"No medicines expiring in the next {days} days")
    conn.commit()
    
def lowStockAlert():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        reportTitle("LOW STOCK ALERT")
        threshold = int(input("Enter stock threshold for alert: "))
        
        sql = "SELECT Medicine_ID, Medicine_Name, Quantity_In_Stock FROM Medicines WHERE Quantity_In_Stock <= %s ORDER BY Quantity_In_Stock"
        cursor.execute(sql, (threshold,))
        results = cursor.fetchall()
        
        if results:
            print("\nMedicines with low stock:")
            print("%-5s %-25s %-10s" % ("ID", "Medicine", "Stock"))
            drawLine(80)
            for row in results:
                print("%-5d %-25s %-10d" % (row[0], row[1], row[2]))
            print("\nPlease reorder these medicines soon!")
        else:
            print(f"No medicines below threshold of {threshold} units.")
    except Exception as e:
        print(f"Error generating low stock alert: {e}")
    finally:
        cursor.close()
        conn.close()

# Admin Login
def admin_login():
    username = input("Admin Username: ")
    password = input("Admin Password: ")
    if username == "admin1" and password == "adminpass":
        print("Logged in successfully as admin!")
        return True
    else:
        print("Invalid credentials!")
        return False

# Guest Menu
def guest_menu():
    conn = connectDb()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        while True:
            print("\nGuest Menu:")
            print("1. Display All Medicines")
            print("2. Search Medicines")
            print("0. Exit to Main Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                viewMedicines()
            elif choice == "2":
                searchMedicine()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"Error in guest menu: {e}")
    finally:
        conn.close()

# Admin Menu
def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("0. Logout")
        print("1. Add Medicine")
        print("2. View Medicines")
        print("3. Update Medicine")
        print("4. Search Medicine")
        print("5. Record Purchase")
        print("6. Record Sale")
        print("7. Daily Sales Report")
        print("8. Daily Purchase Report")
        print("9. Expiring Medicines")
        print("10.Low Stock Alert")
        choice = input("Enter your choice: ")
        if choice == "0":
            print("Logging out...")
            break      
        elif choice == "1":
            addMedicine()
        elif choice == "2":
            viewMedicines()
        elif choice == "3":
            updateMedicines()
        elif choice == "4":
            searchMedicine()
        elif choice == "5":
            recordPurchase()
        elif choice == "6":
            recordSale()
        elif choice == "7":
            dailySalesReport()
        elif choice == "8":
            dailyPurchaseReport()
        elif choice == "9":
            expiringMedicinesReport()
        elif choice =="10":
            lowStockAlert()
        else:
            print("Invalid choice. Please try again.")
            
# Main Function
def main():
    create_tables()
    while True:
        print("\nMain Menu:")
        print("0. Exit")
        print("1. Admin Login")
        print("2. Guest")
        choice = input("Enter your choice: ")
        if choice == "1":
            if admin_login():
                admin_menu()
        elif choice == "2":
            guest_menu()
        elif choice == "0":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
