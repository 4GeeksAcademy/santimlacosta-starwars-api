from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True,  nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(20), nullable=False)
    eye_color = db.Column(db.String(20), nullable=False)  
    skin_color = db.Column(db.String(20), nullable=False) 
    hair_color = db.Column(db.String(20), nullable=False)   
    mass = db.Column(db.Integer, nullable=False) 
    height = db.Column(db.Integer, nullable=False) 

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "mass": self.mass,
            "height": self.height
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True,  nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)  
    gravity = db.Column(db.String(50), nullable=False) 
    population = db.Column(db.Integer, nullable=False) 
    climate = db.Column(db.String(50), nullable=False) 
    terrain = db.Column(db.String(50), nullable=False) 
    surface_water = db.Column(db.Integer, nullable=False)   
        
    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }
    
class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True,  nullable=False)
    model = db.Column(db.String(50), nullable=False)
    vehicle_class = db.Column(db.String(20), nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)  
    cost = db.Column(db.Integer, nullable=False) 
    length = db.Column(db.Integer, nullable=False)  
    crew = db.Column(db.Integer, nullable=False)  
    passengers = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False) 
    cargo_capacity = db.Column(db.Integer, nullable=False) 
    consumables = db.Column(db.String(50), nullable=False)    
        
    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost": self.cost,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "speed": self.speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables
        }

class Favorite_people(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   

    def __repr__(self):
        return '<Favorite_people %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "user_id": self.user_id,
        }
    
class Favorite_planets(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  

    def __repr__(self):
        return '<Favorite_planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planets_id": self.planets_id,
            "user_id": self.user_id,
        }
    
class Favorite_vehicles(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
        
    def __repr__(self):
        return '<Favorite_vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "vehicles_id": self.vehicles_id,
            "user_id": self.user_id,
        }