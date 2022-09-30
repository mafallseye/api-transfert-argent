"""The Endpoints to manage the BOOK_REQUESTS"""

import smtplib
from email.mime.text import MIMEText
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from flask import jsonify, abort, request, Blueprint, url_for, render_template
import pymongo

from validate_email import validate_email
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

REQUEST_API = Blueprint('request_api', __name__)
se = URLSafeTimedSerializer('Mybigsecretmaxefall!')
mongo_client = "mongodb+srv://maxe:MAfall97@cluster0.q8jo5fg.mongodb.net/auth1"
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client.auth1
users = db.signUp1


def get_blueprint():
    """Return the blueprint for the main app module"""

    return REQUEST_API


BOOK_REQUESTS = list(users.find())
# users.insert_many(BOOK_REQUESTS)


@REQUEST_API.route('/request', methods=['GET'])
def get_records():
    """Return all book requests
    @return: 200: an array of all known BOOK_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    BOOK_REQUESTS = list((users.find()))
    return jsonify(BOOK_REQUESTS)


@REQUEST_API.route('/request/<string:_id>', methods=['GET'])
def get_record_by_id(_id):
    """Get book request details by it's id
    @param _id: the id
    @return: 200: a BOOK_REQUESTS as a flask/response object \
    with application/json mimetype.
    @raise 404: if book request not found
    """

    # if _id not in BOOK_REQUESTS:
    #     abort(404)
    userId = users.find_one({"_id": _id})
    return jsonify(userId)


@REQUEST_API.route('/register', methods=['POST'])
def register_record():
    """Create a book request record
    @param email: post : the requesters email address
    @param title: post : the title of the book requested
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('email'):
        abort(400)
    if not validate_email(data['email']):
        abort(400)
    if not data.get('password'):
        abort(400)

    # new_uuid = str(uuid.uuid4())
    book_request = {


        '_id': str(ObjectId()),
        'lastname': data['lastname'],
        'firstname': data['firstname'],
        'password': sha256_crypt.encrypt(data[('password')]),
        'email': data['email'],
        'pays':data['pays'],
        'nationality':data['nationality'],
        'identity':data['identity'],
        'timestamp': datetime.now().timestamp(),


    }
    # BOOK_REQUESTS[new_uuid] = book_request
    # HTTP 201 Created
    users.insert_one(book_request)
    if book_request is not None:
        return jsonify({'message': 'registered successfully', "status": "success"}), 201
    return jsonify({'message': 'something went wrong', "status": "failed"}), 400


@REQUEST_API.route('/request', methods=['POST'])
def create_record():
    """Create a book request record
    @param email: post : the requesters email address
    @param title: post : the title of the book requested
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    email = data['email']
    token = se.dumps(email, salt="confirm-email")
    if not data.get('email'):
        abort(400)
    if not validate_email(data['email']):
        abort(400)
    if not data.get('password'):
        abort(400)

    # new_uuid = str(uuid.uuid4())
    book_request = {
        'password': data['password'],
        'email': data['email'],
        'timestamp': datetime.now().timestamp(),
        'token': '{}'.format(token)

    }
    # BOOK_REQUESTS[new_uuid] = book_request
    # HTTP 201 Created
    return jsonify(book_request), 201


@REQUEST_API.route('/request/<string:_id>', methods=['PUT'])
def edit_record(_id):
    """Edit a book request record
    @param email: post : the requesters email address
    @param title: post : the title of the book requested
    @return: 200: a booke_request as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    # if _id not in BOOK_REQUESTS:
    #     abort(404)

    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    # if not data.get('email'):
    #     abort(400)
    # if not validate_email(data['email']):
    #     abort(400)
    # if not data.get('password'):
    #     abort(400)
    lastname= data['lastname'],
    firstname= data['firstname'],
    password= data['password'],
    email=data['email'],

   

    # BOOK_REQUESTS[_id] = book_request
    updatUsers = users.find_one_and_update(
        {"_id": _id}, {"$set": data},upsert=True)
    return jsonify(  {
                "status" : "success",
                "message" : "Register update successfully",
                "data" : data
            }), 200


