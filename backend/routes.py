from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return all  data"""
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return data by id"""
    if data:
        for picture in data:
            if picture['id'] == id:
                return jsonify(picture), 200
        return {"message": "No image found"}, 404

    return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """add new picture if does not exist already"""
    new_pic = request.json
    if data:
        for picture in data:
            if picture['id'] == new_pic['id'] :
                return {'Message': f"picture with id {new_pic['id']} already present"}, 302
        data.append(new_pic)
        return jsonify(data[-1]), 201

    return {"Message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """update picture by id"""
    new_pic = request.json
    if data:
        for i in range(len(data)):
            if data[i]['id'] == new_pic['id'] :
                data[i] = new_pic
                return jsonify(data[i]), 200
        return {"Message": "picture not found"}, 404

    return {"Message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """delete picture by id"""
    if data:
        for i in range(len(data)):
            if data[i]['id'] == id :
                del data[i]
                return {}, 204
        return {"Message": "picture not found"}, 404

    return {"Message": "Internal server error"}, 500
