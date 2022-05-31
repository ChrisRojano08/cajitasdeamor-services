import logging
from flask import jsonify
from flask_mysqldb import MySQLdb

from .categories_service import CategoriesService
catService = CategoriesService()

class ProductService: 
    def findAll(self, appC):
        mysql = appC

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM productos"
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            productos = []
            content = {}
            for r in result:
                content = {
                    'idProducto': r['idProducto'],
                    'Nombre': r['Imagen'], 
                    'Descripcion': r['Imagen'],
                    'Categoria': catService.findById(appC=mysql, id=r['idCategoria']),
                    'Precio': r['Imagen'],
                    'Tamanio': r['Imagen'],
                    'Imagen': r['Imagen'],
                    }
                productos.append(content)
                content = {}

            cur.close()
            return jsonify(productos)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))
        
    def findById(self, id, appC):
        mysql = appC
        idProd=id

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("SELECT * FROM productos WHERE idProducto='%s'"%idProd)
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            productos = []
            content = {}
            for r in result:
                content = {
                    'idProducto': r['idProducto'],
                    'Nombre': r['Nombre'], 
                    'Descripcion': r['Descripcion'],
                    'Categoria': catService.findById(appC=mysql, id=r['idCategoria']),
                    'Precio': r['Precio'],
                    'Tamanio': r['Tamanio'],
                    'Imagen': r['Imagen'],
                    }
                productos.append(content)
                content = {}

            cur.close()
            return (productos)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))

    def delete(self, datos, appC):
        mysql = appC
        request_data=datos
        idProd = request_data['idProducto']

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("DELETE FROM productos WHERE idProducto='%s'"%idProd)
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            res = {
                    "status": 'Ok',
                    "Mensaje": 'Se elimino el producto con exito!',
                }

            cur.close()
            return (res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)

            res = {
                    "status": 'Error',
                    "exception": ''+str(e),
                }

            return jsonify(res)

    def insertProduct(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            nombre = request_data['Nombre']
            descripcion = request_data['Descripcion']
            idCategoria = request_data['idCategoria']
            precio = request_data['Precio']
            tamanio = request_data['Tamanio']
            imagen = request_data['Imagen']

            cur = mysql.connection.cursor()
            query = "INSERT INTO productos (Nombre, Descripcion, idCategoria, Precio, Tamanio, Imagen) VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(query, (nombre,descripcion,idCategoria,precio,tamanio,imagen))
            mysql.connection.commit()

            res = [
                {
                    "status": 'Ok',
                    "Mensaje": 'Se inserto el producto con exito!'
                }
            ]
            cur.close()
            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))

    def updateProduct(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            idProducto = request_data['idProducto']
            nombre = request_data['Nombre']
            descripcion = request_data['Descripcion']
            idCategoria = request_data['idCategoria']
            precio = request_data['Precio']
            tamanio = request_data['Tamanio']
            imagen = request_data['Imagen']

            cur = mysql.connection.cursor()
            query = "UPDATE productos SET Nombre=%s, Descripcion=%s, idCategoria=%s, Precio=%s, Tamanio=%s, Imagen=%s WHERE idProducto=%s"
            cur.execute(query, (nombre,descripcion,idCategoria,precio,tamanio,imagen,idProducto))
            mysql.connection.commit()

            res = [
                {
                    "status": 'Ok',
                    "Mensaje": 'Se actualizo el producto '+nombre+' con exito!'
                }
            ]
            cur.close()
            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))
