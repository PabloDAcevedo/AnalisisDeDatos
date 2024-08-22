
import json

import mysql.connector
from mysql.connector import Error
from decouple import config



class Producto:
    def __init__(self, idProducto, marca, volumen, precio, cantidadStock):
        self.__volumen = volumen
        self.__precio = self.validar_precio(precio)
        self.__marca = marca
        self.__cantidadStock = cantidadStock
        self.__idProducto = self.validar_idProducto(idProducto)
    
    
    @property
    def volumen(self):
        return self.__volumen
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def marca(self):
        return self.__marca.capitalize()
    
    @property
    def cantidadStock(self):
        return self.__cantidadStock
    
    @property
    def idProducto(self):
        return self.__idProducto
    
    
    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)
        
    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0:
                raise ValueError("El precio debe ser numérico positivo.")
            return precio_num
        except ValueError:
            raise ValueError("El precio debe ser un número válido.")


    @idProducto.setter
    def idProducto(self, nuevo_producto):
        self.__idProducto = self.validar_idProducto(nuevo_producto)

    def validar_idProducto(self, idProducto):
        try:
            idProducto_num = int(idProducto)
            if idProducto_num <= 0:
                raise ValueError("El ID del Producto debe ser numérico positivo.")
            return idProducto_num
        except ValueError:
            raise ValueError("El ID de Producto debe ser un número válido.")



    def to_dict(self):
        return {
            "idProducto": self.idProducto,
            "marca": self.marca,
            "volumen": self.volumen,
            "precio": self.precio,
            "cantidadStock": self.cantidadStock
        }
    


    def __str__(self):
        return f"{self.idProducto} {self.volumen} {self.precio}"
    
    
class ProductosDeAlmacen(Producto):
    def __init__(self, idProducto, marca, volumen, precio, cantidadStock, nombre):
        super().__init__(idProducto, marca, volumen, precio, cantidadStock)
        self.__nombre = nombre
        
        
    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    
    def to_dict(self):
        data = super().to_dict()
        data["nombre"] = self.nombre
        return data
    
    
    def __str__(self):
        return f"{super().__str__()} {self.nombre}"
    
 
class ProductosBebidas(Producto):
    def __init__(self, idProducto, marca, volumen, precio, cantidadStock, tipoDeBebida):
        super().__init__(idProducto, marca, volumen, precio, cantidadStock)
        self.__tipoDeBebida = tipoDeBebida
        
    @property
    def tipoDeBebida(self):
        return self.__tipoDeBebida
    
    
    def to_dict(self):
        data = super().to_dict()
        data["tipoDeBebida"] = self.tipoDeBebida
        return data
    
    
    def __str__(self):
        return f"{super().__str__()} {self.tipoDeBebida}"
    


class GestionProductos:
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port = config('DB_PORT')
           
    def connect(self):
        '''Estabelce conexion con la DB'''
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            
            if connection.is_connected():
                return connection
        
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def leer_inventario(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
            
        except FileNotFoundError:
            return{}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos
        
    def leer_producto(self, idProducto):
        try:
            connection = self.connect()
            
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM producto WHERE idProducto = %s', (idProducto,))
                    producto_data = cursor.fetchone()
                    
                    if producto_data:
                        cursor.execute('SELECT nombre FROM productosdealmacen WHERE idProducto = %s', (idProducto,))
                        nombre = cursor.fetchone()
                        
                        if nombre:
                            producto_data['nombre'] = nombre['nombre']
                            producto = ProductosDeAlmacen(**producto_data)
                            
                        else:
                            cursor.execute('SELECT tipoDeBebida FROM productosbebidas WHERE idProducto = %s', (idProducto,))
                            tipoBebida = cursor.fetchone()
                            
                            if tipoBebida:
                                producto_data['tipoDeBebida'] = tipoBebida['tipoDeBebida']
                                producto = ProductosBebidas(**producto_data)
                            
                            else:
                                producto = Producto(**producto_data)
                        
                        print(f"\n\t   | ID {producto_data['idProducto']} encontrado | \n| Marca: {producto_data['marca']} | Cantidad: {producto_data['cantidadStock']} unidades |\n")
                        
                    else:
                        print(f'\nProducto no encontrado con el ID: {idProducto}')
        
        except Error as e:
            print(f'\Error al buscar el producto: {e}')
        
        finally:
            if connection.is_connected():
                connection.close()
    
    def actualizar_inventario(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
                
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
            
        except Exception as error:
            print(f'Error inesperado: {error}')        
            
    def actualizar_precio(self, idProducto, precio):
        try:
            datos = self.leer_inventario()
            if str(idProducto) in datos.keys():
                datos[idProducto]['precio'] = precio
                self.actualizar_inventario(datos)
                print(f'\nPrecio actualizado correctamente')
            else:
                print(f'\nProducto no encontrado')
                
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
            
        except Exception as error:
            print(f'Error inesperado: {error}')
  
    def actualizar_stock(self, idProducto, cantidadStock):
        try:
            datos = self.leer_inventario()
            if str(idProducto) in datos.keys():
                datos[idProducto]['cantidadStock'] = cantidadStock
                self.actualizar_inventario(datos)
                print(f'\nStock actualizado correctamente')
            else:
                print(f'\nProducto no encontrado...')
                
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
            
        except Exception as error:
            print(f'Error inesperado: {error}')   
    
    def nuevo_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    #Verifica si el Producto existe
                    cursor.execute('SELECT idProducto FROM producto WHERE idProducto = %s', (producto.idProducto,))
                    
                    if cursor.fetchone():
                        print(f'\nEl producto {producto.idProducto} ya existe')
                        return
                    
                    # Insertar producto acorde al tipo
                    if isinstance(producto, ProductosDeAlmacen):
                        query = '''
                        INSERT INTO producto (idProducto, marca, volumen, precio, cantidadStock)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.idProducto, producto.marca, producto.volumen, producto. precio, producto.cantidadStock))
                        
                        query = '''
                        INSERT INTO productosdealmacen (idProducto, nombre)
                        VALUES (%s, %s)
                        '''
                        cursor.execute(query, (producto.idProducto, producto.nombre))

                    elif isinstance(producto, ProductosBebidas):
                        query = '''
                        INSERT INTO producto (idProducto, marca, volumen, precio, cantidadStock)
                        VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.idProducto, producto.marca, producto.volumen, producto. precio, producto.cantidadStock))
                        
                        query = '''
                        INSERT INTO productosbebidas (idProducto, tipoDeBebida)
                        VALUES (%s, %s)
                        '''
                        cursor.execute(query, (producto.idProducto, producto.tipoDeBebida))
                        
                    connection.commit()
                    print(f'\nProducto ID: {producto.idProducto} - {producto.marca} creado correctamente')
                    
        except Exception as error:
            print(f'\nError inesperado al crear producto: {error}')
                 
    def eliminar_producto(self, idProducto):
        try:
            datos = self.leer_inventario()
            if str(idProducto) in datos.keys():
                del datos[idProducto]
                self.actualizar_inventario(datos)
                print(f'\nProducto eliminado correctamente.')
            else:
                print(f'\nProducto no encontrado')
                
        except IOError as error:
            print(f'Error al intentar eliminar los datos en {self.archivo}: {error}')
            
        except Exception as error:
            print(f'Error inesperado: {error}')