@REQUEST_API.route('/change/password', methods=['POST'])
def change_record():
    """Edit a book request record
    @param email: post : the requesters email address
    @param title: post : the title of the book requested
    @return: 200: a booke_request as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    # if _id not in BOOK_REQUESTS:
    #     abort(404)

    # if not request.get_json():
    #     abort(400)
    data = request.get_json(force=True)

    if not data.get('email'):
        abort(400)
    if not validate_email(data['email']):
        abort(400)
    if not data.get('password'):
        abort(400)

    email = data['email']
    passwords = data['password']

    # BOOK_REQUESTS[_id] = book_request
    updaPass = users.find_one_and_update(
        {"email": email}, {"$set":data})
    if updaPass is not None:
        return jsonify(f'Your password {passwords} has been updated! You are now able to log in.', 'success'), 200
    return jsonify("something went wrong")


@REQUEST_API.route('/Forgotpassword', methods=['POST'])
def forgot_record():
   
    # if _id not in BOOK_REQUESTS:
    #     abort(404)

    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)

    if not data.get('email'):
        abort(400)
    if not validate_email(data['email']):

        abort(400)
    # if not data.get('password'):
    #     abort(400)
    email = data['email']
    token = se.dumps(email)
    # password = data['password']

    # book_request = {
    #     'email': data['email'],
    #     # 'password':  data['password'],
    #     'timestamp': datetime.now().timestamp(),
    #     'token': token


    # }
    # link = url_for('confirm_email', token=token, _external=True)
    user_exist = users.find_one({'email': email})
    # msg.body = 'Your link is {}'.format(link)
    if user_exist:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("maguettefseye@gmail.com", "qklhksqmkoxmurra")
        data = request.get_json(force=True)
        email = data['email']
        # password = data['password']
        book_request = {
            # 'password': data['password'],
            'email': data['email'],
            'timestamp': datetime.now().timestamp(),
            'token': '{}'.format(token)

        }
        # email = s.loads(token, salt='reset-password-salt', max_age=3600)

        password = 'bghgvfdrehjkkkuui'

        msg = MIMEText(f"Voici votre mot de passe : {password} ,\n voici votre identifiant : {email}")
        msg['Subject'] = 'Reset password'
        msg['From'] = 'maguettefseye@gmail.com'
        msg['To'] = email
   

        s.sendmail("maguettefseye@gmail.com", email, msg.as_string())

        s.quit()
        result = jsonify(data)
    else:
        result = jsonify(
            {'message': 'this {} does not exist'.format(email)}), 400
    return result
    # passwords=data['password']

    # BOOK_REQUESTS[_id] = book_request
    # updaPass = users.find_one_and_update(
    #     {"email": email}, {"$set": {"password":passwords}})
    # if updaPass is not None:
    #     return jsonify(updaPass), 200
    # return jsonify("something went wrong")


@REQUEST_API.route('/confirm_email/<token>')
def confirm_email(token):
    try:

        email = se.loads(token, salt='confirm_email', max_age=60)

        if not request.get_json():
            abort(400)
        data = request.get_json(force=True)

        book_request = {
            # 'password': data['password'],
            'email': data['email'],
            'timestamp': datetime.now().timestamp(),
            'token': '{}'.format(token)

        }

    except SignatureExpired:
        return 'The token is expired'
    return jsonify(book_request)


@REQUEST_API.route('/request/<string:_id>', methods=['DELETE'])
def delete_record(_id):
    """Delete a book request record
    @param id: the id
    @return: 204: an empty payload.
    @raise 404: if book request not found
    """
    # if _id not in BOOK_REQUESTS:
    #     abort(404)

    # del BOOK_REQUESTS[_id]
    deletUsers = users.find_one_and_delete({"_id": _id})
    if deletUsers is not None:
        return jsonify({"status":"success", "message":"Register successfully deleted"}),200

    return jsonify({"status":"failed", "message":"Something went wrong"}),400



