import { useState } from "react";

function SearchBar({ onSearch, loading }) {
  const [input, setInput] = useState("");

  const handleSubmit = () => {
    if (input.trim()) {
      onSearch(input.trim());
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSubmit();
    }
  };

  return (
    <div style={styles.container}>
      <input
        type="text"
        placeholder="Search for a product (e.g. boAt earphones)"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyPress}
        style={styles.input}
        disabled={loading}
      />
      <button
        onClick={handleSubmit}
        disabled={loading}
        style={styles.button}
      >
        {loading ? "Searching..." : "Search"}
      </button>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    gap: "10px",
    justifyContent: "center",
    marginBottom: "30px",
  },
  input: {
    width: "400px",
    padding: "12px 16px",
    fontSize: "16px",
    borderRadius: "8px",
    border: "1px solid #3EB9A8",
    outline: "none",
    backgroundColor: "#193A31",
    color: "white",
  },
  button: {
    padding: "12px 24px",
    fontSize: "16px",
    backgroundColor: "#1D6C61",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
};

export default SearchBar;