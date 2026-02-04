from flask import Flask
from flask_cors import CORS
from config import Config
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)
register_routes(app)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://encore-fm-frontend.onrender.com"
        ]
    }
})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=app.config.get("PORT", 5000),
        debug=app.config.get("DEBUG", True)
    )