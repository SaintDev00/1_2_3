"""
Inventory and Sales Management System
Simplified version with all required features
"""

from datetime import datetime

# Pre-loaded inventory
inventory = {
    1: {"title": "One Hundred Years of Solitude", "author": "Gabriel García Márquez", "category": "Fiction", "price": 25.99, "stock": 15},
    2: {"title": "The Alchemist", "author": "Paulo Coelho", "category": "Fiction", "price": 18.50, "stock": 20},
    3: {"title": "Sapiens", "author": "Yuval Noah Harari", "category": "Non-Fiction", "price": 22.00, "stock": 12},
    4: {"title": "Educated", "author": "Tara Westover", "category": "Biography", "price": 19.99, "stock": 8},
    5: {"title": "Becoming", "author": "Michelle Obama", "category": "Biography", "price": 24.99, "stock": 10}
}

sales = []
next_id = 6

# ============ VALIDATION ============

def get_positive_num(msg, typ=float):
    """Get and validate positive number"""
    while True:
        try:
            val = typ(input(msg))
            if val > 0:
                return val
            print("Error: Must be positive")
        except:
            print("Error: Invalid input")

def get_text(msg):
    """Get and validate non-empty text"""
    while True:
        txt = input(msg).strip()
        if txt:
            return txt
        print("Error: Cannot be empty")

# ============ INVENTORY ============

def view_inventory():
    """Display all products"""
    print("\n" + "="*80)
    print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Price':<10} {'Stock':<8}")
    print("-"*80)
    for pid, p in inventory.items():
        print(f"{pid:<5} {p['title']:<30} {p['author']:<20} ${p['price']:<9.2f} {p['stock']:<8}")
    print("="*80)

def add_product():
    """Add new product"""
    global next_id
    print("\n=== ADD PRODUCT ===")
    try:
        inventory[next_id] = {
            "title": get_text("Title: "),
            "author": get_text("Author: "),
            "category": get_text("Category: "),
            "price": get_positive_num("Price: $"),
            "stock": int(get_positive_num("Stock: ", int))
        }
        print(f"✓ Product added with ID: {next_id}")
        next_id += 1
    except Exception as e:
        print(f"Error: {e}")

def update_product():
    """Update existing product"""
    view_inventory()
    try:
        pid = int(input("\nProduct ID to update: "))
        if pid not in inventory:
            print("Error: Product not found")
            return
        
        p = inventory[pid]
        print(f"Updating: {p['title']} (press Enter to skip)")
        
        title = input(f"Title [{p['title']}]: ").strip()
        if title: p['title'] = title
        
        author = input(f"Author [{p['author']}]: ").strip()
        if author: p['author'] = author
        
        price = input(f"Price [${p['price']}]: ").strip()
        if price: p['price'] = float(price)
        
        stock = input(f"Stock [{p['stock']}]: ").strip()
        if stock: p['stock'] = int(stock)
        
        print("✓ Updated successfully")
    except Exception as e:
        print(f"Error: {e}")

def delete_product():
    """Delete product"""
    view_inventory()
    try:
        pid = int(input("\nProduct ID to delete: "))
        if pid not in inventory:
            print("Error: Product not found")
            return
        
        if input(f"Delete '{inventory[pid]['title']}'? (yes/no): ").lower() == 'yes':
            del inventory[pid]
            print("✓ Deleted successfully")
    except Exception as e:
        print(f"Error: {e}")

# ============ SALES ============

