import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon (word scores dictionary)
# This only needs to run once — VADER uses a built-in dictionary
# of words and their sentiment scores
nltk.download("vader_lexicon")


def load_cleaned_data(filename="data/cleaned_reviews.csv"):
    """
    Loads the cleaned reviews CSV.
    """
    df = pd.read_csv(filename)
    print(f"Loaded {len(df)} cleaned reviews.")
    return df


def get_sentiment_label(compound_score):
    """
    Converts a VADER compound score into a human-readable label.

    VADER's official thresholds:
    - compound >= 0.05  → Positive
    - compound <= -0.05 → Negative
    - anything between  → Neutral
    """
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def analyze_sentiment(df):
    """
    Runs VADER sentiment analysis on every review body.
    Adds two new columns: sentiment_score and sentiment_label.
    """
    # Initialize the VADER analyzer
    analyzer = SentimentIntensityAnalyzer()

    sentiment_scores = []
    sentiment_labels = []

    for review in df["body"]:
        # Get the sentiment scores for this review
        # polarity_scores() returns a dictionary like:
        # {'neg': 0.0, 'neu': 0.5, 'pos': 0.5, 'compound': 0.6}
        scores = analyzer.polarity_scores(review)

        # We only care about the compound score
        compound = scores["compound"]

        sentiment_scores.append(compound)
        sentiment_labels.append(get_sentiment_label(compound))

    df["sentiment_score"] = sentiment_scores
    df["sentiment_label"] = sentiment_labels

    return df


def print_summary(df):
    """
    Prints a summary of the sentiment analysis results.
    """
    total = len(df)
    counts = df["sentiment_label"].value_counts()

    print("\n=== Sentiment Analysis Summary ===")
    print(f"Total reviews analysed: {total}")
    print()

    for label in ["Positive", "Negative", "Neutral"]:
        count = counts.get(label, 0)
        percentage = (count / total) * 100
        print(f"{label}: {count} reviews ({percentage:.1f}%)")

    print()
    print("Sample results:")
    print(df[["body", "sentiment_score", "sentiment_label"]].head(5).to_string())


def save_sentiment_data(df, filename="data/sentiment_results.csv"):
    """
    Saves the DataFrame with sentiment columns to a new CSV file.
    """
    df.to_csv(filename, index=False)
    print(f"\nSentiment results saved to {filename}")


def main():
    print("=== Starting Sentiment Analysis ===\n")

    # Step 1: Load cleaned data
    df = load_cleaned_data()

    # Step 2: Run sentiment analysis
    df = analyze_sentiment(df)

    # Step 3: Print summary
    print_summary(df)

    # Step 4: Save results
    save_sentiment_data(df)


if __name__ == "__main__":
    main()