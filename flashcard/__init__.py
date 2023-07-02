from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'anay'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file.db'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix = "/")
    app.register_blueprint(auth,url_prefix = "/")


    from .models import User, Note,Deck

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('flashcard/' + "file.db"):
        db.create_all(app=app)
        print('Created Database!')
