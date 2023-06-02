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
from models import db, User, People, Planets, Vehicles
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

# EMPIEZAN LOS ENDPOINTS

#Endpoints GET
@app.route('/user', methods=['GET'])
def handle_user(): 

    results = User.query.all()
    if not results:
        return "" , 204

    users_list = list(map(lambda item: item.serialize(),results))


    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "results": users_list
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def handle_people(): 

    results = People.query.all()
    if not results:
        return "" , 204

    people_list = list(map(lambda item: item.serialize(),results))


    response_body = {
        "msg": "Hello, this is your GET /people response ",
        "results": people_list
    }

    return jsonify(response_body), 200

@app.route('/vehicles', methods=['GET'])
def handle_vehicles(): 

    results = Vehicles.query.all()
    if not results:
        return "" , 204

    vehicles_list = list(map(lambda item: item.serialize(),results))


    response_body = {
        "msg": "Hello, this is your GET /vehicles response ",
        "results": vehicles_list
    }

    return jsonify(response_body), 200   

@app.route('/planets', methods=['GET'])
def handle_planets(): 

    results = Planets.query.all()
    if not results:
        return "" , 204
        
    planets_list = list(map(lambda item: item.serialize(),results))


    response_body = {
        "msg": "Hello, this is your GET /planets response ",
        "results": planets_list
    }

    return jsonify(response_body), 200       


# endpoint para consultar un dato en la tabla user
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    print(id)

    user = User.query.filter_by(id=id).first()
  
    if user is None:
        return jsonify({"msg":"Este usuario no existe"}), 404
    

    response_body = {
        "result": user.serialize()
    }

    return jsonify(response_body), 200


# endpoint para consultar un dato en la tabla people
@app.route('/people/<int:id>', methods=['GET'])
def get_people(id):
    print(id)

    people = People.query.filter_by(id=id).first()
  
    if people is None:
        return jsonify({"msg":"Esta persona no existe"}), 404
    

    response_body = {
        "result": people.serialize()
    }

    return jsonify(response_body), 200

# endpoint para consultar un dato en la tabla vehicles
@app.route('/vehicles/<int:id>', methods=['GET'])
def get_vehicles(id):
    print(id)

    vehicles = Vehicles.query.filter_by(id=id).first()
  
    if vehicles is None:
        return jsonify({"msg":"Este vehiculo no existe"}), 404
    

    response_body = {
        "result": vehicles.serialize()
    }

    return jsonify(response_body), 200    

# endpoint para consultar un dato en la tabla Planets
@app.route('/planets/<int:id>', methods=['GET'])
def get_planets(id):
    print(id)

    planets = Planets.query.filter_by(id=id).first()
  
    if planets is None:
        return jsonify({"msg":"Este planeta no existe"}), 404
    

    response_body = {
        "result": planets.serialize()
    }

    return jsonify(response_body), 200     

# endpoint para crear un dato en la tabla User
@app.route('/user', methods=['POST'])
def create_user():

    body = json.loads(request.data)
    # json.loads(request.body.decode(encoding='UTF-8'))
    print(body)
    user = User(email=body["email"], last_name=body["last_name"], name=body["name"], password=body["password"], is_active=body["is_active"])
    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg": "El usuario ha sido creado",
    }
    return jsonify(response_body), 200    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