def register_sale():
    """Register new sale"""
    print("\n=== REGISTER SALE ===")
    view_inventory()
    
    try:
        customer = get_text("\nCustomer name: ")
        pid = int(input("Product ID: "))
        
        if pid not in inventory:
            print("Error: Product not found")
            return
        
        p = inventory[pid]
        qty = int(get_positive_num("Quantity: ", int))
        
        if p['stock'] < qty:
            print(f"Error: Only {p['stock']} available")
            return
        
        disc = float(input("Discount % (0 if none): "))
        if disc < 0 or disc > 100:
            print("Error: Discount must be 0-100")
            return
        
        subtotal = p['price'] * qty
        disc_amt = subtotal * (disc / 100)
        total = subtotal - disc_amt
        
        sale = {
            "id": len(sales) + 1,
            "customer": customer,
            "product_id": pid,
            "title": p['title'],
            "author": p['author'],
            "qty": qty,
            "price": p['price'],
            "subtotal": subtotal,
            "disc_pct": disc,
            "disc_amt": disc_amt,
            "total": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        inventory[pid]['stock'] -= qty
        sales.append(sale)
        
        print("\n" + "="*40)
        print(f"Customer: {customer}")
        print(f"Product: {p['title']}")
        print(f"Quantity: {qty} x ${p['price']:.2f} = ${subtotal:.2f}")
        if disc > 0:
            print(f"Discount ({disc}%): -${disc_amt:.2f}")
        print(f"TOTAL: ${total:.2f}")
        print("="*40)
        print("✓ Sale registered")
    except Exception as e:
        print(f"Error: {e}")

def view_sales():
    """Display sales history"""
    print("\n" + "="*90)
    if not sales:
        print("No sales yet")
        return
    
    print(f"{'ID':<5} {'Customer':<15} {'Product':<25} {'Qty':<5} {'Total':<12} {'Date':<20}")
    print("-"*90)
    for s in sales:
        print(f"{s['id']:<5} {s['customer']:<15} {s['title']:<25} {s['qty']:<5} ${s['total']:<11.2f} {s['date']:<20}")
    print("="*90)

# ============ REPORTS ============

def top_products():
    """Top 3 best-selling products"""
    print("\n=== TOP 3 PRODUCTS ===")
    if not sales:
        print("No data available")
        return
    
    # Aggregate by product
    prod_data = {}
    for s in sales:
        pid = s['product_id']
        if pid not in prod_data:
            prod_data[pid] = {'title': s['title'], 'qty': 0, 'revenue': 0}
        prod_data[pid]['qty'] += s['qty']
        prod_data[pid]['revenue'] += s['total']
    
    # Sort and get top 3 using lambda
    top3 = sorted(prod_data.items(), key=lambda x: x[1]['qty'], reverse=True)[:3]
    
    print(f"{'Rank':<6} {'Product':<30} {'Units':<10} {'Revenue':<12}")
    print("-"*60)
    for i, (pid, data) in enumerate(top3, 1):
        print(f"{i:<6} {data['title']:<30} {data['qty']:<10} ${data['revenue']:<11.2f}")

def sales_by_author():
    """Sales grouped by author"""
    print("\n=== SALES BY AUTHOR ===")
    if not sales:
        print("No data available")
        return
    
    author_data = {}
    for s in sales:
        author = s['author']
        if author not in author_data:
            author_data[author] = {'units': 0, 'gross': 0, 'net': 0, 'disc': 0}
        author_data[author]['units'] += s['qty']
        author_data[author]['gross'] += s['subtotal']
        author_data[author]['net'] += s['total']
        author_data[author]['disc'] += s['disc_amt']
    
    print(f"{'Author':<25} {'Units':<8} {'Gross':<12} {'Net':<12} {'Discount':<10}")
    print("-"*70)
    for author, data in sorted(author_data.items(), key=lambda x: x[1]['net'], reverse=True):
        print(f"{author:<25} {data['units']:<8} ${data['gross']:<11.2f} ${data['net']:<11.2f} ${data['disc']:<9.2f}")

def financial_summary():
    """Calculate gross and net income"""
    print("\n=== FINANCIAL SUMMARY ===")
    if not sales:
        print("No data available")
        return
    
    gross = sum(map(lambda s: s['subtotal'], sales))
    disc = sum(map(lambda s: s['disc_amt'], sales))
    net = sum(map(lambda s: s['total'], sales))
    units = sum(map(lambda s: s['qty'], sales))
    
    print(f"Total Units: {units}")
    print(f"Gross Revenue: ${gross:.2f}")
    print(f"Discounts: ${disc:.2f}")
    print(f"Net Revenue: ${net:.2f}")

def reports_menu():
    """Reports submenu"""
    while True:
        print("\n=== REPORTS ===")
        print("1. Top 3 Products")
        print("2. Sales by Author")
        print("3. Financial Summary")
        print("4. Back")
        
        choice = input("Option: ")
        if choice == '1':
            top_products()
        elif choice == '2':
            sales_by_author()
        elif choice == '3':
            financial_summary()
        elif choice == '4':
            break

# ============ MAIN ============

def main():
    """Main program"""
    print("\n=== INVENTORY & SALES SYSTEM ===")
    
    while True:
        try:
            print("\n=== MAIN MENU ===")
            print("1. View Inventory")
            print("2. Add Product")
            print("3. Update Product")
            print("4. Delete Product")
            print("5. Register Sale")
            print("6. View Sales")
            print("7. Reports")
            print("8. Exit")
            
            choice = input("Option: ")
            
            if choice == '1':
                view_inventory()
            elif choice == '2':
                add_product()
            elif choice == '3':
                update_product()
            elif choice == '4':
                delete_product()
            elif choice == '5':
                register_sale()
            elif choice == '6':
                view_sales()
            elif choice == '7':
                reports_menu()
            elif choice == '8':
                print("\nGoodbye!")
                break
            else:
                print("Invalid option")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if _name_ == "_main_":
    main()
