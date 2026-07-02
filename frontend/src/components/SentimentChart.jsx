import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = {
  Positive: "#5AA371",
  Negative: "#dc2626",
  Neutral: "#3EB9A8",
};

function SentimentChart({ sentimentData }) {
  const chartData = Object.entries(sentimentData.counts).map(
    ([label, count]) => ({
      name: label,
      value: count,
    })
  );

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Sentiment Distribution</h3>
      <p style={styles.subtitle}>Based on {sentimentData.total} reviews</p>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            outerRadius={100}
            dataKey="value"
            label={({ name, percent }) =>
              `${name} ${(percent * 100).toFixed(1)}%`
            }
          >
            {chartData.map((entry) => (
              <Cell key={entry.name} fill={COLORS[entry.name] || "#8884d8"} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>

      <div style={styles.summary}>
        {Object.entries(sentimentData.percentages).map(([label, pct]) => (
          <div key={label} style={styles.summaryItem}>
            <span style={{ ...styles.dot, backgroundColor: COLORS[label] }} />
            <span style={styles.label}>{label}</span>
            <span style={styles.percent}>{pct}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: "#1E201F",
    borderRadius: "12px",
    padding: "24px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
    marginBottom: "24px",
  },
  title: {
    margin: "0 0 4px 0",
    fontSize: "18px",
    color: "#3EB9A8",
  },
  subtitle: {
    margin: "0 0 16px 0",
    fontSize: "14px",
    color: "#5AA371",
  },
  summary: {
    display: "flex",
    justifyContent: "center",
    gap: "24px",
    marginTop: "16px",
  },
  summaryItem: {
    display: "flex",
    alignItems: "center",
    gap: "6px",
  },
  dot: {
    width: "12px",
    height: "12px",
    borderRadius: "50%",
    display: "inline-block",
  },
  label: {
    fontSize: "14px",
    color: "#3EB9A8",
  },
  percent: {
    fontSize: "14px",
    fontWeight: "bold",
    color: "white",
  },
};

export default SentimentChart;