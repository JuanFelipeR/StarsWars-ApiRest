from flask import Flask, jsonify, request
# ORM para interactuar con la base de datos usando clases.
from flask_sqlalchemy import SQLAlchemy
# para manejar migraciones de esquemas (cambios en modelos).
from flask_migrate import Migrate
# permite que otras apps (como frontend) consuman la API.
from flask_cors import CORS
from models import db
from models import Character
from models import Planet
from models import Vehicle
from models import User
from models import FavoriteCharacter
from models import FavoritePlanet
from models import FavoriteVehicle


# Inicializar Flask y extensiones
app = Flask(__name__)  # Creamos un servidor flask
# Le indica a Flask dónde está la base de datos.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gitpod:postgres@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Aquí es donde registras tu app en SQLAlchemy
db.init_app(app)

# db = SQLAlchemy(app) # Inicializa SQLAlchemy para conectarse con la base de datos definida arriba.
# permite usar comandos de migración para crear tablas, agregar columnas, etc.
migrate = Migrate(app, db)
CORS(app)

# Ejemplo de ruta simple para probar


@app.route('/')
def hello():
    return jsonify({"message": "API de Star Wars activa"}), 200

# Endpoint para obtener un usuario

@app.route('/users', methods=['GET']) #listar todos los usuarios del blog
def get_users():
    users = User.query.all() #query.all() devuelve todos los usuarios
    return jsonify([user.serialize() for user in users]), 200

# Definimos ruta y metodo para obtener personajes
@app.route('/people', methods=['GET'])
def get_characters():
    # Devuelve una lista de objetos de la clase character con cada uno de los personajes
    characters = Character.query.all()
    # Transforma la data en formato json y transforma el objeto en dict, 200 es el cod que indica ok
    return jsonify([character.serialize() for character in characters]), 200


#Endpoin para obetener personaj por ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    #Busca el personaje por el id
    character = Character.query.get(people_id)
    #Si no lo encuentra devuelve 404
    if character is None:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(character.serialize()), 200

# Endpoint para obtener los planetas
@app.route('/planets',methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

#Endpoin para obetener planeta por ID
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200

# Endpoint para obtener vehiculos
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]), 200

# Endpoint vehiculos por id
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200


# añadir personaje a lista de favoritos
@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    # Usuario actual (en un proyecto real se obtendría por autenticación)
    current_user_id = 1

    # Verificar que el personaje con ese ID exista
    selected_character = Character.query.get(character_id)
    if selected_character is None:
        return jsonify({"error": "Personaje no encontrado"}), 404

    # Verificar si ya existe como favorito del usuario
    already_favorited = FavoriteCharacter.query.filter(
        FavoriteCharacter.user_id == current_user_id,
        FavoriteCharacter.character_id == character_id
    ).first()

    if already_favorited:
        return jsonify({"message": "El personaje ya está en favoritos"}), 200

    # Crear una nueva instancia de favorito
    new_favorite = FavoriteCharacter(
        user_id=current_user_id,
        character_id=character_id
    )

    # Agregarlo a la sesión de la base de datos
    db.session.add(new_favorite)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    # Enviar respuesta exitosa
    return jsonify({"message": "Personaje agregado a favoritos"}), 201

#Endpoint para añadir planeta a favoritos
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user_id = 1

    selected_planet = Planet.query.get(planet_id)
    if selected_planet is None:
        return jsonify({"error": "Planeta no encontrado"}), 404

    already_favorited = FavoritePlanet.query.filter(
        FavoritePlanet.user_id == current_user_id,
        FavoritePlanet.planet_id == planet_id
    ).first()

    if already_favorited:
        return jsonify({"message": "El planeta ya está en favoritos"}), 200

    new_favorite = FavoritePlanet(
        user_id=current_user_id,
        planet_id=planet_id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Planeta agregado a favoritos"}), 201

#Endpoint para añadir vehiculo a favoritos
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    current_user_id = 1

    selected_vehicle = Vehicle.query.get(vehicle_id)
    if selected_vehicle is None:
        return jsonify({"error": "Vehículo no encontrado"}), 404

    already_favorited = FavoriteVehicle.query.filter(
        FavoriteVehicle.user_id == current_user_id,
        FavoriteVehicle.vehicle_id == vehicle_id
    ).first()

    if already_favorited:
        return jsonify({"message": "El vehículo ya está en favoritos"}), 200

    new_favorite = FavoriteVehicle(
        user_id=current_user_id,
        vehicle_id=vehicle_id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Vehículo agregado a favoritos"}), 201

#Endpoint para eliminar personaje de favoritos
@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    current_user_id = 1

    favorite = FavoriteCharacter.query.filter(
        FavoriteCharacter.user_id == current_user_id,
        FavoriteCharacter.character_id == character_id
    ).first()

    if favorite is None:
        return jsonify({"error": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorito eliminado correctamente"}), 200

#Endpoint para eliminar planeta de favoritos
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user_id = 1

    favorite = FavoritePlanet.query.filter(
        FavoritePlanet.user_id == current_user_id,
        FavoritePlanet.planet_id == planet_id
    ).first()

    if favorite is None:
        return jsonify({"error": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorito eliminado correctamente"}), 200

#Endpoint para eliminar vehiculo de favoritos
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    current_user_id = 1

    favorite = FavoriteVehicle.query.filter(
        FavoriteVehicle.user_id == current_user_id,
        FavoriteVehicle.vehicle_id == vehicle_id
    ).first()

    if favorite is None:
        return jsonify({"error": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorito eliminado correctamente"}), 200


if __name__ == '__main__':
    # recarga automática para ver cambios y mensajes de error útiles
    app.run(host='0.0.0.0', port=3245, debug=True)
