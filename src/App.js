// App.js

import React, { useState, useEffect } from 'react';
import './App.css';
import { format } from 'date-fns';

function App() {
  const [items, setItems] = useState([]);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    const fetchArticles = async () => {
      try {
        const res = await fetch(`https://hn.algolia.com/api/v1/search?query=${query}`);
        const data = await res.json();
        setItems(data.hits);
        setIsLoading(false); // Set loading to false when data is fetched
      } catch (error) {
        console.error('Error fetching data:', error);
        setIsLoading(false); // Set loading to false in case of an error
      }
    };

    fetchArticles();
    setCategory(query); // Update the category based on the current query
  }, [query]); // Add query as a dependency to the useEffect hook

  return (
    <section className="section">
      <form autoComplete="off" onSubmit={(e) => e.preventDefault()}>
        <input
          type="text"
          name="search"
          id="search"
          placeholder="Search for something"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" onClick={() => setQuery(query)}>
          Search
        </button>
      </form>
      {isLoading ? (
        <div className="spinner"></div>
      ) : (
        <div>
          {category && <h2>Category: {category}</h2>}
          <div className="cards">
            {items.map(({ author, created_at, title, url, objectID }) => (
              <div key={objectID}>
                <h2>{title}</h2>
                <ul>
                  <li> By {author}</li>
                  <li>
                    <a href={url} target="_blank" rel="noreferrer">
                      Read Full Article
                    </a>
                  </li>
                </ul>
                <p>{created_at}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}

export default App;
