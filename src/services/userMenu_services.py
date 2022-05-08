import logging
from flask import jsonify
from flask_mysqldb import MySQLdb


class UserMenuService: 
    def findByUserId(self, datos, appC):
        mysql = appC
        request_data = datos


        try:
            id= int(request_data['idUsuario'])
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("SELECT * FROM compra  WHERE idUsuario='%s'"%str(id))
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()
            
            if len(result) == 0:
                content={'status':'Vacio'}
                return jsonify(content)

            productos = []
            content = {}
            for r in result:
                content = {
                    'idCompra': r['idCompra'],
                    'Estado': r['Estado'] 
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
        idCompra = request_data['idCompra']

        try:

            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("DELETE FROM carritocompras WHERE idCarrito=%s"%str(idCompra))
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            res = {
                    "status": 'Ok',
                    "Mensaje": 'Se cancelo el pedido con exito!',
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

