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

from services.shopping_service import ShoppingService
shopService = ShoppingService()

from services.cartServices import CartService
cartService = CartService()

from services.home_service import HomeService
home_service = HomeService()

from services.payment_service import PaymentService
payment_service = PaymentService()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cajitasdeamor'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
CORS(app)

#Enpoint para productos
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

@app.route('/product/delete', methods=['POST'])
def product_delete():
    datos = request.get_json()
    try:
        response = proService.delete(datos=datos, appC=mysql)

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


#Endpoint para carrito de compras
@app.route('/cart/findByUserId', methods=['POST'])
def cart_findByUserId():
    datos = request.get_json()
    try:
        response = cartService.findByUserId(appC=mysql, datos=datos)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/cart/insert', methods=['POST'])
def cart_insert():
    datos = request.get_json()
    try:
        response = cartService.insert(appC=mysql, datos=datos)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/cart/delete', methods=['POST'])
def cart_delete():
    datos = request.get_json()
    try:
        response = cartService.delete(appC=mysql, datos=datos)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))


#Enpoint para usuarios
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

@app.route('/users/find', methods=['POST'])
def users_find():
    datos = request.get_json()
    try:
        response = userService.findByUserPass(datos=datos, appC=mysql)

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


@app.route('/users/delete', methods=['POST'])
def users_delete():
    datos = request.get_json()
    try:
        response = userService.delete(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/users/findEmail', methods=['POST'])
def users_findEmail():
    datos = request.get_json()
    try:
        response = userService.findUserByEmail(datos=datos, appC=mysql)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/users/changePass', methods=['POST'])
def users_changePass():
    datos = request.get_json()
    try:
        response = userService.changePass(datos=datos, appC=mysql)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))


#Enpoint para compras
@app.route('/shopping/findAll', methods=['POST'])
def shopping_findAll():
    try:
        response = shopService.findAll(appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/shopping/update', methods=['POST'])
def shopping_update():
    datos = request.get_json()
    try:
        response = shopService.update(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/shopping/updateDed', methods=['POST'])
def shopping_updateDed():
    datos = request.get_json()
    try:
        response = shopService.updateDed(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/shopping/insert', methods=['POST'])
def shopping_insert():
    datos = request.get_json()
    try:
        response = shopService.insert(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/shopping/cancel', methods=['POST'])
def shopping_cancel():
    datos = request.get_json()
    try:
        response = shopService.cancel(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))
        
@app.route('/shopping/findByUserId', methods=['POST'])
def menuUsuario_findByUserId():
    datos = request.get_json()
    try:
        response = shopService.findByUserId(appC=mysql, datos=datos)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))


#Enpoint para Home
@app.route('/home/insert', methods=['POST'])
def home_insertHome():
    datos = request.get_json()
    try:
        response = home_service.insertHome(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/home/findByUserId', methods=['POST'])
def home_findByUserId():
    datos = request.get_json()
    try:
        response = home_service.findByUserId(appC=mysql, datos=datos)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))


#Enpoint para Metodo De Pago
@app.route('/payment/insert', methods=['POST'])
def pago_insertPago():
    datos = request.get_json()
    try:
        response = payment_service.insert(datos=datos, appC=mysql)

        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

@app.route('/payment/findByUserId', methods=['POST'])
def payment_findByUserId():
    datos = request.get_json()
    try:
        response = payment_service.findByUserId(appC=mysql, datos=datos)
        return response
    except Exception as e:
        logging.exception(e)
        return jsonify(status='Error',  info='Algo salio mal', excepcion=''+str(e))

if __name__ == "__main__":
    app.run(host='0.0.0.0')