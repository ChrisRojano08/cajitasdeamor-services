import logging
from flask import jsonify
from flask_mysqldb import MySQLdb
from requests import request

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

    def findById(self, id, appC):
        mysql = appC
        idUss = id

        try:

            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("SELECT * FROM usuarios WHERE idUsuario='%s'"%idUss)
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
            return (usuarios)
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

            if (any(chr.isdigit() for chr in nombre)):
                content={'status':'No ingrese números en su Nombre'}
                return jsonify(content)
            if (any(chr.isdigit() for chr in apellidos)):
                content={'status':'No ingrese números en sus Apellidos'}
                return jsonify(content)
            if contrasenia.isupper() or contrasenia.islower():
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
            tipo = request_data['Tipo']

            if (any(chr.isdigit() for chr in nombre)):
                content={'status':'No ingrese números en su Nombre'}
                return jsonify(content)
            if (any(chr.isdigit() for chr in apellidos)):
                content={'status':'No ingrese números en sus Apellidos'}
                return jsonify(content)

            cur = mysql.connection.cursor()
            query = "UPDATE usuarios SET Nombre=%s, Apellidos=%s, Correo=%s, Tipo=%s WHERE idUsuario=%s"
            cur.execute(query, (nombre,apellidos,correo,tipo,idUsuario))
            mysql.connection.commit()

            res = [
                {
                    "status": 'Ok',
                    "Mensaje": 'Se actualizo el usuario '+nombre+' con exito!'
                }
            ]
            cur.close()
            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

    def delete(self, datos, appC):
        mysql = appC
        request_data=datos
        idUss = request_data['idUsuario']

        try:

            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("DELETE FROM usuarios WHERE idUsuario=%s"%str(idUss))
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            res = {
                    "status": 'Ok',
                    "Mensaje": 'Se elimino al usuario con exito!',
                }

            cur.close()
            return (res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

    def changePass(self, datos, appC):
        request_data = datos
        mysql = appC

        try:
            correo = request_data['Correo']
            contrasenia = request_data['Contrasenia']

            if not(contrasenia.isupper() or contrasenia.islower()):
                content={'status':'no letra'}
                return jsonify(content)
            if not(any(chr.isdigit() for chr in contrasenia)):
                content={'status':'no numero'}
                return jsonify(content)
            if (contrasenia.find('#')==-1 and contrasenia.find('$')==-1 and contrasenia.find('%')==-1 and contrasenia.find('_')==-1 and contrasenia.find('-')==-1):
                content={'status':'no caracter'}
                return jsonify(content)

            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("UPDATE usuarios SET Contrasenia=%s WHERE Correo=%s")
            cur.execute(query, (contrasenia,correo))

            mysql.connection.commit()

            res ={
                    "status": 'Ok',
                    "Mensaje": 'Se actualizo la contraseña con exito!'
                }
            
            cur.close()
            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))

    def findUserByEmail(self, datos, appC):
        mysql = appC
        try:
            emailUser = datos
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = ("SELECT * FROM usuarios WHERE Correo='%s'"%emailUser)
            cur.execute(query)
            
            mysql.connection.commit()
            result = cur.fetchall()

            if len(result) != 0:
                res = {
                    "status": 'Ok',
                    "Mensaje": 'Se encontro el usuario'
                }
            else:
                res = {
                    "status": 'Error',
                    "Mensaje": 'No se encotro un usuario con este correo'
                } 

            cur.close()
            return jsonify(res)
            
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            return jsonify(status='Error', exception=''+str(e))