function StatsCards({ reviews, sentimentData }) {
  // Parse rating as float to avoid NaN
  const ratingsWithValues = reviews.filter((r) => parseFloat(r.rating) > 0);
  const avgRating =
    ratingsWithValues.length > 0
      ? (
          ratingsWithValues.reduce((sum, r) => sum + parseFloat(r.rating), 0) /
          ratingsWithValues.length
        ).toFixed(1)
      : "N/A";

  const counts = sentimentData.counts;
  const dominant = Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];

  const dominantColors = {
    Positive: "#5AA371",
    Negative: "#dc2626",
    Neutral: "#3EB9A8",
  };

  const stats = [
    {
      label: "Total Reviews",
      value: sentimentData.total,
      icon: "📝",
      color: "#1D6C61",
    },
    {
      label: "Average Rating",
      value: `${avgRating} / 5`,
      icon: "⭐",
      color: "#3EB9A8",
    },
    {
      label: "Positive Reviews",
      value: `${sentimentData.percentages.Positive}%`,
      icon: "😊",
      color: "#5AA371",
    },
    {
      label: "Dominant Sentiment",
      value: dominant,
      icon: "📊",
      color: dominantColors[dominant],
    },
  ];

  return (
    <div style={styles.grid}>
      {stats.map((stat) => (
        <div key={stat.label} style={styles.card}>
          <span style={styles.icon}>{stat.icon}</span>
          <p style={styles.label}>{stat.label}</p>
          <p style={{ ...styles.value, color: stat.color }}>{stat.value}</p>
        </div>
      ))}
    </div>
  );
}

const styles = {
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "16px",
    marginBottom: "24px",
  },
  card: {
    backgroundColor: "#193A31",
    borderRadius: "12px",
    padding: "20px",
    textAlign: "center",
    boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
  },
  icon: {
    fontSize: "28px",
  },
  label: {
    fontSize: "13px",
    color: "#3EB9A8",
    margin: "8px 0 4px 0",
  },
  value: {
    fontSize: "22px",
    fontWeight: "bold",
    margin: 0,
  },
};

export default StatsCards;