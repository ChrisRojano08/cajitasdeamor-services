import logging
from flask import jsonify
from flask_mysqldb import MySQLdb

from .home_service import HomeService
homeService = HomeService()

class UsersService: 
    def findAll(self, appC):
        mysql = appC

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM usuarios"
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            productos = []
            content = {}
            for r in result:
                content = {
                    'idUsuario': r['idUsuario'],
                    'Nombre': r['Nombre'], 
                    'Apellidos': r['Apellidos'],
                    'Correo': r['Correo'],
                    'Tipo': r['Tipo'],
                    'Domicilio': homeService.findById(appC=mysql, id=r['idDomicilio'])
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

    def insertUser(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            nombre = request_data['Nombre']
            apellidos = request_data['Apellidos']
            correo = request_data['Correo']
            contrasenia = request_data['Contrasenia']
            tipo = request_data['Tipo']

            idDomicilio = homeService.insertHome(appC=mysql, datos=datos)

            cur = mysql.connection.cursor()
            query = "INSERT INTO usuarios (Nombre, Apellidos, Correo, Contrasenia, Tipo, idDomicilio) VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(query, (nombre,apellidos,correo,contrasenia,tipo,idDomicilio))
            mysql.connection.commit()

            res = [
                {
                    "status": 'Ok',
                    "Mensaje": 'Se inserto el usuario con exito!',
                    "idUsuario": ''+str(cur.lastrowid)
                }
            ]
            cur.close()
            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

    def updateUser(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            idUsuario = request_data['idUsuario']
            nombre = request_data['Nombre']
            apellidos = request_data['Apellidos']
            correo = request_data['Correo']
            contrasenia = request_data['Contrasenia']
            tipo = request_data['Tipo']
            idDomicilio = request_data['idDomicilio']

            upHom = homeService.updateHome(appC=mysql, datos=request_data)

            if upHom['status'] != 'Ok':
                raise ConnectionError('Error al actualizar el domicilio')

            cur = mysql.connection.cursor()
            query = "UPDATE usuarios SET Nombre=%s, Apellidos=%s, Correo=%s, Contrasenia=%s, Tipo=%s, idDomicilio=%s WHERE idUsuario=%s"
            cur.execute(query, (nombre,apellidos,correo,contrasenia,tipo,idDomicilio,idUsuario))
            mysql.connection.commit()

            res = [
                {
                    "status": 'Ok',
                    "Mensaje": 'Se actualizo el usuario '+nombre+' con exito!',
                    "Domicilio": str(upHom)
                }
            ]
            cur.close()
            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))
