from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS — allows React (port 3000) to call Flask (port 5000)
# Without this, browsers will block the requests for security
CORS(app)

# Import and register the routes Blueprint
from routes.review_routes import review_bp
app.register_blueprint(review_bp)

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    print(f"Starting Flask server on port {port}...")
    app.run(debug=True, port=port)