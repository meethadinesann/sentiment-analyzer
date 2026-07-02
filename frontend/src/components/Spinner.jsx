function Spinner() {
  return (
    <div style={styles.container}>
      <div style={styles.spinner}></div>
      <p style={styles.text}>Analyzing reviews...</p>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "40px",
  },
  spinner: {
    width: "48px",
    height: "48px",
    border: "5px solid #193A31",
    borderTop: "5px solid #3EB9A8",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
  },
  text: {
    marginTop: "16px",
    color: "#3EB9A8",
    fontSize: "16px",
  },
};

export default Spinner;