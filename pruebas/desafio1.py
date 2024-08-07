
import json



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
    def precio(self, nuevo_producto):
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
    def __init__(self, archivo):
        self.archivo = archivo
        

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
            datos = self.leer_inventario()
            if idProducto in datos:
                producto_data = datos[idProducto]
                if 'nombre' in producto_data:
                    producto = ProductosDeAlmacen(**producto_data)
                    print(f"\nID encontrado. - {producto_data['nombre']} - Marca: {producto_data['marca']} - Cantidad: {producto_data['cantidadStock']} unidades\n")
                else:
                    producto = ProductosBebidas(**producto_data)
                    print(f"\nID encontrado. - {producto_data['tipoDeBebida']} - Marca: {producto_data['marca']} - Cantidad: {producto_data['cantidadStock']} unidades\n")
            else:
                print(f'Producto no encontrado...')
                
        except Exception as error:
            print(f'Error al buscar el producto: {error}')
    
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
                print(f'Precio actualizado correctamente')
            else:
                print(f'Producto no encontrado')
                
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
            
        except Exception as error:
            print(f'Error inesperado: {error}')
            


    '''
    def actualizar_inventario(self, idProducto, cantidadStock):
        try:
            datos = self.leer_inventario()
            if str(idProducto) in datos.keys():
                datos[idProducto]['cantidadStock'] = cantidadStock
                self.actualizar_inventario(datos)
                print(f'Stock actualizado correctamente')
            else:
                print(f'Producto no encontrado')
                
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
            
        except Exception as error:
            print(f'Error inesperado: {error}')
    '''
    
    def nuevo_producto(self, producto):
        try:
            datos = self.leer_inventario()
            idProducto = producto.idProducto
            if not str(idProducto) in datos.keys():
                datos[idProducto] = producto.to_dict()
                self.actualizar_inventario(datos)
                print(f'Datos guardados correctamente')
            else:
                print(f'El producto ya existe')
            
        except Exception as error:
            print(f'Error inesperado al crear colaborador: {error}')
            
            
    def eliminar_producto(self, idProducto):
        try:
            datos = self.leer_inventario()
            if str(idProducto) in datos.keys():
                del datos[idProducto]
                self.actualizar_inventario(datos)
                print(f'Producto eliminado correctamente.')
            else:
                print(f'Producto no encontrado')
                
        except IOError as error:
            print(f'Error al intentar eliminar los datos en {self.archivo}: {error}')
            
        except Exception as error:
            print(f'Error inesperado: {error}')