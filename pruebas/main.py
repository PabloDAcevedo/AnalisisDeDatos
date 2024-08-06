
import os
import platform

from desafio1 import (
    ProductosDeAlmacen,
    ProductosBebidas,
    ProductosGalletitas,
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
    print('3. Buscar un producto')
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
            print('Opción inválida...')
            return
        
        
        gestion.nuevo_producto(producto)
        
        input('Presione Enter para continuar...')
        
    except ValueError as error:
        print(f'Error: {error}')
    except Exception as error:
        print(f'Error inesperado: {error}')


def buscar_producto(gestion):
    idProducto = input('Ingrese el ID del producto que desea buscar: ')
    gestion.leer_producto(idProducto)
    input('Presione Enter para continuar...')


def actualizar_salario_colaborador(gestion):
    pass

def eliminar_colaborador_por_dni(gestion):
    pass

def mostrar_todos_los_colaboradores(gestion):
    pass


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
            
        else:
            print('Opción no válida')