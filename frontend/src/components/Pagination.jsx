function Pagination({ currentPage, totalPages, onPageChange }) {
  if (totalPages <= 1) return null;

  return (
    <div style={styles.container}>
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        style={{
          ...styles.button,
          opacity: currentPage === 1 ? 0.4 : 1,
        }}
      >
        ← Prev
      </button>

      <span style={styles.info}>
        Page {currentPage} of {totalPages}
      </span>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        style={{
          ...styles.button,
          opacity: currentPage === totalPages ? 0.4 : 1,
        }}
      >
        Next →
      </button>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    gap: "16px",
    marginTop: "20px",
    marginBottom: "20px",
  },
  button: {
    backgroundColor: "#193A31",
    color: "#3EB9A8",
    border: "1px solid #1D6C61",
    borderRadius: "8px",
    padding: "8px 16px",
    fontSize: "14px",
    cursor: "pointer",
  },
  info: {
    color: "#3EB9A8",
    fontSize: "14px",
  },
};

export default Pagination;