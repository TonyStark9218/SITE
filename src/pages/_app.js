import '../styles/globals.css';
import { useState } from 'react';

export default function App({ Component, pageProps }) {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <div className={darkMode ? 'dark' : ''}>
      <button
        className="fixed top-4 right-4 p-2 bg-gray-200 dark:bg-gray-700 rounded"
        onClick={() => setDarkMode(!darkMode)}
      >
        {darkMode ? 'Light' : 'Dark'}
      </button>
      <Component {...pageProps} />
    </div>
  );
}