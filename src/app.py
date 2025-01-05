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
from models import FavoritePeople, FavoritePlanet, People, Planet, db, User
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

# ------------------- PEOPLE ----------------------
@app.route('/people', methods=['GET'])
def handle_get_all_people():
    all_people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))

    return jsonify(all_people), 200

@app.route('/people/<int:id>', methods=['GET'])
def handle_get_people(id):
    person = People.query.get(id)
    if person is None:
        return jsonify({'msg': 'person not found'}), 404
    
    person = person.serialize()
    return jsonify(person), 200

# ------------------ PLANET -------------------------
@app.route('/planet', methods=['GET'])
def handle_get_all_planet():
    all_planet = Planet.query.all()
    all_planet = list(map(lambda x: x.serialize(), all_planet))

    return jsonify(all_planet), 200

@app.route('/planet/<int:id>', methods=['GET'])
def handle_get_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({'msg': 'planet not found'}), 404
    
    planet = planet.serialize()
    return jsonify(planet), 200

# ----------------- USER ---------------------
@app.route('/user', methods=['GET'])
def handle_get_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))

    return jsonify(all_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def handle_get_user(id):
    user = User.query.get(id)
    user = user.serialize()

    return jsonify(user), 200

@app.route('/user', methods=['POST'])
def handle_add_user():
    body = request.get_json()
    print(body)
    if 'name' not in body:
        return jsonify({'msg': 'error name not empty'}), 400
    
    if 'email' not in body:
        return jsonify({'msg': 'error email not empty'}), 400
    
    if 'password' not in body:
        return jsonify({'msg': 'error password not empty'}), 400
    
    new_user = User();
    new_user.name = body['name']
    new_user.email = body['email']
    new_user.password = body['password']

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@app.route('/user/<int:id>', methods=['DELETE'])
def handle_delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'msg': 'id not exist'}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({}), 204

# ------------ FAVORITES ----------------------
@app.route('/user/favorite', methods=['GET'])
def handle_get_user_favorite():
    user_id = 1
    fav_planet = FavoritePlanet.query.filter_by(id_user=user_id).all()
    fav_people = FavoritePeople.query.filter_by(id_user=user_id).all()

    favorites = {
        "planet": [fav.serialize() for fav in fav_planet],
        "people": [fav.serialize() for fav in fav_people]
    }

    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:id>', methods=['POST'])
def handle_add_favorite_planet(id):
    user_id = 1
    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({'msg': 'planet not found'}), 404
    
    new_favorite = FavoritePlanet(id_user=user_id, id_planet=id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(), 201

@app.route('/favorite/people/<int:id>', methods=['POST'])
def handle_add_favorite_people(id):
    user_id = 1
    person = People.query.get(id)
    if person is None:
        return jsonify({'msg': 'planet not found'}), 404
    
    new_favorite = FavoritePeople(id_user=user_id, id_people=id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(), 201

@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def handle_delete_favorite_planet(id):
    user_id = 1
    favorite = FavoritePlanet.query.filter_by(id_user=user_id, id_planet=id).first()
    if favorite is None:
        return jsonify({'msg': 'favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify(), 204

@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def handle_delete_favorite_people(id):
    user_id = 1
    favorite = FavoritePeople.query.filter_by(id_user=user_id, id_people=id).first()
    if favorite is None:
        return jsonify({'msg': 'favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify(), 204

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
