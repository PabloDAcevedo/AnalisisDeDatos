class Persona:
    def __init__(self, nombre, edad, sexo):
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo
    
    
    def saludar(self):
        return print(f'Hola, me llamo {self.nombre} y tengo {self.edad} y mi sexo es {self.sexo}')


prueba = Persona('Pablo', 23, 'Masculino')


print ('Holaaa')



--------------------------------------------------------------------------------------------------------------------------------------------

import json



class Producto:
    def __init__(self, nombre, precio, marca, cantidadStock, categoria, idProducto):
        self.__nombre = nombre
        self.__precio = self.validar_precio(precio)
        self.__marca = marca
        self.__cantidadStock = cantidadStock
        self.__categoria = categoria
        self.__idProducto = self.validar_idProducto(idProducto)
    
    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
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
    def categoria(self):
        return self.__categoria
    
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
            "nombre": self.nombre,
            "precio": self.precio,
            "marca": self.marca,
            "cantidadStock": self.cantidadStock,
            "categoria": self.categoria
        }
    


    def __str__(self):
        return f"{self.nombre} {self.volumen} {self.precio}"
    
    
    
class ProductosDeAlmacen(Producto):
    def __init__(self, nombre, precio, marca, cantidadStock, categoria, idProducto,  volumen):
        super().__init__(nombre, precio, marca, cantidadStock, categoria, idProducto)
        self.__volumen = volumen
        
        
    @property
    def volumen(self):
        return self.__volumen
    
    
    def to_dict(self):
        data = super().to_dict()
        data["volumen"] = self.volumen
        return data
    
    
    def __str__(self):
        return f"{super().__str__()} {self.volumen}"
    
    
 
class ProductosBebidas(Producto):
    def __init__(self, nombre, precio, marca, cantidadStock, categoria, idProducto,  mililitros):
        super().__init__(nombre, precio, marca, cantidadStock, categoria, idProducto)
        self.__mililitros = mililitros
        
    @property
    def mililitros(self):
        return self.__mililitros
    
    
    def to_dict(self):
        data = super().to_dict()
        data["mililitros"] = self.mililitros
        return data
    
    
    def __str__(self):
        return f"{super().__str__()} {self.volumen}"
    
    
class ProductosGalletitas():
    pass



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
        
    
    def actualizar_inventario(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
                
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
            
        except Exception as error:
            print(f'Error inesperado: {error}')
            
            
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