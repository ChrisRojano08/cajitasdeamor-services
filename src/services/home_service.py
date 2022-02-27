import logging
from flask import jsonify
from flask_mysqldb import MySQLdb

class HomeService:
    def findById(self, appC, id):
        mysql = appC
        id = id

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM domicilio WHERE idDomicilio=(%s)"
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

    def insertHome(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            calle = request_data['Calle']
            municipio = request_data['Municipio']
            estado = request_data['Estado']
            codigoPostal = request_data['CodigoPostal']

            cur = mysql.connection.cursor()
            query = "INSERT INTO domicilio (Calle, Municipio, Estado, CodigoPostal) VALUES (%s,%s,%s,%s)"
            cur.execute(query, (calle,municipio,estado,codigoPostal))
            mysql.connection.commit()

            return (cur.lastrowid)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))

    def updateHome(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            idDomicilio = request_data['idDomicilio']
            calle = request_data['Calle']
            municipio = request_data['Municipio']
            estado = request_data['Estado']
            codigoPostal = request_data['CodigoPostal']

            cur = mysql.connection.cursor()
            query = "UPDATE domicilio SET Calle=%s, Municipio=%s, Estado=%s, CodigoPostal=%s WHERE idDomicilio=%s"
            cur.execute(query, (calle,municipio,estado,codigoPostal,idDomicilio))
            mysql.connection.commit()

            res = {
                    "status": 'Ok',
                    "Mensaje": 'Se actualizo el domicilio '+str(idDomicilio)+' con exito!',
                }
            

            cur.close()

            logging.exception('res')
            logging.exception(res)

            return (res)
        except Exception as e:
            logging.error('Error dom: ')
            logging.error(e)
            
            return jsonify(status='Error dom', exception=''+str(e))

