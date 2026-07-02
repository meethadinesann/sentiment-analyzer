import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

const COLORS = {
  Positive: "#5AA371",
  Negative: "#dc2626",
  Neutral: "#3EB9A8",
};

function SentimentBarChart({ sentimentData }) {
  const chartData = Object.entries(sentimentData.counts).map(
    ([label, count]) => ({
      name: label,
      count: count,
      percentage: sentimentData.percentages[label],
    })
  );

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Sentiment Breakdown</h3>
      <p style={styles.subtitle}>Number of reviews per sentiment</p>

      <ResponsiveContainer width="100%" height={250}>
        <BarChart
          data={chartData}
          margin={{ top: 10, right: 20, left: 0, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#193A31" />
          <XAxis dataKey="name" stroke="#3EB9A8" />
          <YAxis allowDecimals={false} stroke="#3EB9A8" />
          <Tooltip
            contentStyle={{ backgroundColor: "#1E201F", border: "1px solid #3EB9A8" }}
            labelStyle={{ color: "#3EB9A8" }}
            formatter={(value, name, props) => [
              `${value} reviews (${props.payload.percentage}%)`,
              "Count",
            ]}
          />
          <Bar dataKey="count" radius={[6, 6, 0, 0]}>
            {chartData.map((entry) => (
              <Cell key={entry.name} fill={COLORS[entry.name] || "#8884d8"} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
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
};

export default SentimentBarChart;