from flask import Flask
from flask_cors import CORS
from config import Config
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={
    r"/api/*": {
        "origins": [app.config['FRONTEND_URL']],
        "supports_credentials": True
    }
})
register_routes(app)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=app.config.get("PORT", 5000),
        debug=app.config.get("DEBUG", True)
    )