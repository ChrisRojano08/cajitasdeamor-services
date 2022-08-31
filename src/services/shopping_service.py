import logging
from flask import jsonify
from flask_mysqldb import MySQLdb
from datetime import datetime

from .users_service import UsersService
userService = UsersService()

from .product_service import ProductService
proService = ProductService()

from .home_service import HomeService
homeService = HomeService()

from .payment_service import PaymentService
payService = PaymentService()

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
                    'MetodoPago': r['idMetodoPago'],
                    'Domicilio': r['idDomicilio'],
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

    def insert(self, datos, appC):
        request_data = datos
        mysql = appC

        logging.error(request_data)

        try:
            idUs = request_data['idUsuario']
            fecha = datetime.today().strftime('%Y-%m-%d')
            dedicatoria = request_data['Dedicatoria']
            nombre = request_data['Nombre']
            ids = request_data['idsProductos']
            estado = "En espera"
            idMetodo = request_data['idMetodoPago']
            idDomicilio = request_data['idDomicilio']
            total = request_data['Monto']

            if(str(ids)[-1] == ','):
                ids = str(ids)[:-1]

            cur = mysql.connection.cursor()
            query = "INSERT INTO compra (idUsuario, Fecha, Dedicatoria, Nombre, idsProductos, Estado, idMetodoPago, idDomicilio, Monto) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(query, (idUs,fecha,dedicatoria,nombre,ids,estado,idMetodo,idDomicilio,total))
            mysql.connection.commit()

            res = {
                    "status": 'Ok',
                    "Mensaje": 'Se realizo la compra con exito!'
                }
            cur.close()
            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
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
                estado="Llevando a paquetería"
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

    def updateDed(self, datos, appC):
        request_data = datos
        mysql = appC

        logging.error(request_data)

        try:
            dedicatoria = request_data['Dedicatoria']
            nombre = request_data['Nombre']
            id = request_data['idCompra']

            cur = mysql.connection.cursor()
            query = "UPDATE compra SET Dedicatoria=%s, Nombre=%s WHERE idCompra=%s"
            cur.execute(query, (dedicatoria,nombre, str(id)))
            mysql.connection.commit()

            res = {
                    "status": 'Ok',
                    "Mensaje": 'Se actualizo la dedicatoria con exito!'
                }
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
                content=[{'status':'Vacio'}]
                return jsonify(content)

            productos = []
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
                    'Usuario': userService.findById(appC=mysql, id=r['idUsuario']),
                    'Fecha': r['Fecha'].strftime('%d-%m-%Y'),
                    'Dedicatoria': r['Dedicatoria'],
                    'Nombre': r['Nombre'],
                    'Productos': prods,
                    'Estado': r['Estado'],
                    'MetodoPago': payService.findById(appC=mysql, id=r['idMetodoPago']),
                    'Domicilio': homeService.findById(appC=mysql, id=r['idDomicilio']),
                    'Monto': r['Monto'],
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
