import logging
from flask import jsonify
from flask_mysqldb import MySQLdb

from .product_service import ProductService
proService = ProductService()

class CartService: 
    def findByUserId(self, datos, appC):
        mysql = appC
        request_data = datos

        try:
            id= int(request_data['idUsuario'])

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("SELECT * FROM carritocompras  WHERE idUsuario='%s'"%str(id))
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            if len(result) == 0:
                content={'status':'Vacio'}
                return jsonify(content)

            productos = []
            content = {}
            total=0
            for r in result:
                subtotal=1
                cont = proService.findById(appC=mysql, id=r['idProducto'])

                subtotal=cont[0]['Precio']*r['Cantidad']

                content = {
                    'idCarrito': r['idCarrito'],
                    'Producto': cont,
                    'Cantidad': r['Cantidad'],
                    'Subtotal': subtotal
                    }
                productos.append(content)
                total+=subtotal
                content = {}
            
            content={'Total': total}          

            cur.close()
            return jsonify(productos, content)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))

    def insert(self, datos, appC):
        request_data = datos
        mysql = appC

        logging.error(request_data)

        try:
            idUsuario = request_data['idUsuario']
            idProducto = request_data['idProducto']

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            queryCom = "SELECT * FROM carritocompras WHERE idProducto=(%s) AND idUsuario=(%s)"

            cur.execute(queryCom, (idProducto, idUsuario))
            mysql.connection.commit()

            logging.error('uwu')

            result = cur.fetchone()

            logging.error('awa')

            if result is None:
                Cantidad = int(request_data['Cantidad'])
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "INSERT INTO carritocompras (idUsuario, idProducto, Cantidad) VALUES (%s,%s,%s)"
                cur.execute(query, (idUsuario, idProducto, Cantidad))
                mysql.connection.commit()
            else:
                Cantidad = int(result['Cantidad']) + int(request_data['Cantidad'])
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                query = "UPDATE carritocompras SET Cantidad=(%s) WHERE idCarrito=(%s)"
                cur.execute(query, (Cantidad, result['idCarrito']))
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

            res = [
                {
                    "status": 'Error',
                    "exception": ''+str(e)
                }
            ]

            return jsonify(res)

    def delete(self, datos, appC):
        mysql = appC
        request_data=datos
        idCarrito = request_data['idCarrito']

        try:

            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("DELETE FROM carritocompras WHERE idCarrito=%s"%str(idCarrito))
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