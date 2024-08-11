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
@app.route("/picture/<string:id>", methods=["POST"])
def create_picture(id):
    """
    Create a new picture entry with the given ID.
    
    :param id: The ID of the picture to create
    :return: JSON response indicating success or error
    """
    # Extract picture data from the request body
    picture_data = request.get_json()

    # Check if a picture with the given ID already exists
    existing_picture = next((item for item in data if item["id"] == id), None)
    if existing_picture:
        # Return a 302 status code if the picture already exists
        return jsonify({"Message": f"Picture with id {id} already present"}), 302

    # Append the new picture data to the data list
    picture_data["id"] = id  # Ensure the ID is set correctly
    data.append(picture_data)
    
    # Optionally, save the updated data back to the file
    with open(json_url, 'w') as file:
        json.dump(data, file, indent=4)

    # Return a success message
    return jsonify({"Message": "Picture created successfully"}), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
