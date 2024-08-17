"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoints para personajes (people)
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    results = [character.to_dict() for character in characters]
    return jsonify(results), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(character.to_dict()), 200

# Endpoints para planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    results = [planet.to_dict() for planet in planets]
    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planet.to_dict()), 200

# Endpoints para usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    results = [user.to_dict() for user in users]
    return jsonify(results), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.to_dict()), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    favorites = Favorite.query.filter_by(user_id=user.id).all()
    results = [fav.to_dict() for fav in favorites]
    return jsonify(results), 200

# Endpoints para añadir y eliminar favoritos
@app.route('/favorites/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "El ID de usuario es requerido"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planeta no encontrado"}), 404
    
    favorite = Favorite(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorito añadido"}), 201

@app.route('/favorites/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "El ID de usuario es requerido"}), 400
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Personaje no encontrado"}), 404
    
    favorite = Favorite(user_id=user.id, character_id=character.id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"message": "Favorito añadido"}), 201

@app.route('/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "El ID de usuario es requerido"}), 400
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"error": "Favorito no encontrado"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorito eliminado"}), 200

@app.route('/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "El ID de usuario es requerido"}), 400
    favorite = Favorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if favorite is None:
        return jsonify({"error": "Favorito no encontrado"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorito eliminado"}), 200

# Ejecuta la app
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)