import logging
from flask import jsonify
from flask_mysqldb import MySQLdb

from .users_service import UsersService
userService = UsersService()

from .product_service import ProductService
proService = ProductService()

class ShoppingService: 
    def findAll(self, appC):
        mysql = appC

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM compra"
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            compras = []
            content = {}
            for r in result:
                x=r['idsProductos'].split(',')
                
                prods=[]
                cont={}
                for y in x :
                    cont = proService.findById(appC=mysql, id=y)
                    prods.append(cont)
                    cont={}

                content = {
                    'idCompra': r['idCompra'],
                    'idUsuario': userService.findById(appC=mysql, id=r['idUsuario']), 
                    'Fecha': r['Fecha'].strftime('%d-%m-%Y'),
                    'Dedicatoria': r['Dedicatoria'],
                    'Nombre': r['Nombre'],
                    'idsProductos': prods,
                    'Estado': r['Estado'],
                    'idMetodoPago': r['idMetodoPago'],
                    'idDomicilio': r['idDomicilio'],
                    'Monto': r['Monto']
                    }
                compras.append(content)
                content = {}

            cur.close()
            return jsonify(compras)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))

    def update(self, datos, appC):
        request_data = datos
        mysql = appC

        logging.error(request_data)

        try:
            numEstado = request_data['Estado']

            estado=""
            if numEstado=='0':
                estado="En espera"
            elif numEstado=='2':
                estado="Llevando a paqueteria"
            elif numEstado=='3':
                estado="En reparto"
            elif numEstado=='4':
                estado="En devolución"
            elif numEstado=='5':
                estado="Entregado"
            elif numEstado=='6':
                estado="Cancelado"
            elif numEstado=='1':
                estado="En construccion"
            
            id = request_data['idCompra']

            cur = mysql.connection.cursor()
            query = "UPDATE compra SET Estado=%s WHERE idCompra=%s"
            cur.execute(query, (estado,str(id)))
            mysql.connection.commit()

            res = [
                {
                    "status": 'Ok',
                    "Mensaje": 'Se actualizo la compra '+str(id)+' con exito!'
                }
            ]
            cur.close()
            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

    def cancel(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            id = request_data['idCompra']

            cur = mysql.connection.cursor()
            query = ("UPDATE compra SET Estado='Cancelado' WHERE idCompra='%s'"%str(id))
            cur.execute(query)
            mysql.connection.commit()

            res = [
                {
                    "status": 'Ok',
                    "Mensaje": 'Se cancelo la compra '+str(id)+' con exito!'
                }
            ]
            cur.close()
            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))
