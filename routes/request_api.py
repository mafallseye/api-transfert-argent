"""The Endpoints to manage the BOOK_REQUESTS"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
import pymongo
from validate_email import validate_email
REQUEST_API = Blueprint('request_api', __name__)
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
        '_id': data['_id'],
        'nom': data['nom'],
        'prenom': data['prenom'],
        'password': data['password'],
        'email': data['email'],
        'timestamp': datetime.now().timestamp()

    }
    # BOOK_REQUESTS[new_uuid] = book_request
    # HTTP 201 Created
    users.insert_one(book_request)
    return jsonify(book_request), 201


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
        'timestamp': datetime.now().timestamp()
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

    # if not request.get_json():
    #     abort(400)
    data = request.get_json(force=True)

    # if not data.get('email'):
    #     abort(400)
    # if not validate_email(data['email']):
    #     abort(400)
    # if not data.get('password'):
    #     abort(400)

    book_request = {
        'nom': data['nom'],
        'prenom': data['prenom'],
        'password': data['password'],
        'email': data['email'],
        'timestamp': datetime.now().timestamp()
    }

    # BOOK_REQUESTS[_id] = book_request
    updatUsers = users.find_one_and_update(
        {"_id": _id}, {"$set": book_request})
    return jsonify(updatUsers), 200


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
        return jsonify(deletUsers), 204

    return "id does not exist"
