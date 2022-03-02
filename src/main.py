from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL
from flask_cors import CORS
import logging

from services.product_service import ProductService
proService = ProductService()

from services.categories_service import CategoriesService
catService = CategoriesService()

from services.users_service import UsersService
userService = UsersService()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql3.freesqldatabase.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'sql3475018'
app.config['MYSQL_PASSWORD'] = 'IHcHDIAjiM'
app.config['MYSQL_DB'] = 'sql3475018'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
CORS(app)

@app.route('/product/findAll', methods=['POST'])
def product_findAll():
    try:
        response = proService.findAll(appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/product/insert', methods=['POST'])
def product_insertProduct():
    datos = request.get_json()
    try:
        response = proService.insertProduct(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/product/update', methods=['POST'])
def product_updateProduct():
    datos = request.get_json()
    try:
        response = proService.updateProduct(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/categories/findAll', methods=['POST'])
def categories_findAll():
    try:
        response = catService.findAll(appC=mysql)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))



@app.route('/users/findAll', methods=['POST'])
def users_findAll():
    try:
        response = userService.findAll(appC=mysql)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/users/insert', methods=['POST'])
def users_insertUser():
    datos = request.get_json()
    try:
        response = userService.insertUser(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/users/update', methods=['POST'])
def users_updateUser():
    datos = request.get_json()
    try:
        response = userService.updateUser(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

        
if __name__ == "__main__":
    app.run(host='0.0.0.0')