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

            usuarios = []
            content = {}
            for r in result:
                content = {
                    'idUsuario': r['idUsuario'],
                    'Nombre': r['Nombre'], 
                    'Apellidos': r['Apellidos'],
                    'Correo': r['Correo'],
                    'Tipo': r['Tipo']
                    }
                usuarios.append(content)
                content = {}

            cur.close()
            return jsonify(usuarios)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))

    def findByUserPass(self, datos, appC):
        mysql = appC
        request_data = datos

        try:
            correo = request_data['Correo']
            passw = request_data['Contrasenia']

            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM usuarios WHERE Correo=(%s) AND Contrasenia=(%s)"
            cur.execute(query, (correo, passw))
            mysql.connection.commit()

            result = cur.fetchall()

            usuarios = []
            content = {}
            for r in result:
                content = {
                    'idUsuario': r['idUsuario'],
                    'Nombre': r['Nombre'], 
                    'Apellidos': r['Apellidos'],
                    'Correo': r['Correo'],
                    'Tipo': r['Tipo']
                    }
                usuarios.append(content)
                content = {}

            cur.close()
            return jsonify(usuarios)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

    def insertUser(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            nombre = request_data['Nombre']
            apellidos = request_data['Apellidos']
            correo = request_data['Correo']
            contrasenia = request_data['Contrasenia']
            tipo = 'usuario'

            logging.error(request_data)

            if not(contrasenia.isupper() or contrasenia.islower()):
                content={'status':'no letra'}
                return jsonify(content)
            if not(any(chr.isdigit() for chr in contrasenia)):
                content={'status':'no numero'}
                return jsonify(content)
            if (contrasenia.find('#')==-1 and contrasenia.find('$')==-1 and contrasenia.find('%')==-1 and contrasenia.find('_')==-1 and contrasenia.find('-')==-1):
                content={'status':'no caracter'}
                return jsonify(content)

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            queryCom = ("SELECT * FROM usuarios WHERE Correo='%s'"%correo)
            logging.error(queryCom)
            cur.execute(queryCom)
            mysql.connection.commit()
            result = cur.fetchall()
            if len(result) != 0:
                content={'status':'duplicado'}
                return jsonify(content)

            query = "INSERT INTO usuarios (Nombre, Apellidos, Correo, Contrasenia, Tipo) VALUES (%s,%s,%s,%s,%s)"
            cur.execute(query, (nombre,apellidos,correo,contrasenia,tipo))
            mysql.connection.commit()

            res = {
                    "status": 'Ok',
                    "Mensaje": 'Se inserto el usuario con exito!',
                    "idUsuario": ''+str(cur.lastrowid)
                }
            
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

            upHom = homeService.updateHome(appC=mysql, datos=request_data)

            if upHom['status'] != 'Ok':
                raise ConnectionError('Error al actualizar el domicilio')

            cur = mysql.connection.cursor()
            query = "UPDATE usuarios SET Nombre=%s, Apellidos=%s, Correo=%s, Contrasenia=%s, Tipo=%s, WHERE idUsuario=%s"
            cur.execute(query, (nombre,apellidos,correo,contrasenia,tipo,idUsuario))
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
