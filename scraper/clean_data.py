import pandas as pd
import re


def load_data(filename="data/raw_reviews.csv"):
    """
    Loads the raw CSV file into a pandas DataFrame.
    """
    df = pd.read_csv(filename)
    print(f"Loaded {len(df)} reviews.")
    return df


def remove_duplicates(df):
    """
    Removes duplicate reviews based on the body text.
    Same review body appearing twice = duplicate.
    """
    before = len(df)
    df = df.drop_duplicates(subset=["body"])
    after = len(df)
    print(f"Removed {before - after} duplicate reviews. {after} remaining.")
    return df


def handle_missing_values(df):
    """
    Handles missing values in the DataFrame.
    - Missing title: replace with 'No Title'
    - Missing rating: replace with 0.0 (we'll flag these as unrated)
    """
    df["title"] = df["title"].fillna("No Title")
    df["rating"] = df["rating"].fillna(0.0)
    print(f"Missing values handled.")
    print(df.isnull().sum())
    return df


def clean_text(text):
    """
    Cleans a single review text string.
    Removes special characters, extra spaces, and normalizes the text.
    """
    if not isinstance(text, str):
        return ""

    # Remove URLs (some reviews paste links)
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove HTML tags if any slipped through
    text = re.sub(r"<.*?>", "", text)

    # Remove special characters but keep letters, numbers, spaces
    # and basic punctuation like . , ! ?
    text = re.sub(r"[^a-zA-Z0-9\s.,!?]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Convert to lowercase
    text = text.lower()

    return text


def clean_reviews(df):
    """
    Applies text cleaning to the body and title columns.
    """
    df["body"] = df["body"].apply(clean_text)
    df["title"] = df["title"].apply(clean_text)

    # Remove rows where body became empty after cleaning
    before = len(df)
    df = df[df["body"].str.strip() != ""]
    after = len(df)
    print(f"Removed {before - after} empty reviews after cleaning. {after} remaining.")

    return df


def save_clean_data(df, filename="data/cleaned_reviews.csv"):
    """
    Saves the cleaned DataFrame to a new CSV file.
    Always save cleaned data separately — never overwrite raw data.
    """
    df.to_csv(filename, index=False)
    print(f"Cleaned data saved to {filename}")


def main():
    print("=== Starting Data Cleaning ===\n")

    # Step 1: Load
    df = load_data()
    print()

    # Step 2: Remove duplicates
    df = remove_duplicates(df)
    print()

    # Step 3: Handle missing values
    df = handle_missing_values(df)
    print()

    # Step 4: Clean text
    df = clean_reviews(df)
    print()

    # Step 5: Final summary
    print("=== Cleaning Complete ===")
    print(f"Final dataset: {len(df)} reviews")
    print(f"\nRating distribution:")
    print(df["rating"].value_counts().sort_index())
    print(f"\nSample cleaned reviews:")
    print(df[["rating", "title", "body"]].head(3).to_string())

    # Step 6: Save
    save_clean_data(df)


if __name__ == "__main__":
    main()