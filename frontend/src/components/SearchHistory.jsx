function SearchHistory({ history, onSelect }) {
  if (history.length === 0) return null;

  return (
    <div style={styles.container}>
      <p style={styles.label}>Recent Searches:</p>
      <div style={styles.pills}>
        {history.map((item, index) => (
          <button
            key={index}
            onClick={() => onSelect(item)}
            style={styles.pill}
          >
            {item}
          </button>
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    marginBottom: "24px",
  },
  label: {
    color: "#5AA371",
    fontSize: "13px",
    marginBottom: "8px",
  },
  pills: {
    display: "flex",
    flexWrap: "wrap",
    gap: "8px",
    justifyContent: "center",
  },
  pill: {
    backgroundColor: "#193A31",
    color: "#3EB9A8",
    border: "1px solid #1D6C61",
    borderRadius: "20px",
    padding: "6px 14px",
    fontSize: "13px",
    cursor: "pointer",
  },
};

export default SearchHistory;