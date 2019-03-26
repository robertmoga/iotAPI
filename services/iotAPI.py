from flask import blueprints, redirect, request, jsonify
import json, re, random, base64
from datetime import datetime
from .user_auth import token_required

iotAPI = blueprints.Blueprint('iot', __name__)
PIR_ACTIVE = False
'''
    Room temperature endpoints
'''

@iotAPI.route('/roomtemp', methods=['GET'])
@token_required
def get_room_temperature():
    # get from database the last output
    print (request)
    return jsonify({"timestamp:": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "temperature": 25.5})


@iotAPI.route('/roomtemp', methods=['POST'])
def post_room_temperature():
    return jsonify({"message:": "Successful"})


'''
    Outside temperature endpoints
'''

@iotAPI.route('/outtemp', methods=['GET'])
def get_outside_temperature():
    # get from database the last entry
    pass

@iotAPI.route('/outtemp', methods=['POST'])
def post_outside_temperature():
    # commit temp to database
    pass


'''
    Presence endpoints
'''
@iotAPI.route('/activatePIR/<state>', methods=['POST'])
def update_presence_listening_status(state):
    print(">> Update presence listening status : " + str(state))

@iotAPI.route('/updatePIRStatus', methods=['POST'])
def post_presence_status():
    # aici trebuie sa se apeleze o metoda POST a clientului un timestamp
    # clientul il retine local, si cand pagina se incarca, afiseaza ultimul timestamp
    # prin care se trimite un time stamp si o imagine -> prin mail
    #
    pass

@iotAPI.route('/getPIRStatus', methods=['GET'])
def get_presence_status():
    pass