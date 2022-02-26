from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from product_service import ProductService
import logging

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql3.freesqldatabase.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'sql3475018'
app.config['MYSQL_PASSWORD'] = 'IHcHDIAjiM'
app.config['MYSQL_DB'] = 'sql3475018'
mysql = MySQL(app)

proService = ProductService()

@app.route('/product/findAll', methods=['POST'])
def findAll():
    try:
        response = proService.findAll(appC=mysql)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

if __name__ == "__main__":
    app.run(host='0.0.0.0')