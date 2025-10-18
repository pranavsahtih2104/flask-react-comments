# backend/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS 

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_object=None):
    app = Flask(__name__)
    CORS(app) 

    # Default config — change DATABASE_URL in production
    app.config.from_object('app.config.DefaultConfig' if config_object is None else config_object)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .comments import comments_bp
    app.register_blueprint(comments_bp, url_prefix='/api/comments')

    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health():
        return {"status": "ok"}, 200

    # Root route (optional)
    @app.route('/', methods=['GET'])
    def root():
        return {"message": "Backend is running!"}, 200

    return app
