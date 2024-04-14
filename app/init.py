from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Importar las rutas de la aplicación Flask
        from . import routes

        # Registrar otros blueprints si existen
        # app.register_blueprint(xyz_blueprint)

        return app