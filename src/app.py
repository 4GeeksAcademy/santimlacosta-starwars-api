"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, Favorite_people, Favorite_planets, Favorite_vehicles #importar todas las tablas
#from models import Person

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "keySecret"  # Change this!
jwt = JWTManager(app)

bcrypt = Bcrypt(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# EMPIEZAN LOS ENDPOINTS

# ENDPOINTS ACCESO/REGISTRO

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)


    user = User.query.filter_by(email=email).first() #Comprobamos si existe el email en la BBDD


    if user is None:
       return jsonify({"msg": "Este usuario no exsite"}), 404 

    #None.email
    if email != user.email or password != user.password:
        return jsonify({"msg": "Las credenciales no son correctas"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


@app.route("/signup", methods=["POST"])
def signup():

    name = request.json.get("name", None)
    last_name = request.json.get("last_name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if name is None:
        return jsonify({"msg" : "Falta el nombre"}),400
    
    if last_name is None:
        return jsonify({"msg" : "Falta el apellido"}),400
                       
    if email is None:
        return jsonify({"msg" : "Falta el email"}),400
                       
    if password is None:
        return jsonify({"msg" : "Falta el password"}),400
                       
    user = User.query.filter_by(email=email).first()

    if user != None:
         return jsonify({"msg" : "Este usuario ya existe"}),401
    
    pw_hash = bcrypt.generate_password_hash("password").decode("utf-8")


    add_user = User(name=name, last_name=last_name, email=email, password=pw_hash)

    db.session.add(add_user)
    db.session.commit()

    return jsonify({"msg" : "Usuario creado correctamente"}),200
        



#  ENDPOINTS RUTAS PROTEGIDAS
@app.route("/profile", methods=["GET"])
@jwt_required()
def get_info_profile():
     # Access the identity of the current user with get_jwt_identity#     
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first() #Hacemos consulta a la BBDD de cualquier dato
    
    print(user.serialize()) # Recibimos el objeto con toda la info
    #return jsonify(logged_in_as=current_user), 200
    return jsonify({"user":user.serialize()}), 200


#   ENPOINTS GET TABLAS USER, PEOPLE, PLANETS, VEHICLES

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
    print(results)
    if not results:
        return "", 204

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


 # ENDPOINT PARA CONSULTAR UN DATO EN TABLA USER
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


# ENDPOINT PARA CONSULTAR UN DATO EN TABLA PEOPLE
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

# ENDPOINT PARA CONSULTAR UN DATO EN TABLA VEHICLES
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

# ENDPOINT PARA CONSULTAR UN DATO EN TABLA PLANETS
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
# ENDPOINTS PARA FAVORITE TABLES
# ENDPOINT PARA LISTAR TODOS LOS FAVORITOS DE UN USER
@app.route('/user/favorites/<int:user_id>', methods=['GET'])
def favorites_user(user_id):

    user= User.query.get(user_id)
    if user is None:
       return jsonify({"msg":"Este usuario no existe"})

    result1 = Favorite_people.query.filter_by(user_id=user_id).all()
    favorite_people_list = list(map(lambda item: item.serialize(),result1 ))
  
    result2 = Favorite_planets.query.filter_by(user_id=user_id).all()
    favorite_planets_list = list(map(lambda item: item.serialize(),result2 ))

    result3 = Favorite_vehicles.query.filter_by(user_id=user_id).all()
    favorite_vehicles_list = list(map(lambda item: item.serialize(),result3 ))


    if not [*favorite_people_list,*favorite_planets_list,*favorite_vehicles_list] : 
        return jsonify({"msg":"Este usuario no tiene favoritos"})

    response_body = {
         "results": [*favorite_people_list,*favorite_planets_list,*favorite_vehicles_list]

    }

    return jsonify(response_body), 200

# ENDPOINT PARA CREAR UNA PERSONA FAVORITA
@app.route('/favorites/people/<int:people_id>/<int:user_id>', methods=['POST'])
def create_people_favorite(people_id,user_id):

    user = User.query.filter_by(id=user_id).first()
    # user = User.query.filter_by(id=body["user_id"]).first() # En el caso que enviemos el user_id en el body de la petición
    people = People.query.get(people_id) 
    people_favorite = Favorite_people.query.filter_by(people_id=people_id  ,user_id=user_id).first()


    if user is None:
        return jsonify({"msg":"Este usuario no existe"}), 404
    
    if people is None:
        return jsonify({"msg":"Esta persona no existe"}), 404
   
    if people_favorite: 
        return jsonify({"msg":"Esta persona ya estaba marcada como favorito"}), 208
    


    favorite_people = Favorite_people(user_id=user_id, people_id=people_id)
    db.session.add(favorite_people)
    db.session.commit()

    return jsonify({"msg":"Has añadido esta persona como favorito"}), 200 

# ENDPOINT PARA CREAR UN PLANETA FAVORITO
@app.route('/favorites/planets/<int:planets_id>/<int:user_id>', methods=['POST'])
def create_planets_favorite(planets_id,user_id):

    user = User.query.filter_by(id=user_id).first()
    planets = Planets.query.get(planets_id) 
    planets_favorite = Favorite_planets.query.filter_by(planets_id=planets_id,user_id=user_id).first()


    if user is None:
        return jsonify({"msg":"Este usuario no existe"}), 404
    
    if planets is None:
        return jsonify({"msg":"Este planeta no existe"}), 404
   
    if planets_favorite: 
        return jsonify({"msg":"Este planeta ya estaba marcado como favorito"}), 208
    


    favorite_planets = Favorite_planets(user_id=user_id, planets_id=planets_id)
    db.session.add(favorite_planets)
    db.session.commit()

    return jsonify({"msg":"Has añadido este planeta como favorito"}), 200 

# ENDPOINT PARA CREAR UN VEHICULO FAVORITO
@app.route('/favorites/vehicles/<int:vehicles_id>/<int:user_id>', methods=['POST'])
def create_vehicles_favorite(vehicles_id,user_id):

    user = User.query.filter_by(id=user_id).first()
    vehicles = Vehicles.query.get(vehicles_id) 
    vehicles_favorite = Favorite_vehicles.query.filter_by(vehicles_id=vehicles_id, user_id=user_id).first()


    if user is None:
        return jsonify({"msg":"Este usuario no existe"}), 404
    
    if vehicles is None:
        return jsonify({"msg":"Este vehiculo no existe"}), 404
   
    if vehicles_favorite: 
        return jsonify({"msg":"Este vehiculo ya estaba marcado como favorito"}), 208
    


    favorite_vehicles = Favorite_vehicles(user_id=user_id, vehicles_id=vehicles_id)
    db.session.add(favorite_vehicles)
    db.session.commit()

    return jsonify({"msg":"Has añadido este vehiculo como favorito"}), 200 


# ENDPOINT PARA BORRAR UNA PERSONA FAVORITA DE UN USUARIO
@app.route('/favorites/people/<int:people_id>/<int:user_id>', methods=['DELETE'])
def delete_people_favorite(people_id,user_id):

    people_favorite = Favorite_people.query.filter_by(people_id=people_id).first()
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return jsonify({"msg":"Este usuario no existe"}), 404
   
    if people_favorite is None:
        return jsonify({"msg":"Esta persona no existe"}), 404

 
    db.session.delete(people_favorite)
    db.session.commit()
    
    return jsonify({"msg":"La persona ha sido borrada de Favoritos"}), 200


# ENDPOINT PARA BORRAR UN PLANETA FAVORITA DE UN USUARIO
@app.route('/favorites/planets/<int:planets_id>/<int:user_id>', methods=['DELETE'])
def delete_people_favorite(planets_id,user_id):

    planets_favorite = Favorite_planets.query.filter_by(planets_id=planets_id).first()
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return jsonify({"msg":"Este usuario no existe"}), 404
   
    if planets_favorite is None:
        return jsonify({"msg":"Este planeta no existe"}), 404

 
    db.session.delete(planets_favorite)
    db.session.commit()
    
    return jsonify({"msg":"El planeta ha sido borrado de Favoritos"}), 200


# ENDPOINT PARA BORRAR UN VEHICULO FAVORITA DE UN USUARIO
@app.route('/favorites/vehicles/<int:vehicles_id>/<int:user_id>', methods=['DELETE'])
def delete_people_favorite(vehicles_id,user_id):

    vehicles_favorite = Favorite_vehicles.query.filter_by(vehicles_id=vehicles_id).first()
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return jsonify({"msg":"Este usuario no existe"}), 404
   
    if vehicles_favorite is None:
        return jsonify({"msg":"Este vehiculo no existe"}), 404

 
    db.session.delete(vehicles_favorite)
    db.session.commit()
    
    return jsonify({"msg":"El vehiculo ha sido borrado de Favoritos"}), 200


# ENDPOINT PARA CREAR UN DATO EN TABLA USER
@app.route('/user', methods=['POST'])
def create_user():

    body = json.loads(request.data)
    print(body)
    
    if body == None:
        return jsonify({"msg":"No hay información para procesar"}), 404
    
    if not "email" in body:
        return jsonify({"msg":"Es obligatorio indicar un email"}), 404
    
    email = User.query.filter_by(email=body["email"]).first()

    if email != None: 
        return jsonify({"msg":"Existe un usuario con este email"}), 404

    if not "name" in body:
        return jsonify({"msg":"Es obligatorio indicar un nombre"}), 404
    
    if not "last_name" in body:
        return jsonify({"msg":"Es obligatorio indicar un apellido"}), 404

    if not "password" in body:
        return jsonify({"msg":"Es obligatorio indicar un password"}), 404
    

    user = User(email=body["email"], last_name=body["last_name"], name=body["name"], password=body["password"])
    
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
