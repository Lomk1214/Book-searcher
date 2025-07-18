import { useState } from 'react';
import './App.css';

function App() {
  const [search, setSearch] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch('http://localhost:3001/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ book_name: search })
      });

      const data = await res.json();

      if (res.ok) {
        setResults(data);
      } else {
        setError(data.error || 'Something went wrong');
        setResults([]);
      }
    } catch (err) {
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Book Search</h1>
      </header>

      <form className="search-form" onSubmit={handleSearch}>
        <input
          type="text"
          className="search-input"
          placeholder="Search for a book..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button className="search-button" type="submit">Search</button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div className="book-grid">
        {results.map((book, index) => (
          <a key={index} className="book-card" href={book.link} target="_blank" rel="noreferrer">
            <img className="book-cover" src={book.image} alt={book.title} />
            <h3>{book.title}</h3>
          </a>
        ))}
      </div>
    </div>
  );
}

export default App;

