import logging
from flask import jsonify

class ProductService: 
    def findAll(self, appC):
        mysql = appC

        try:

            cur = mysql.connection.cursor()
            query = "SELECT * FROM productos"
            cur.execute(query)
            mysql.connection.commit()

            result = cur.fetchall()

            res = [
                {
                    "status": 'Ok',
                    "data": result
                }
            ]

            cur.close()
            return jsonify(res)
        except Exception as e:
            logging.error('Error: ')
            logging.error(e)
            cur.close()
            return jsonify(status='Error')
