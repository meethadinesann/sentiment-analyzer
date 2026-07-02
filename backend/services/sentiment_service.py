import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

# Download vader lexicon if not already downloaded
nltk.download("vader_lexicon", quiet=True)


def clean_text(text):
    """
    Cleans review text before sentiment analysis.
    """
    if not isinstance(text, str):
        return ""

    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s.,!?]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.lower()

    return text


def get_sentiment_label(compound_score):
    """
    Converts VADER compound score to a label.
    """
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def analyze_reviews(reviews):
    """
    Takes a list of review dictionaries and adds
    sentiment_score and sentiment_label to each one.
    Returns the updated list.
    """
    analyzer = SentimentIntensityAnalyzer()

    for review in reviews:
        body = clean_text(review.get("body", ""))
        scores = analyzer.polarity_scores(body)
        compound = scores["compound"]

        review["sentiment_score"] = compound
        review["sentiment_label"] = get_sentiment_label(compound)

    return reviews