import { getReviews, getSentiment, scrapeProduct, checkScrapeStatus } from "../api/api";
import { useState } from "react";
import SearchBar from "../components/SearchBar";
import ReviewCard from "../components/ReviewCard";
import SentimentChart from "../components/SentimentChart";
import StatsCards from "../components/StatsCards";
import SentimentBarChart from "../components/BarChart";
import Spinner from "../components/Spinner";
import SearchHistory from "../components/SearchHistory";
import Pagination from "../components/Pagination";
import { getReviews, getSentiment, scrapeProduct } from "../api/api";

const REVIEWS_PER_PAGE = 5;

function HomePage() {
  const [reviews, setReviews] = useState([]);
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searchedProduct, setSearchedProduct] = useState("");
  const [searchHistory, setSearchHistory] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

const handleSearch = async (productName) => {
  setLoading(true);
  setError("");
  setReviews([]);
  setSentiment(null);
  setCurrentPage(1);
  setSearchedProduct(productName);

  setSearchHistory((prev) => {
    const filtered = prev.filter((item) => item !== productName);
    return [productName, ...filtered].slice(0, 5);
  });

  try {
    // Try to get existing data first
    const [reviewData, sentimentData] = await Promise.all([
      getReviews(productName),
      getSentiment(productName),
    ]);
    setReviews(reviewData.reviews);
    setSentiment(sentimentData);
    setLoading(false);

  } catch (err) {
    // Not in database — start scraping
    try {
      setError("Product not found. Scraping in background... please wait.");
      await scrapeProduct(productName);

      // Poll every 10 seconds until done
      const pollInterval = setInterval(async () => {
        try {
          const statusData = await checkScrapeStatus(productName);

          if (statusData.status === "done") {
            clearInterval(pollInterval);

            const [reviewData, sentimentData] = await Promise.all([
              getReviews(productName),
              getSentiment(productName),
            ]);

            setError("");
            setReviews(reviewData.reviews);
            setSentiment(sentimentData);
            setLoading(false);

          } else if (statusData.status === "error") {
            clearInterval(pollInterval);
            setError("Could not scrape this product. Please try again.");
            setLoading(false);
          } else {
            setError("Still scraping... please wait.");
          }
        } catch (pollErr) {
          clearInterval(pollInterval);
          setError("Something went wrong. Please try again.");
          setLoading(false);
        }
      }, 10000); // Check every 10 seconds

    } catch (scrapeErr) {
      setError("Could not start scraping. Please try again.");
      setLoading(false);
    }
  }
};

  // Pagination logic
    const totalPages = Math.ceil(reviews.length / REVIEWS_PER_PAGE);
    const startIndex = (currentPage - 1) * REVIEWS_PER_PAGE;
    const endIndex = startIndex + REVIEWS_PER_PAGE;
    const paginatedReviews = reviews.slice(startIndex, endIndex);

  return (
    <div style={styles.page}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.title}>🔍 Product Sentiment Analyzer</h1>
        <p style={styles.subtitle}>
          Search for a product to view its reviews and sentiment analysis
        </p>
      </div>

      {/* Search Bar */}
      <SearchBar onSearch={handleSearch} loading={loading} />

      {/* Search History */}
      <SearchHistory history={searchHistory} onSelect={handleSearch} />

      {/* Error or Status Message */}
      {error && (
        <p style={error.includes("Scraping") ? styles.info : styles.error}>
          {error}
        </p>
      )}

      {/* Loading Spinner */}
      {loading && <Spinner />}

      {/* Dashboard */}
      {!loading && sentiment && reviews.length > 0 && (
        <div style={styles.results}>
          <h2 style={styles.resultTitle}>
            Results for "{searchedProduct}"
          </h2>

          {/* Stats Cards */}
          <StatsCards reviews={reviews} sentimentData={sentiment} />

          {/* Charts Row */}
          <div style={styles.chartsRow}>
            <div style={styles.chartLeft}>
              <SentimentChart sentimentData={sentiment} />
            </div>
            <div style={styles.chartRight}>
              <SentimentBarChart sentimentData={sentiment} />
            </div>
          </div>

          {/* Reviews List */}
          <h3 style={styles.reviewsTitle}>
            Reviews ({reviews.length})
          </h3>

          {paginatedReviews.map((review) => (
            <ReviewCard key={review._id} review={review} />
          ))}

          {/* Pagination */}
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        </div>
      )}
    </div>
  );
}

const styles = {
  page: {
    maxWidth: "1000px",
    margin: "0 auto",
    padding: "40px 20px",
    fontFamily: "sans-serif",
    backgroundColor: "#1E201F",
    minHeight: "100vh",
  },
  header: {
    textAlign: "center",
    marginBottom: "32px",
  },
  title: {
    fontSize: "28px",
    color: "#3EB9A8",
    margin: "0 0 8px 0",
  },
  subtitle: {
    fontSize: "16px",
    color: "#5AA371",
    margin: 0,
  },
  error: {
    color: "#dc2626",
    textAlign: "center",
    fontSize: "14px",
    marginBottom: "16px",
  },
  info: {
    color: "#3EB9A8",
    textAlign: "center",
    fontSize: "14px",
    marginBottom: "16px",
    backgroundColor: "#193A31",
    padding: "12px",
    borderRadius: "8px",
  },
  results: {
    marginTop: "24px",
  },
  resultTitle: {
    fontSize: "20px",
    color: "white",
    marginBottom: "20px",
  },
  chartsRow: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "16px",
    marginBottom: "16px",
  },
  chartLeft: {
    minWidth: 0,
  },
  chartRight: {
    minWidth: 0,
  },
  reviewsTitle: {
    fontSize: "16px",
    color: "#3EB9A8",
    marginBottom: "12px",
    marginTop: "8px",
  },
};

export default HomePage;