from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.db import connect
from bson.objectid import ObjectId

connection = connect()
db = connection.shineafrika

# define the blueprint
products = Blueprint(name="products", import_name=__name__)

# add view function to the blueprint
@products.route('/', methods=['GET'])
def returnProducts():
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

@products.route("/new", methods=['POST'])
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

@products.route("/<id>", methods=['GET'])
def retrieveProduct(id):
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

@products.route('/edit', methods=['PUT'])
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

@products.route('/delete', methods=['DELETE'])
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