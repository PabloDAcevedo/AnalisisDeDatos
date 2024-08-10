
import os
import platform

from desafio1 import (
    ProductosDeAlmacen,
    ProductosBebidas,
    GestionProductos,
)

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo '''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_menu():
    print("==================================================")
    print("========== Menú de Gestión de Productos ==========")
    print("==================================================")
    print('1. Agregar Producto Nuevo de Almacen')
    print('2. Agregar Producto Nuevo de Bebidas')
    print('3. Buscar existencia de un producto')
    print('4. Actualizar precio de un producto')
    print('5. Actualizar el stock de un producto')
    print('6. Eliminar producto')
    print('7. Mostrar todos los productos')
    print('0. Salir')
    print('')

def nuevo_producto(gestion, tipo_producto):
    try:
        idProducto = int(input('Ingrese el ID del producto: '))
        marca = input('Ingrese la marca del producto: ')
        volumen = input('Ingrese las medidas del producto del producto: ')
        precio = float(input('Ingrese precio del producto: '))
        cantidadStock = int(input('Ingrese la cantidad de unidades del producto: '))
        
        if tipo_producto == '1':
            nombre = input('Ingrese nombre del producto: ')
            producto = ProductosDeAlmacen(idProducto, marca, volumen, precio, cantidadStock, nombre)
        elif tipo_producto == '2':
            tipoDeBebida = input('Ingrese que tipo de bebida es: ')
            producto = ProductosBebidas(idProducto, marca, volumen, precio, cantidadStock, tipoDeBebida)
        else:
            print('\nOpción inválida...')
            return
        
        
        gestion.nuevo_producto(producto)
        input('\nPresione Enter para continuar...')
        
    except ValueError as error:
        print(f'Error: {error}')
    except Exception as error:
        print(f'Error inesperado: {error}')


def buscar_producto(gestion):
    idProducto = input('\nIngrese el ID del producto que desea buscar: ')
    gestion.leer_producto(idProducto)
    input('\nPresione Enter para continuar...')


def actualizar_producto(gestion, tipo_producto):
    
    try:
        idProducto = input('\nIngrese el ID del producto a actualizar: ')
        
        if tipo_producto == '4':
            precio = float(input('Ingrese el precio nuevo: '))
            gestion.actualizar_precio(idProducto, precio)
            input('\nPresione Enter para continuar...')
        elif tipo_producto == '5':
            cantidadStock = int(input('Ingrese la cantidad en stock actualizada: '))
            gestion.actualizar_stock(idProducto, cantidadStock)
            input('\nPresione Enter para continuar...')
        else:
            print('\nOpción inválida...')
            return
    
    except ValueError as error:
            print(f'Error: {error}')
    except Exception as error:
            print(f'Error inesperado: {error}')
    

def eliminar_producto(gestion):
    idProducto = input('\nIngrese el ID del producto a eliminar: ')
    gestion.eliminar_producto(idProducto)
    input('\nPresione Enter para continuar...')

def mostrar_todos_los_producto(gestion):
    print('-----------------------------------------------------------------------------------------')
    print('|                              Listado de los Productos:                                |')
    print('-----------------------------------------------------------------------------------------')
    for producto in gestion.leer_inventario().values():
        if 'nombre' in producto:
            print(f"|| {producto['nombre']} - Marca: {producto['marca']} - Cantidad: {producto['cantidadStock']} unidades")
        else:
            print(f"|| {producto['tipoDeBebida']} - Marca: {producto['marca']} - Cantidad: {producto['cantidadStock']} unidades")
    print('-----------------------------------------------------------------------------------------\n')
    input('Presione Enter para continuar...')
        


if __name__ == '__main__':

    archivo_productos = 'stock_de_inventario_db.json'
    gestion_productos = GestionProductos(archivo_productos)
    
    while True:
        limpiar_pantalla()
        
        mostrar_menu()
        opcion = input('Seleccione una opción: ')
        
        if opcion == '1' or opcion == '2':
            nuevo_producto(gestion_productos, opcion)
            
        elif opcion == '3':
            buscar_producto(gestion_productos)
            
        elif opcion == '4':
            actualizar_producto(gestion_productos, opcion)
        
        elif opcion == '5':
            actualizar_producto(gestion_productos, opcion)
            
        elif opcion == '6':
            eliminar_producto(gestion_productos)
            
        elif opcion == '7':
            mostrar_todos_los_producto(gestion_productos)
            
        elif opcion == '0':
            print('\nSaliendo del programa...')
            break
        
        else:
            print('Opción no válida. Por favor elija una de las opciones brindadas.')