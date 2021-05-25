from types import MethodDescriptorType
from flask import Flask, jsonify,request
from flask_cors import CORS, cross_origin

from bson.objectid import ObjectId
from db import connect
import members

connection = connect()
db = connection.shineafrika

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def index():
    return "Ooops! Nothing here"

@app.route('/products', methods=['GET'])
def getProducts():
    json_products = []
    products = db.products.find()

    for product in products:
        json_products.append({
            'id': str(product['_id']),
            'title':product['title'],
            'expires': product['expires'],
            'customer': product['customer'],
            'price': product['price'],
        })

    response = jsonify({
        'result':'successful',
        'products': json_products
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/products", methods=['POST'])
@cross_origin()
def createProduct():
    product_data = request.get_json()
    product = db.products.insert_one({
        'title': product_data['title'],
        'customer' : product_data['customer'],
        'price' : product_data['price'],
        'expires' : product_data['expires']
    })

    productID = product.inserted_id
    productFound = db.products.find_one({'_id': ObjectId(productID)})
    productJSON = {
        'id': str(productFound['_id']),
        'customer': productFound['customer'],
        'title': productFound['title'],
        'price': productFound['price'],
        'expires': productFound['expires']
    }

    return jsonify({
        'result':'successful',
        'product': productJSON
    })

@app.route("/products/<id>", methods=['GET'])
def getProduct(id):
    product = db.products.find_one({'_id': ObjectId(id)})
    json_product = {
        'id': str(product['_id']),
        'customer': product['customer'],
        'title': product['title'],
        'price': product['price'],
        'expires': product['expires']
    }

    return jsonify({
        'result':'successful',
        'product':json_product
    })

@app.route('/products', methods=['PUT'])
def updateProduct():
    products = request.get_json()
    result = db.products.update_one({'_id': ObjectId(products['id'])}, {"$set": products['info']})

    if(result.modified_count > 0):
        return jsonify({
            'result': 'successful',
            'msg': 'Updated'
        })
    
    return jsonify({
        'result': 'failure'
    })


@app.route('/products', methods=['DELETE'])
def deleteProduct():
    products = request.get_json()
    result = db.products.delete_one({'_id' : ObjectId(products['id'])})
    
    if result.deleted_count == 1:
        response = f"{result.deleted_count} Product deleted"
    elif result.deleted_count > 1:
        response = f"{result.deleted_count} Products deleted"
    else:
        response = "Product to delete Not Found"
        return jsonify({
        'result': 'failure',
        'msg' : response
        })
    
    return jsonify({
        'result': 'successful',
        'msg':response
    })

@app.route('/members', methods=['GET'])
def returnMembers():
    return members.retrieveMembers()

@app.route('/login', methods=['POST'])
def Login():
    return members.login()

@app.route('/members', methods=['POST'])
def 

if __name__ == '__main__':
    app.run()