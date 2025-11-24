"""
Comprehensive Inventory and Sales Management System
Author: [Your Name]
Date: November 2024
Description: A robust system for managing bookstore inventory, sales, and generating dynamic reports.
"""

from datetime import datetime
from typing import Dict, List, Tuple

# Constants
MIN_STOCK = 0
MIN_PRICE = 0.0
MIN_QUANTITY = 1

# Pre-loaded inventory with 5 products
inventory: Dict[int, Dict] = {
    1: {
        "title": "One Hundred Years of Solitude",
        "author": "Gabriel García Márquez",
        "category": "Fiction",
        "price": 25.99,
        "stock": 15
    },
    2: {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "category": "Fiction",
        "price": 18.50,
        "stock": 20
    },
    3: {
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "category": "Non-Fiction",
        "price": 22.00,
        "stock": 12
    },
    4: {
        "title": "Educated",
        "author": "Tara Westover",
        "category": "Biography",
        "price": 19.99,
        "stock": 8
    },
    5: {
        "title": "Becoming",
        "author": "Michelle Obama",
        "category": "Biography",
        "price": 24.99,
        "stock": 10
    }
}

# Sales records storage
sales_records: List[Dict] = []

# Product ID counter
next_product_id = 6


# ==================== VALIDATION FUNCTIONS ====================

def validate_positive_number(prompt: str, number_type=float) -> float:
    """
    Validates and returns a positive number from user input.
    
    Args:
        prompt: Message to display to user
        number_type: Type of number to validate (int or float)
    
    Returns:
        Valid positive number
    """
    while True:
        try:
            value = number_type(input(prompt))
            if value <= 0:
                print("Error: Value must be positive.")
                continue
            return value
        except ValueError:
            print(f"Error: Please enter a valid {number_type._name_}.")


