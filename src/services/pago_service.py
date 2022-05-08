import logging
from flask import jsonify
from flask_mysqldb import MySQLdb

class PagoService:
    def findById(self, appC, id):
        mysql = appC
        id = id

        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM metodopago WHERE idMetodoPago=(%s)"
            cur.execute(query, (str(id)))
            mysql.connection.commit()

            result = cur.fetchone()

            cur.close()
            return (result)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))

    def insertPago(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            nombre = request_data['Nombre']
            banco = request_data['Banco']
            cuenta = request_data['Cuenta']
            idUsuario = request_data['idUsuario']
            cvv = request_data['CVV']
            fechavencimiento = request_data['FechaVencimiento']

            cur = mysql.connection.cursor()
            query = "INSERT INTO metodopago (Nombre, Banco, Cuenta, idUsuario, CVV, FechaVencimiento) VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(query, (nombre,banco,cuenta,idUsuario,cvv,fechavencimiento))
            mysql.connection.commit()

            return jsonify(cur.lastrowid)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

    def updatePago(self, datos, appC):
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

