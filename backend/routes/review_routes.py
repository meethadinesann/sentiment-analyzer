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
import threading

review_bp = Blueprint("reviews", __name__)

# Track which products are currently being scraped
scraping_status = {}


def scrape_in_background(product_name):
    """
    Runs scraping in a background thread.
    Updates scraping_status when done.
    """
    try:
        scraping_status[product_name] = "scraping"
        raw_reviews = run_scraper(product_name)

        if raw_reviews:
            analyzed_reviews = analyze_reviews(raw_reviews)
            insert_reviews_to_db(analyzed_reviews, product_name)
            scraping_status[product_name] = "done"
        else:
            scraping_status[product_name] = "error"

    except Exception as e:
        print(f"Background scraping error: {e}")
        scraping_status[product_name] = "error"


@review_bp.route("/api/scrape", methods=["POST"])
def scrape():
    """
    POST /api/scrape
    Starts scraping in background and returns immediately.
    """
    data = request.get_json()

    if not data or "product_name" not in data:
        return jsonify({"error": "product_name is required"}), 400

    product_name = data["product_name"].strip()

    if not product_name:
        return jsonify({"error": "product_name cannot be empty"}), 400

    # Already in database
    if product_exists_in_db(product_name):
        return jsonify({
            "message": f"Reviews for '{product_name}' already exist.",
            "status": "done",
            "scraped": False
        }), 200

    # Already being scraped
    if scraping_status.get(product_name) == "scraping":
        return jsonify({
            "message": "Scraping already in progress.",
            "status": "scraping"
        }), 200

    # Start scraping in background thread
    thread = threading.Thread(
        target=scrape_in_background,
        args=(product_name,)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        "message": "Scraping started in background.",
        "status": "scraping"
    }), 202


@review_bp.route("/api/scrape/status", methods=["GET"])
def scrape_status():
    """
    GET /api/scrape/status?product=oppo phone
    Returns current scraping status for a product.
    """
    product_name = request.args.get("product")

    if not product_name:
        return jsonify({"error": "product is required"}), 400

    if product_exists_in_db(product_name):
        return jsonify({"status": "done"}), 200

    status = scraping_status.get(product_name, "not_started")
    return jsonify({"status": status}), 200


@review_bp.route("/api/reviews", methods=["GET"])
def get_reviews():
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
    product_name = request.args.get("product")
    if not product_name:
        return jsonify({"error": "product query parameter is required"}), 400

    summary = get_sentiment_summary_from_db(product_name)
    total = sum(summary.values())

    if total == 0:
        return jsonify({"error": "No reviews found for this product"}), 404

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
    products = get_all_products()
    return jsonify({
        "products": products,
        "count": len(products)
    }), 200


@review_bp.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "API is running"}), 200