def validate_non_empty_string(prompt: str) -> str:
    """
    Validates and returns a non-empty string from user input.
    
    Args:
        prompt: Message to display to user
    
    Returns:
        Non-empty string
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: This field cannot be empty.")


def validate_stock(quantity: int, product_id: int) -> bool:
    """
    Validates if there is sufficient stock for a sale.
    
    Args:
        quantity: Requested quantity
        product_id: Product identifier
    
    Returns:
        True if stock is sufficient, False otherwise
    """
    if product_id not in inventory:
        return False
    return inventory[product_id]["stock"] >= quantity


# ==================== INVENTORY MANAGEMENT ====================

def add_product() -> None:
    """Registers a new product in the inventory."""
    global next_product_id
    
    print("\n=== ADD NEW PRODUCT ===")
    try:
        title = validate_non_empty_string("Enter product title: ")
        author = validate_non_empty_string("Enter author name: ")
        category = validate_non_empty_string("Enter category: ")
        price = validate_positive_number("Enter price: $", float)
        stock = int(validate_positive_number("Enter initial stock: ", int))
        
        inventory[next_product_id] = {
            "title": title,
            "author": author,
            "category": category,
            "price": price,
            "stock": stock
        }
        
        print(f"\n✓ Product added successfully with ID: {next_product_id}")
        next_product_id += 1
        
    except Exception as e:
        print(f"Error adding product: {str(e)}")


def view_inventory() -> None:
    """Displays all products in the inventory."""
    print("\n" + "="*80)
    print("INVENTORY".center(80))
    print("="*80)
    
    if not inventory:
        print("No products in inventory.")
        return
    
    print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Price':<10} {'Stock':<8}")
    print("-"*80)
    
    for product_id, product in inventory.items():
        print(f"{product_id:<5} {product['title']:<30} {product['author']:<20} "
              f"${product['price']:<9.2f} {product['stock']:<8}")
    print("="*80)


def update_product() -> None:
    """Updates an existing product in the inventory."""
    view_inventory()
    
    try:
        product_id = int(input("\nEnter product ID to update: "))
        
        if product_id not in inventory:
            print("Error: Product not found.")
            return
        
        product = inventory[product_id]
        print(f"\nUpdating: {product['title']}")
        print("(Press Enter to keep current value)")
        
        title = input(f"New title [{product['title']}]: ").strip()
        if title:
            product['title'] = title
        
        author = input(f"New author [{product['author']}]: ").strip()
        if author:
            product['author'] = author
        
        category = input(f"New category [{product['category']}]: ").strip()
        if category:
            product['category'] = category
        
        price_input = input(f"New price [${product['price']}]: ").strip()
        if price_input:
            product['price'] = float(price_input)
        
        stock_input = input(f"New stock [{product['stock']}]: ").strip()
        if stock_input:
            product['stock'] = int(stock_input)
        
        print("\n✓ Product updated successfully!")
        
    except ValueError:
        print("Error: Invalid input format.")
    except Exception as e:
        print(f"Error updating product: {str(e)}")


def delete_product() -> None:
    """Removes a product from the inventory."""
    view_inventory()
    
    try:
        product_id = int(input("\nEnter product ID to delete: "))
        
        if product_id not in inventory:
            print("Error: Product not found.")
            return
        
        product = inventory[product_id]
        confirm = input(f"Are you sure you want to delete '{product['title']}'? (yes/no): ")
        
        if confirm.lower() == 'yes':
            del inventory[product_id]
            print("\n✓ Product deleted successfully!")
        else:
            print("Deletion cancelled.")
            
    except ValueError:
        print("Error: Invalid product ID.")
    except Exception as e:
        print(f"Error deleting product: {str(e)}")


# ==================== SALES MANAGEMENT ====================

def register_sale() -> None:
    """Registers a new sale transaction."""
    print("\n=== REGISTER NEW SALE ===")
    view_inventory()
    
    try:
        customer_name = validate_non_empty_string("\nEnter customer name: ")
        product_id = int(input("Enter product ID: "))
        
        if product_id not in inventory:
            print("Error: Product not found.")
            return
        
        product = inventory[product_id]
        quantity = int(validate_positive_number("Enter quantity: ", int))
        
        if not validate_stock(quantity, product_id):
            print(f"Error: Insufficient stock. Available: {product['stock']}")
            return
        
        discount = float(input("Enter discount percentage (0 if none): "))
        if discount < 0 or discount > 100:
            print("Error: Discount must be between 0 and 100.")
            return
        
        # Calculate totals
        subtotal = product['price'] * quantity
        discount_amount = subtotal * (discount / 100)
        total = subtotal - discount_amount
        
        # Create sale record
        sale = {
            "sale_id": len(sales_records) + 1,
            "customer": customer_name,
            "product_id": product_id,
            "product_title": product['title'],
            "author": product['author'],
            "quantity": quantity,
            "unit_price": product['price'],
            "subtotal": subtotal,
            "discount_percent": discount,
            "discount_amount": discount_amount,
            "total": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Update inventory stock
        inventory[product_id]['stock'] -= quantity
        
        # Add to sales records
        sales_records.append(sale)
        
        print("\n" + "="*50)
        print("SALE RECEIPT".center(50))
        print("="*50)
        print(f"Customer: {customer_name}")
        print(f"Product: {product['title']}")
        print(f"Quantity: {quantity}")
        print(f"Unit Price: ${product['price']:.2f}")
        print(f"Subtotal: ${subtotal:.2f}")
        if discount > 0:
            print(f"Discount ({discount}%): -${discount_amount:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Date: {sale['date']}")
        print("="*50)
        print("✓ Sale registered successfully!")
        
    except ValueError:
        print("Error: Invalid input format.")
    except Exception as e:
        print(f"Error registering sale: {str(e)}")


def view_sales() -> None:
    """Displays all sales records."""
    print("\n" + "="*100)
    print("SALES HISTORY".center(100))
    print("="*100)
    
    if not sales_records:
        print("No sales recorded yet.")
        return
    
    print(f"{'ID':<5} {'Customer':<15} {'Product':<25} {'Qty':<5} {'Total':<12} {'Date':<20}")
    print("-"*100)
    
    for sale in sales_records:
        print(f"{sale['sale_id']:<5} {sale['customer']:<15} {sale['product_title']:<25} "
              f"{sale['quantity']:<5} ${sale['total']:<11.2f} {sale['date']:<20}")
    print("="*100)


# ==================== REPORTS MODULE ====================

def generate_top_products_report() -> None:
    """Generates a report of the top 3 best-selling products."""
    print("\n" + "="*60)
    print("TOP 3 BEST-SELLING PRODUCTS".center(60))
    print("="*60)
    
    if not sales_records:
        print("No sales data available.")
        return
    
    # Aggregate sales by product using lambda
    product_sales = {}
    for sale in sales_records:
        product_id = sale['product_id']
        if product_id not in product_sales:
            product_sales[product_id] = {
                'title': sale['product_title'],
                'quantity': 0,
                'revenue': 0.0
            }
        product_sales[product_id]['quantity'] += sale['quantity']
        product_sales[product_id]['revenue'] += sale['total']
    
    # Sort by quantity sold and get top 3
    sorted_products = sorted(product_sales.items(), 
                           key=lambda x: x[1]['quantity'], 
                           reverse=True)[:3]
    
    print(f"{'Rank':<6} {'Product':<30} {'Units Sold':<12} {'Revenue':<12}")
    print("-"*60)
    
    for rank, (product_id, data) in enumerate(sorted_products, 1):
        print(f"{rank:<6} {data['title']:<30} {data['quantity']:<12} ${data['revenue']:<11.2f}")
    
    print("="*60)


def generate_sales_by_author_report() -> None:
    """Generates a report of total sales grouped by author."""
    print("\n" + "="*70)
    print("SALES REPORT BY AUTHOR".center(70))
    print("="*70)
    
    if not sales_records:
        print("No sales data available.")
        return
    
    # Aggregate sales by author
    author_sales = {}
    for sale in sales_records:
        author = sale['author']
        if author not in author_sales:
            author_sales[author] = {
                'units_sold': 0,
                'gross_revenue': 0.0,
                'net_revenue': 0.0,
                'total_discount': 0.0
            }
        author_sales[author]['units_sold'] += sale['quantity']
        author_sales[author]['gross_revenue'] += sale['subtotal']
        author_sales[author]['net_revenue'] += sale['total']
        author_sales[author]['total_discount'] += sale['discount_amount']
    
    print(f"{'Author':<25} {'Units':<8} {'Gross Revenue':<15} {'Net Revenue':<15} {'Discount':<12}")
    print("-"*70)
    
    # Sort by net revenue
    sorted_authors = sorted(author_sales.items(), 
                          key=lambda x: x[1]['net_revenue'], 
                          reverse=True)
    
    for author, data in sorted_authors:
        print(f"{author:<25} {data['units_sold']:<8} ${data['gross_revenue']:<14.2f} "
              f"${data['net_revenue']:<14.2f} ${data['total_discount']:<11.2f}")
    
    print("="*70)


def generate_financial_summary() -> None:
    """Calculates and displays gross and net income totals."""
    print("\n" + "="*50)
    print("FINANCIAL SUMMARY".center(50))
    print("="*50)
    
    if not sales_records:
        print("No sales data available.")
        return
    
    # Calculate totals using lambda functions
    total_gross = sum(map(lambda sale: sale['subtotal'], sales_records))
    total_discounts = sum(map(lambda sale: sale['discount_amount'], sales_records))
    total_net = sum(map(lambda sale: sale['total'], sales_records))
    total_units = sum(map(lambda sale: sale['quantity'], sales_records))
    
    print(f"Total Units Sold: {total_units}")
    print(f"Gross Revenue (before discounts): ${total_gross:.2f}")
    print(f"Total Discounts Applied: ${total_discounts:.2f}")
    print(f"Net Revenue (after discounts): ${total_net:.2f}")
    print(f"Average Discount per Sale: ${(total_discounts/len(sales_records)):.2f}")
    print("="*50)


def reports_menu() -> None:
    """Displays the reports submenu."""
    while True:
        print("\n" + "="*40)
        print("REPORTS MENU".center(40))
        print("="*40)
        print("1. Top 3 Best-Selling Products")
        print("2. Sales by Author")
        print("3. Financial Summary")
        print("4. Back to Main Menu")
        print("="*40)
        
        try:
            choice = input("Select an option: ")
            
            if choice == '1':
                generate_top_products_report()
            elif choice == '2':
                generate_sales_by_author_report()
            elif choice == '3':
                generate_financial_summary()
            elif choice == '4':
                break
            else:
                print("Invalid option. Please try again.")
        except Exception as e:
            print(f"Error: {str(e)}")


# ==================== MAIN MENU ====================

def display_main_menu() -> None:
    """Displays the main menu of the system."""
    print("\n" + "="*50)
    print("INVENTORY & SALES MANAGEMENT SYSTEM".center(50))
    print("="*50)
    print("1. View Inventory")
    print("2. Add Product")
    print("3. Update Product")
    print("4. Delete Product")
    print("5. Register Sale")
    print("6. View Sales History")
    print("7. Generate Reports")
    print("8. Exit")
    print("="*50)


def main() -> None:
    """Main function to run the system."""
    print("\n" + "="*50)
    print("WELCOME TO THE INVENTORY MANAGEMENT SYSTEM".center(50))
    print("="*50)
    
    while True:
        try:
            display_main_menu()
            choice = input("Select an option: ")
            
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
                print("\nThank you for using the system. Goodbye!")
                break
            else:
                print("Invalid option. Please select a number between 1 and 8.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            print("Please try again.")


if _name_ == "_main_":
    main()
