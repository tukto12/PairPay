from flask import Flask
from flask_cors import CORS
from app.config import config_by_name
from app.db import db
from app.routes.bill_api import bill_bp
from app.routes.auth import auth_bp
from app.db.db_init import init_db
from flask_jwt_extended import JWTManager


class AppFactory:
    def __init__(self, config_name="development"):
        self.config_name = config_name
        self.app = Flask(__name__)

    def _load_config(self):
        self.app.config.from_object(config_by_name.get(
            self.config_name, config_by_name["development"]))

    def _initialize_cors(self):
        CORS(self.app, resources={r"/*": {"origins": self.app.config['CORS_ORIGINS'],
                                          "methods": self.app.config['CORS_METHODS'],
                                          "allow_headers": self.app.config['CORS_ALLOW_HEADERS']}})

    def _register_blueprints(self):
        self.app.register_blueprint(auth_bp)
        self.app.register_blueprint(bill_bp)

    def _initialize_db(self):
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            init_db()

    def _initialize_jwt(self):
        self.jwt = JWTManager(self.app)

    def create_app(self):
        self._load_config()
        self._initialize_cors()
        self._initialize_db()
        self._initialize_jwt()
        self._register_blueprints()
        return self.app


def create_app(config_name="development"):
    factory = AppFactory(config_name)
    return factory.create_app()