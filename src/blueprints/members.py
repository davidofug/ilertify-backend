from enum import unique
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from src.db import connect
from bson.objectid import ObjectId
import hashlib
import os
from src.helpers import generateToken
import datetime
from pymongo import TEXT, errors

# connection = connect()
# db = connection.shineafrika
db = connect()
# define the blueprint
db.members.create_index([('username', 1)],unique=True)
db.members.create_index([("phone",1)], unique=True)

members = Blueprint(name="members", import_name=__name__)

@members.route('/new', methods=['POST'])
@cross_origin()
def addMember():
    data = request.get_json()
    salt = os.urandom(32)
    password = data['password']
    password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    password = salt + password
    
    ### Initial access & refresh tokens ###
    access = generateToken({'username':data['username'], 'exp':7200000})
    refresh = generateToken({'exp':7200000}, 2)
    
    try:
        member = db.members.insert_one({
            'username': data['username'],
            'password': password,
            'name' : {
                'first': data['first_name'],
                'last': data['last_name'],
            },
            'email': data['email'], 
            'phone' : data['phone'],
            'tokens':{
                'access': access,
                'refresh': refresh
            },
        })

        id = member.inserted_id
        result = db.members.find_one({'_id': ObjectId(id)})
        user = {
            'username': result['username'],
            'tokens': {
                'access': '',
                'refresh': '',
            },
            'name': result['name'],
            'email': result['email'],
            'phone': result['phone'],
            'tokens':{
                'acess': access,
                'refresh': refresh
            }
        }

        return jsonify({
            'result':'successful',
            'member': user
        })

    except errors.DuplicateKeyError :
        print()
        return jsonify({
            'result':'failure',
            'msg': 'Username or Email or Phone number already taken!'
        })


# add view function to the blueprint
@members.route('/', methods=['GET'])
def retrieveMembers():
    json_members = []
    members = db.members.find()

    for Member in members:
        json_members.append({
            'id': str(Member['_id']),
            'title':Member['title'],
            'expires': Member['expires'],
            'customer': Member['customer'],
            'price': Member['price'],
        })

    response = jsonify({
        'result':'successful',
        'members': json_members
    })

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@members.route('/<id>', methods=['GET'])
def retrieveMember(id):
    Member = db.members.find_one({'_id': ObjectId(id)})
    json_Member = {
        'id': str(Member['_id']),
        'customer': Member['customer'],
        'title': Member['title'],
        'price': Member['price'],
        'expires': Member['expires']
    }

    return jsonify({
        'result':'successful',
        'Member':json_Member
    })

@members.route('/auth', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if(username == '' or password == '') :
        return jsonify({
            'result': 'failure',
            'msg': 'Provide username and password!'
        })

    result = db.members.find_one({'username': username})

    if(result):
        salt = result['password'][:32]
        passwordHash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        
        if( passwordHash == result['password'][32:]):
            access = generateToken({'username':data['username'], 'exp':7200000})
            refresh = generateToken({'exp':7200000})

            result['tokens'] = {
                'action': access,
                'refresh': refresh
            }

            updated = db.members.update_one({'_id': ObjectId(result['_id'])}, {"$set": result['tokens']})
            
            if(updated.modified_count > 0):
            
                user = {
                    'username': result['username'],
                    'tokens': result['tokens'],
                    'name': result['name'],
                    'email': result['email'],
                    'phone': result['phone']
                }

                return jsonify({
                    'result': 'successful',
                    'user': user
                })
            
            return jsonify({
                'result':'failure',
                'msg': 'User not found'
            })

        return jsonify({
            'result': 'failure',
            'msg': 'Wrong username/password'
        })

    return jsonify({
        'result':'failure',
        'msg':'Wrong username'
    })

@members.route('/edit', methods=['PUT'])
def updateMember():
    data = request.get_json()
    result = db.members.update_one({'_id': ObjectId(data['id'])}, {"$set": members['info']})

    if(result.modified_count > 0):
        return jsonify({
            'result': 'successful',
            'msg': 'Updated'
        })
    
    return jsonify({
        'result': 'failure'
    })

@members.route('/delete', methods=['DELETE'])
def deleteMember():
    data = request.get_json()
    result = db.members.delete_one({'_id' : ObjectId(data['id'])})
    
    if result.deleted_count == 1:
        response = f"{result.deleted_count} Member deleted"
    elif result.deleted_count > 1:
        response = f"{result.deleted_count} members deleted"
    else:
        response = "Member to delete Not Found"
        return jsonify({
            'result': 'failure',
            'msg' : response
        })
    
    return jsonify({
        'result': 'successful',
        'msg':response
    })