import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [faqList, setFaqList] = useState([]);
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    // Fetch FAQ list from the backend on component mount
    fetchFaqList();
  }, []);

  const fetchFaqList = async () => {
    try {
      const response = await axios.get("http://localhost:8000/faq-data/");
      setFaqList(response.data);
    } catch (error) {
      console.error("Error fetching FAQ list:", error);
    }
  };

  const handleSearch = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/faq-search/?query=${encodeURIComponent(query)}`
      );
      setResult(response.data);
    } catch (error) {
      console.error("Error searching FAQ:", error);
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`container ${darkMode ? "dark-mode" : ""}`}>
      <div className="input-container">
        <h1>Welcome!</h1>

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search your query..."
        />
        <button className="input-button" onClick={handleSearch}>
          Search
        </button>
      </div>
      {result && (
        <div className="faq-item">
          <h7>
            <i>Most Similar Question from FAQ list:</i>
          </h7>
          <h3 className="color-text">{result.question}</h3>
          <h4 className="color-text">{result.answer}</h4>
          <p>Similarity Score: {result.score}</p>
        </div>
      )}
      <div className="faq-list">
        <h2>Frequently Asked Questions</h2>
        {faqList.map((faq, index) => (
          <div key={index} className="faq-item">
            <p className="faq-question">● {faq.question}</p>
            <p className="faq-answer">➔ {faq.answer}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
