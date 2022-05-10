import logging
from flask import jsonify
from flask_mysqldb import MySQLdb

class HomeService:
    def findByUserId(self, appC, id):
        mysql = appC
        id = id

        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM domicilio WHERE idUsuario=(%s)"
            cur.execute(query, (str(id)))
            mysql.connection.commit()

            result = cur.fetchall()

            domicilio = []
            content = {}
            for r in result:
                content = {
                    'idDomicilio': r['idDomicilio'],
                    'Numero': r['Numero'], 
                    'Calle': r['Calle'],
                    'Colonia': r['Colonia'],
                    'Municipio': r['Municipio'],
                    'Estado': r['Estado'],
                    'CodigoPostal': r['CodigoPostal']
                    }
                domicilio.append(content)
                content = {}

            cur.close()
            return (domicilio)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))

    def insertHome(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            numero = request_data['Numero']
            calle = request_data['Calle']
            colonia = request_data['Colonia']
            municipio = request_data['Municipio']
            estado = request_data['Estado']
            codigoPostal = request_data['CodigoPostal']
            idUsuario = request_data['idUsuario']

            cur = mysql.connection.cursor()
            query = "INSERT INTO domicilio (Numero, Calle, Colonia, Municipio, Estado, CodigoPostal, idUsuario) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(query, (numero,calle,colonia,municipio,estado,codigoPostal,idUsuario))
            mysql.connection.commit()

            return jsonify(cur.lastrowid)
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
            numero = request_data['Numero']
            calle = request_data['Calle']
            colonia = request_data['Colonia']
            municipio = request_data['Municipio']
            estado = request_data['Estado']
            codigoPostal = request_data['CodigoPostal']
            

            cur = mysql.connection.cursor()
            query = "UPDATE domicilio SET Numero=%s, Calle=%s, Colonia=%s, Municipio=%s, Estado=%s, CodigoPostal=%s WHERE idDomicilio=%s"
            cur.execute(query, (numero,calle,colonia,municipio,estado,codigoPostal,idDomicilio))
            mysql.connection.commit()

            res = {
                    "status": 'Ok',
                    "Mensaje": 'Se actualizo el domicilio '+str(idDomicilio)+' con exito!',
                }
            

            cur.close()

            logging.exception('res')
            logging.exception(res)

            return jsonify(res)
        except Exception as e:
            logging.error('Error dom: ')
            logging.error(e)
            
            return jsonify(status='Error dom', exception=''+str(e))

    def findById(self, id, appC):
        mysql = appC
        idDom = id

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("SELECT * FROM domicilio WHERE idDomicilio='%s'"%idDom)
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            domicilio = []
            content = {}
            for r in result:
                content = {
                    'idDomicilio': r['idDomicilio'],
                    'Numero': r['Numero'], 
                    'Calle': r['Calle'],
                    'Colonia': r['Colonia'],
                    'Municipio': r['Municipio'],
                    'Estado': r['Estado'],
                    'CodigoPostal': r['CodigoPostal']
                    }
                domicilio.append(content)
                content = {}

            cur.close()
            return (domicilio)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

