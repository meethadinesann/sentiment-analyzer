import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_database():
    """
    Creates and returns a connection to MongoDB Atlas.
    Think of this like opening a filing cabinet.
    """
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise ValueError("MONGO_URI not found in .env file")

    # Create a MongoDB client (connection to the server)
    client = MongoClient(mongo_uri)

    # Access our specific database
    # If it doesn't exist yet, MongoDB creates it automatically
    db = client["sentiment_analyzer"]

    return db


def insert_reviews(reviews_data, product_name):
    """
    Inserts scraped and analysed reviews into MongoDB.
    Each review becomes one document in the 'reviews' collection.
    """
    db = get_database()

    # Access the 'reviews' collection
    # Like opening a specific drawer in the filing cabinet
    collection = db["reviews"]

    # Add product name to each review document
    for review in reviews_data:
        review["product"] = product_name

    # Insert all reviews at once
    result = collection.insert_many(reviews_data)
    print(f"Inserted {len(result.inserted_ids)} reviews into MongoDB.")
    return result


def get_reviews(product_name):
    """
    Retrieves all reviews for a specific product from MongoDB.
    """
    db = get_database()
    collection = db["reviews"]

    # Find all documents where product matches
    # {} means no filter - returns everything
    reviews = list(collection.find({"product": product_name}))

    # MongoDB adds an '_id' field automatically to every document
    # We convert it to string because it's a special MongoDB object
    for review in reviews:
        review["_id"] = str(review["_id"])

    print(f"Retrieved {len(reviews)} reviews for '{product_name}'.")
    return reviews


def get_sentiment_summary(product_name):
    """
    Returns sentiment counts for a product.
    Example: {"Positive": 43, "Negative": 1, "Neutral": 2}
    """
    db = get_database()
    collection = db["reviews"]

    # MongoDB aggregation pipeline
    # Think of it like a series of filters and transformations
    pipeline = [
        # Stage 1: Filter by product name
        {"$match": {"product": product_name}},

        # Stage 2: Group by sentiment_label and count
        {"$group": {
            "_id": "$sentiment_label",
            "count": {"$sum": 1}
        }}
    ]

    results = list(collection.aggregate(pipeline))

    # Convert to a clean dictionary
    summary = {}
    for item in results:
        summary[item["_id"]] = item["count"]

    return summary


def load_and_insert_from_csv(csv_path="data/sentiment_results.csv", product_name="boAt earphones"):
    """
    Reads the sentiment results CSV and inserts into MongoDB.
    This is our bridge between Phase 4 (CSV) and Phase 5 (MongoDB).
    """
    df = pd.read_csv(csv_path)

    # Convert DataFrame rows to list of dictionaries
    reviews_data = df.to_dict(orient="records")

    print(f"Loading {len(reviews_data)} reviews into MongoDB...")
    insert_reviews(reviews_data, product_name)


# --- Main execution ---
if __name__ == "__main__":
    print("=== Testing MongoDB Connection ===\n")

    # Test 1: Insert data
    print("Step 1: Inserting reviews from CSV...")
    load_and_insert_from_csv(
        csv_path="data/sentiment_results.csv",
        product_name="boAt earphones"
    )

    print()

    # Test 2: Retrieve data
    print("Step 2: Retrieving reviews from MongoDB...")
    reviews = get_reviews("boAt earphones")
    print(f"First review: {reviews[0] if reviews else 'None'}")

    print()

    # Test 3: Get sentiment summary
    print("Step 3: Getting sentiment summary...")
    summary = get_sentiment_summary("boAt earphones")
    print(f"Sentiment summary: {summary}")