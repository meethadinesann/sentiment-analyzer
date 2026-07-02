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

    # Add SSL settings for Render compatibility
    client = MongoClient(
        mongo_uri,
        tls=True,
        tlsAllowInvalidCertificates=True
    )

    db = client["sentiment_analyzer"]
    return db


def get_reviews_from_db(product_name):
    db = get_database()
    collection = db["reviews"]
    reviews = list(collection.find({"product": product_name}))
    for review in reviews:
        review["_id"] = str(review["_id"])
    return reviews


def insert_reviews_to_db(reviews, product_name):
    db = get_database()
    collection = db["reviews"]
    for review in reviews:
        review["product"] = product_name
    result = collection.insert_many(reviews)
    return len(result.inserted_ids)


def get_sentiment_summary_from_db(product_name):
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
    db = get_database()
    collection = db["reviews"]
    count = collection.count_documents({"product": product_name})
    return count > 0


def get_all_products():
    db = get_database()
    collection = db["reviews"]
    products = collection.distinct("product")
    return products