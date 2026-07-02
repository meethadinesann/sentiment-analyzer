from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

from routes.review_routes import review_bp
app.register_blueprint(review_bp)

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    print(f"Starting Flask server on port {port}...")
    # Use 0.0.0.0 so Render can access it externally
    app.run(debug=False, host="0.0.0.0", port=port)