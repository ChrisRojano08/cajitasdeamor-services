import logging
from flask import jsonify
from flask_mysqldb import MySQLdb

class CategoriesService: 
    def findAll(self, appC):
        mysql = appC

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM categorias"
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            cats = []
            content = {}
            for r in result:
                content = {
                    'idCategorias': r['idCategorias'],
                    'Descripcion': r['Descripcion']
                    }
                cats.append(content)
                content = {}

            cur.close()
            return jsonify(cats)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error', exception=''+str(e))

    def findById(self, appC, id):
        mysql = appC
        id = id

        try:
            cur = cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM categorias WHERE idCategorias=(%s)"
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

