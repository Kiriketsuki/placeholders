from flask import Flask
from views import views
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'
app.register_blueprint(views, url_prefix = "/")

if __name__ == '__main__':
    app.run(debug = True)