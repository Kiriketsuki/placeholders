from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
import pandas as pd
# from .models import import_buildings

db = SQLAlchemy()
DB_NAME = "database.db"

def createApp():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'abc123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix = "/")

    createDatabase(app, DB_NAME)
    login_manager = LoginManager()
    login_manager.login_view = 'views.landing'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # from .initialize_db import init_db
    # with app.app_context():
    #     init_db()
    return app
    
def createDatabase(app, name):
    if not os.path.exists('website/' + name):
        db.create_all(app=app)

        from .initialize_db import init_db
        with app.app_context():
            init_db()
            
        print("Database created.")

