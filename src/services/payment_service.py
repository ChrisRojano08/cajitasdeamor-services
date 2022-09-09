import logging
from flask import jsonify
from flask_mysqldb import MySQLdb
import re

class PaymentService:
    def findById(self, id, appC):
        mysql = appC
        idPago = id

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("SELECT * FROM metodopago WHERE idMetodoPago='%s'"%idPago)
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            metodoP = []
            content = {}
            for r in result:
                content = {
                    'idMetodoPago': r['idMetodoPago'],
                    'Nombre': r['Nombre'], 
                    'Banco': r['Banco'],
                    'Cuenta': r['Cuenta'],
                    'CVV': r['CVV'],
                    'FechaVencimiento': r['FechaVencimiento'].strftime('%d-%m-%Y')
                    }
                metodoP.append(content)
                content = {}

            cur.close()
            return (metodoP)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

    def insert(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            nombre = request_data['Nombre']
            banco = request_data['Banco']
            cuenta = request_data['Cuenta']
            idUsuario = request_data['idUsuario']
            cvv = request_data['CVV']
            fechavencimiento = request_data['FechaVencimiento']

            if (any(chr.isdigit() for chr in nombre)):
                content={'status':'No ingrese números en su nombre'}
                return jsonify(content)
            if not re.match(r"^[A-Za-z ]+$", nombre):
                content={'status':'No ingrese números o caracteres en su nombre'}
                return jsonify(content)

            cur = mysql.connection.cursor()
            query = "INSERT INTO metodopago (Nombre, Banco, Cuenta, idUsuario, CVV, FechaVencimiento) VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(query, (nombre,banco,cuenta,idUsuario,cvv,fechavencimiento))
            mysql.connection.commit()

            res = {
                    "status": 'Ok',
                    "Mensaje": 'Se inserto el método con exito!',
                    "idMetodoPago": cur.lastrowid
                }

            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

    def update(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            idMetodoPago = request_data['idMetodoPago']
            nombre = request_data['Nombre']
            banco = request_data['Banco']
            cuenta = request_data['Cuenta']
            cvv = request_data['CVV']
            fechavencimiento = request_data['FechaVencimiento']
            

            cur = mysql.connection.cursor()
            query = "UPDATE metodopago SET Nombre=%s, Banco=%s, Cuenta=%s, CVV=%s, FechaVencimiento=%s WHERE idMetodoPago=%s"
            cur.execute(query, (nombre,banco,cuenta,cvv,fechavencimiento,idMetodoPago))
            mysql.connection.commit()

            res = {
                    "status": 'Ok',
                    "Mensaje": 'Se actualizo el domicilio '+str(idMetodoPago)+' con exito!',
                }
            

            cur.close()

            logging.exception('res')
            logging.exception(res)

            return jsonify(res)
        except Exception as e:
            logging.error('Error dom: ')
            logging.error(e)
            
            return jsonify(status='Error dom', exception=''+str(e))

    def findByUserId(self, datos, appC):
        mysql = appC

        request_data = datos
        idU = request_data['idUsuario']

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("SELECT * FROM metodopago WHERE idUsuario='%s'"%idU)
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            if len(result) == 0:
                content=[{'status':'Vacio'}]
                return jsonify(content)

            metodoP = []
            content = {}
            for r in result:
                content = {
                    'idMetodoPago': r['idMetodoPago'],
                    'Nombre': r['Nombre'], 
                    'Banco': r['Banco'],
                    'Cuenta': r['Cuenta'],
                    'CVV': r['CVV'],
                    'FechaVencimiento': r['FechaVencimiento'].strftime('%d-%m-%Y')
                    }
                metodoP.append(content)
                content = {}

            cur.close()
            return jsonify(metodoP)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

