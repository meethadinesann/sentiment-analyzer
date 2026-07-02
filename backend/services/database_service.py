import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_database():
    """
    Returns a connection to the MongoDB database.
    """
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI not found in .env file")

    client = MongoClient(mongo_uri)
    db = client["sentiment_analyzer"]
    return db


def get_reviews_from_db(product_name):
    """
    Retrieves all reviews for a product from MongoDB.
    """
    db = get_database()
    collection = db["reviews"]
    reviews = list(collection.find({"product": product_name}))

    # Convert ObjectId to string so it can be sent as JSON
    for review in reviews:
        review["_id"] = str(review["_id"])

    return reviews


def insert_reviews_to_db(reviews, product_name):
    """
    Inserts a list of review dictionaries into MongoDB.
    """
    db = get_database()
    collection = db["reviews"]

    for review in reviews:
        review["product"] = product_name

    result = collection.insert_many(reviews)
    return len(result.inserted_ids)


def get_sentiment_summary_from_db(product_name):
    """
    Returns sentiment counts for a product using aggregation.
    Example output: {"Positive": 43, "Negative": 1, "Neutral": 2}
    """
    db = get_database()
    collection = db["reviews"]

    pipeline = [
        {"$match": {"product": product_name}},
        {"$group": {
            "_id": "$sentiment_label",
            "count": {"$sum": 1}
        }}
    ]

    results = list(collection.aggregate(pipeline))

    summary = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for item in results:
        if item["_id"] in summary:
            summary[item["_id"]] = item["count"]

    return summary


def product_exists_in_db(product_name):
    """
    Checks if a product already has reviews in MongoDB.
    Returns True if found, False if not.
    """
    db = get_database()
    collection = db["reviews"]

    count = collection.count_documents({"product": product_name})
    return count > 0


def get_all_products():
    """
    Returns a list of all unique product names in the database.
    """
    db = get_database()
    collection = db["reviews"]

    products = collection.distinct("product")
    return products