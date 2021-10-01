from flask import Flask
from views import views
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

app.register_blueprint(views, url_prefix = "/")

def createDatabase(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Database created.")

# from models import User
createDatabase(app)

if __name__ == '__main__':
    app.run(debug = True)

