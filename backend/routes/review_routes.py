from flask import Blueprint, request, jsonify
from services.scraper_service import run_scraper
from services.sentiment_service import analyze_reviews
from services.database_service import (
    get_reviews_from_db,
    insert_reviews_to_db,
    get_sentiment_summary_from_db,
    product_exists_in_db,
    get_all_products
)

# Blueprint is Flask's way of organizing routes into separate files
# Think of it like a section of the menu
review_bp = Blueprint("reviews", __name__)


@review_bp.route("/api/scrape", methods=["POST"])
def scrape():
    """
    POST /api/scrape
    Body: {"product_name": "boAt earphones"}

    Scrapes reviews for a product, runs sentiment analysis,
    and stores results in MongoDB.
    """
    # Get the product name from the request body
    data = request.get_json()

    if not data or "product_name" not in data:
        return jsonify({"error": "product_name is required"}), 400

    product_name = data["product_name"].strip()

    if not product_name:
        return jsonify({"error": "product_name cannot be empty"}), 400

    # Check if we already have this product in the database
    if product_exists_in_db(product_name):
        return jsonify({
            "message": f"Reviews for '{product_name}' already exist in database.",
            "scraped": False
        }), 200

    # Run the scraper
    print(f"Starting scraper for: {product_name}")
    raw_reviews = run_scraper(product_name)

    if not raw_reviews:
        return jsonify({"error": "No reviews found for this product"}), 404

    # Run sentiment analysis
    analyzed_reviews = analyze_reviews(raw_reviews)

    # Store in MongoDB
    count = insert_reviews_to_db(analyzed_reviews, product_name)

    return jsonify({
        "message": f"Successfully scraped and analysed {count} reviews.",
        "product": product_name,
        "count": count,
        "scraped": True
    }), 201


@review_bp.route("/api/reviews", methods=["GET"])
def get_reviews():
    """
    GET /api/reviews?product=boAt earphones

    Returns all reviews for a product from MongoDB.
    """
    product_name = request.args.get("product")

    if not product_name:
        return jsonify({"error": "product query parameter is required"}), 400

    reviews = get_reviews_from_db(product_name)

    if not reviews:
        return jsonify({"error": "No reviews found for this product"}), 404

    return jsonify({
        "product": product_name,
        "count": len(reviews),
        "reviews": reviews
    }), 200


@review_bp.route("/api/sentiment", methods=["GET"])
def get_sentiment():
    """
    GET /api/sentiment?product=boAt earphones

    Returns sentiment summary for a product.
    """
    product_name = request.args.get("product")

    if not product_name:
        return jsonify({"error": "product query parameter is required"}), 400

    summary = get_sentiment_summary_from_db(product_name)
    total = sum(summary.values())

    if total == 0:
        return jsonify({"error": "No reviews found for this product"}), 404

    # Calculate percentages
    percentages = {}
    for label, count in summary.items():
        percentages[label] = round((count / total) * 100, 1)

    return jsonify({
        "product": product_name,
        "total": total,
        "counts": summary,
        "percentages": percentages
    }), 200


@review_bp.route("/api/products", methods=["GET"])
def get_products():
    """
    GET /api/products

    Returns all product names stored in the database.
    """
    products = get_all_products()
    return jsonify({
        "products": products,
        "count": len(products)
    }), 200


@review_bp.route("/api/health", methods=["GET"])
def health_check():
    """
    GET /api/health

    Simple health check to confirm the API is running.
    """
    return jsonify({"status": "ok", "message": "API is running"}), 200