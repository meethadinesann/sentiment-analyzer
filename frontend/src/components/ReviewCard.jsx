function ReviewCard({ review }) {
  const sentimentColors = {
    Positive: "#5AA371",
    Negative: "#dc2626",
    Neutral: "#3EB9A8",
  };

  const color = sentimentColors[review.sentiment_label] || "#666";

  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <span style={styles.rating}>⭐ {review.rating || "N/A"}</span>
        <span style={{ ...styles.badge, backgroundColor: color }}>
          {review.sentiment_label}
        </span>
      </div>
      <h4 style={styles.title}>{review.title}</h4>
      <p style={styles.body}>{review.body}</p>
      <p style={styles.score}>
        Sentiment Score: {review.sentiment_score?.toFixed(2)}
      </p>
    </div>
  );
}

const styles = {
  card: {
    backgroundColor: "#193A31",
    borderRadius: "10px",
    padding: "16px",
    marginBottom: "12px",
    boxShadow: "0 1px 4px rgba(0,0,0,0.2)",
    borderLeft: "4px solid #3EB9A8",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "8px",
  },
  rating: {
    fontSize: "14px",
    fontWeight: "bold",
    color: "#3EB9A8",
  },
  badge: {
    color: "white",
    padding: "4px 10px",
    borderRadius: "20px",
    fontSize: "12px",
    fontWeight: "bold",
  },
  title: {
    margin: "0 0 8px 0",
    fontSize: "15px",
    color: "white",
  },
  body: {
    margin: "0 0 8px 0",
    fontSize: "14px",
    color: "#3EB9A8",
    lineHeight: "1.5",
  },
  score: {
    margin: 0,
    fontSize: "12px",
    color: "#5AA371",
  },
};

export default ReviewCard;