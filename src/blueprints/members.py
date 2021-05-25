from flask import jsonify,request

from bson.objectid import ObjectId
from db import connect

connection = connect()
db = connection.shineafrika

def addMember():
    return 'Register'

def login():

    member = {
        'id': 1,
        'username':'Username',
        'tokens':{
            'access':'Access',
            'refresh': 'Refresh'
        }
    }

    response = jsonify({
        'result':'successful',
        'member': member
    })

    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

def retrieveMembers():
    json_members = []
    members = db.members.find()

    for member in members:
        json_members.append({
            'id': str(member['_id']),
            'username':member['username'],
            'email': member['email'],
            'phone': member['phone']
        })

    response = jsonify({
        'result':'successful',
        'members': json_members
    })

    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

def updateMember():
    return 'Update'

def deleteMember():
    return 'Delete'