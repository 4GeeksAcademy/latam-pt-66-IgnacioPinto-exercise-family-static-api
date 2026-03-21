"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# 1) Obtener todos los miembros
@app.route('/members', methods=['GET'])
def get_all_members():
    # Obtenemos la lista de diccionarios llamando a la estructura de datos
    members = jackson_family.get_all_members()
    
    return jsonify(members), 200

# 2) recuperar solo un miembro por ID
@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404
    
######################################################################
# 3) Añadir un nuevo miembro
@app.route('/members', methods=['POST'])
def add_new_member():
    body = request.get_json()

    if not body:
        return jsonify({"Error": "Peticion incorrecta o cuerpo vacio"}), 400
    
    #Guardando el nuevo miembro en una variable para despues retornar ese miembro
    new_member = jackson_family.add_member(body)

    return jsonify(new_member), 200

######################################################################
# 4) Eliminar un miembro por ID
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_single_member(member_id):
    deleted = jackson_family.delete_member(member_id)

    if deleted:
        return jsonify({"done": True}), 200
    
    else:
        return jsonify({"Error": "Miembro no encontrado"}), 404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)


#proyecto finalizado