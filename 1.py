#!/usr/bin/env python3
# All comments and user messages are in English (requirement)

from datetime import datetime

# -----------------------------
# CONSTANTS
# -----------------------------
FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

# -----------------------------
# INITIAL DATA (5 required)
# -----------------------------
productos = {
    1: {'titulo': "El Camino Python", 'autor': "Ana Torres", 'categoria': "Programación", 'precio': 29.90, 'stock': 10, 'vendidos': 0},
    2: {'titulo': "Estructuras de Datos", 'autor': "Luis Gómez", 'categoria': "Informática", 'precio': 24.50, 'stock': 8, 'vendidos': 0},
    3: {'titulo': "Algoritmos Básicos", 'autor': "Ana Torres", 'categoria': "Programación", 'precio': 34.75, 'stock': 5, 'vendidos': 0},
    4: {'titulo': "Literatura Universal", 'autor': "Claudia Ríos", 'categoria': "Ficción", 'precio": 15.00, 'stock': 20, 'vendidos': 0},
    5: {'titulo': "Redes para Principiantes", 'autor': "Diego Pérez", 'categoria': "Redes", 'precio': 39.99, 'stock': 4, 'vendidos': 0}
}

ventas = []
idProductoSiguiente = max(productos.keys()) + 1
idVentaSiguiente = 1

# -----------------------------
# VALIDATIONS
# -----------------------------
def validarEnteroPositivo(valorStr, nombreCampo="value"):
    """Validate positive integer."""
    try:
        v = int(valorStr)
        if v <= 0:
            raise ValueError(f"{nombreCampo} must be positive.")
        return v
    except:
        raise ValueError(f"Invalid {nombreCampo}. Enter a positive integer.")

def validarFloatNoNegativo(valorStr, nombreCampo="value"):
    """Validate non-negative float."""
    try:
        v = float(valorStr)
        if v < 0:
            raise ValueError(f"{nombreCampo} must be non-negative.")
        return v
    except:
        raise ValueError(f"Invalid {nombreCampo}. Enter a non-negative number.")

# -----------------------------
# PRODUCT CRUD FUNCTIONS
# -----------------------------
def listarProductos():
    """List all products."""
    if not productos:
        print("No products available.")
        return
    print("\nID | Título | Autor | Categoría | Precio | Stock")
    print("-" * 60)
    for pid, p in productos.items():
        print(f"{pid} | {p['titulo']} | {p['autor']} | {p['categoria']} | ${p['precio']:.2f} | {p['stock']}")
    print()

def verProducto():
    """View product by ID."""
    try:
        pid = validarEnteroPositivo(input("Enter product ID: "), "product ID")
    except Exception as e:
        print("Error:", e)
        return

    if pid not in productos:
        print("Product not found.")
        return

    p = productos[pid]
    print(f"\nProduct {pid}:")
    for k, v in p.items():
        print(f"  {k}: {v}")
    print()

def agregarProducto():
    """Add product."""
    global idProductoSiguiente
    try:
        titulo = input("Title: ").strip()
        autor = input("Author: ").strip()
        categoria = input("Category: ").strip()
        precio = validarFloatNoNegativo(input("Price: "), "price")
        stock = validarEnteroPositivo(input("Stock: "), "stock")

        if not titulo or not autor or not categoria:
            print("Fields are mandatory.")
            return

        productos[idProductoSiguiente] = {
            'titulo': titulo,
            'autor': autor,
            'categoria': categoria,
            'precio': precio,
            'stock': stock,
            'vendidos': 0
        }
        print(f"Product added with ID {idProductoSiguiente}.")
        idProductoSiguiente += 1

    except Exception as e:
        print("Error:", e)

def actualizarProducto():
    """Update existing product."""
    try:
        pid = validarEnteroPositivo(input("Enter product ID to update: "), "product ID")
    except Exception as e:
        print("Error:", e)
        return

    if pid not in productos:
        print("Product not found.")
        return

    p = productos[pid]

    print("Press ENTER to keep current value.")
    titulo = input(f"Title [{p['titulo']}]: ").strip() or p['titulo']
    autor = input(f"Author [{p['autor']}]: ").strip() or p['autor']
    categoria = input(f"Category [{p['categoria']}]: ").strip() or p['categoria']

    try:
        precioStr = input(f"Price [{p['precio']}]: ").strip()
        precio = p['precio'] if precioStr == "" else validarFloatNoNegativo(precioStr, "price")

        stockStr = input(f"Stock [{p['stock']}]: ").strip()
        stock = p['stock'] if stockStr == "" else validarEnteroPositivo(stockStr, "stock")

    except Exception as e:
        print("Error:", e)
        return

    p.update({'titulo': titulo, 'autor': autor, 'categoria': categoria, 'precio': precio, 'stock': stock})
    print("Product updated.")

def eliminarProducto():
    """Delete product."""
    try:
        pid = validarEnteroPositivo(input("Enter ID to delete: "), "product ID")
    except Exception as e:
        print("Error:", e)
        return

    if pid not in productos:
        print("Product not found.")
        return

    confirm = input("Are you sure? (y/N): ").lower()
    if confirm == "y":
        del productos[pid]
        print("Product deleted.")
    else:
        print("Cancelled.")

# -----------------------------
# SALES FUNCTIONS
# -----------------------------
def registrarVenta():
    """Register sale."""
    global idVentaSiguiente
    try:
        cliente = input("Client name: ").strip()
        pid = validarEnteroPositivo(input("Product ID: "), "product ID")
        cantidad = validarEnteroPositivo(input("Quantity: "), "quantity")

        descuentoStr = input("Discount % (empty = 0): ").strip()
        descuento = 0 if descuentoStr == "" else float(descuentoStr)

        if descuento < 0 or descuento > 100:
            print("Invalid discount.")
            return

    except Exception as e:
        print("Error:", e)
        return

    if pid not in productos:
        print("Product not found.")
        return

    producto = productos[pid]

    if cantidad > producto['stock']:
        print("Not enough stock.")
        return

    precioUnitario = producto['precio']
    totalBruto = precioUnitario * cantidad
    totalNeto = totalBruto * (1 - descuento / 100)

    venta = {
        'id': idVentaSiguiente,
        'cliente': cliente,
        'idProducto': pid,
        'cantidad': cantidad,
        'fecha': datetime.now().strftime(FORMATO_FECHA),
        'descuento': descuento,
        'precioUnitario': precioUnitario,
        'totalBruto': round(totalBruto, 2),
        'totalNeto': round(totalNeto, 2)
    }

    ventas.append(venta)
    producto['stock'] -= cantidad
    producto['vendidos'] += cantidad

    print(f"Sale recorded. ID {idVentaSiguiente}")
    idVentaSiguiente += 1

def listarVentas():
    """List all sales."""
    if not ventas:
        print("No sales available.")
        return

    print("\nID | Cliente | Producto | Cantidad | Fecha | Bruto | Neto")
    print("-" * 80)
    for v in ventas:
        print(f"{v['id']} | {v['cliente']} | {v['idProducto']} | {v['cantidad']} | {v['fecha']} | ${v['totalBruto']} | ${v['totalNeto']}")
    print()

# -----------------------------
# REPORTS
# -----------------------------
def topProductos(n=3):
    """Top products by units sold."""
    ordenados = sorted(productos.items(), key=lambda item: item[1]['vendidos'], reverse=True)
    top = ordenados[:n]
    print(f"\nTop {n} products:")
    for pid, p in top:
        print(f"{pid} - {p['titulo']} ({p['vendidos']} sold)")
    print()

def ventasPorAutor():
    """Sales grouped by author."""
    resumen = {}

    for v in ventas:
        pid = v['idProducto']
        autor = productos[pid]['autor']

        if autor not in resumen:
            resumen[autor] = {'bruto': 0, 'neto': 0, 'unidades': 0}

        resumen[autor]['bruto'] += v['totalBruto']
        resumen[autor]['neto'] += v['totalNeto']
        resumen[autor]['unidades'] += v['cantidad']

    print("\nAuthor | Units | Gross | Net")
    for autor, r in resumen.items():
        print(f"{autor} | {r['unidades']} | ${r['bruto']:.2f} | ${r['neto']:.2f}")
    print()

def resumenIngresos():
    """Gross and net income."""
    totalBruto = sum(map(lambda v: v['totalBruto'], ventas))
    totalNeto = sum(map(lambda v: v['totalNeto'], ventas))

    print("\nIncome Summary:")
    print(f"Gross: ${totalBruto:.2f}")
    print(f"Net:   ${totalNeto:.2f}\n")

# -----------------------------
# MAIN MENU (SWITCH-CASE)
# -----------------------------
def menuPrincipal():
    menu = """
Bookstore System - Menu
1. List products
2. View product
3. Add product
4. Update product
5. Delete product
6. Register sale
7. List sales
8. Top 3 products
9. Sales by author
10. Income summary
0. Exit
"""

    while True:
        print(menu)
        opcion = input("Option: ").strip()

        match opcion:
            case "1":
                listarProductos()
            case "2":
                verProducto()
            case "3":
                agregarProducto()
            case "4":
                actualizarProducto()
            case "5":
                eliminarProducto()
            case "6":
                registrarVenta()
            case "7":
                listarVentas()
            case "8":
                topProductos()
            case "9":
                ventasPorAutor()
            case "10":
                resumenIngresos()
            case "0":
                print("Exiting system.")
                break
            case _:
                print("Invalid option.")

# -----------------------------
# RUN PROGRAM
# -----------------------------
print("Starting bookstore system...")
menuPrincipal()
