import os
from flask_admin import Admin
from models import db, User, People, Planets, Vehicles, Favorite_people, Favorite_planets, Favorite_vehicles
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    class Favorite_peopleAdmin(ModelView):
        column_list = ("id", "people_id", "user_id")
        form_columns = ("people_id", "user_id")
        column_hide_backrefs = False

    class Favorite_planetsAdmin(ModelView):
        column_list = ("id", "planets_id", "user_id")
        form_columns = ("planets_id", "user_id")
        column_hide_backrefs = False

    class Favorite_vehiclesAdmin(ModelView):
        column_list = ("id", "vehicles_id", "user_id")
        form_columns = ("vehicles_id", "user_id")
        column_hide_backrefs = False

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(Vehicles, db.session))
    admin.add_view(Favorite_peopleAdmin(Favorite_people, db.session))
    admin.add_view(Favorite_planetsAdmin(Favorite_planets, db.session))
    admin.add_view(Favorite_vehiclesAdmin(Favorite_vehicles, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))