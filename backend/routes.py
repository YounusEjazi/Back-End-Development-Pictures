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
    """Return the list of all pictures"""
    if data:
        return jsonify(data), 200
    return jsonify({"message": "No pictures found"}), 404


######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """
    Retrieve a picture by its ID from the data list.
    
    :param id: The ID of the picture to retrieve
    :return: JSON response containing the picture details or an error message
    """
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_data = request.get_json()
    if not picture_data or "id" not in picture_data:
        return jsonify({"Message": "No data provided or ID is missing"}), 400

    # Check if the ID is an integer
    try:
        picture_id = int(picture_data["id"])
    except ValueError:
        return jsonify({"Message": "Invalid ID format"}), 400

    # Check if a picture with the same ID already exists
    existing_picture = next((item for item in data if item["id"] == picture_id), None)
    if existing_picture:
        return jsonify({"Message": f"picture with id {picture_id} already present"}), 302

    # Add the new picture to the data list
    data.append(picture_data)
    return jsonify(picture_data), 201
######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture_by_id(id):
    picture_data = request.get_json()
    if not picture_data:
        return jsonify({"Message": "No data provided"}), 400

    # Find the picture with the given ID
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return jsonify({"Message": "Picture not found"}), 404

    # Update the picture data
    picture.update(picture_data)
    return jsonify(picture), 200 
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the picture with the given ID
    picture = next((item for item in data if item["id"] == id), None)
    
    if picture:
        # Remove the picture from the list
        data.remove(picture)
        # Return an empty body with HTTP 204 No Content
        return '', 204
    else:
        # If the picture was not found, return a 404 error
        return jsonify({"message": "picture not found"}), 404