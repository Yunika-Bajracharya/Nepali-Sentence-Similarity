import React, { useState, useEffect } from "react";
import { ReactTransliterate } from "react-transliterate";

import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [faqList, setFaqList] = useState([]);
  const [darkMode, setDarkMode] = useState(true);

  const [lang, setLang] = useState("ne");

  const [transliteration, setTransliteration] = useState(false);

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

  // const toggleDarkMode = () => {
  //   setDarkMode(!darkMode);
  // };

  return (
    <div className={`container ${darkMode ? "dark-mode" : ""}`}>
      <div className="input-container">
        <h1>Welcome!</h1>

        <div>
          <button
            className={`input-section-button ${
              transliteration == false ? "blue" : ""
            }`}
            onClick={() => setTransliteration(false)}
          >
            Default
          </button>

          <button
            className={`input-section-button ${
              transliteration == true ? "blue" : ""
            }`}
            onClick={() => setTransliteration(true)}
          >
            Nepali Transliteration
          </button>
        </div>

        <div className="input-section">
          {transliteration == false && (
            <input
              type="text"
              placeholder="Search your query..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          )}

          {transliteration == true && (
            <ReactTransliterate
              // renderComponent={(props) => <input {...props} />}
              value={query}
              placeholder="Search in romanized Nepali..."
              onChangeText={(text) => {
                setQuery(text);
              }}
              lang={lang}
            />
          )}

          <button className="input-button" onClick={handleSearch}>
            Search
          </button>
        </div>
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
