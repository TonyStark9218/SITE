import { useState } from 'react';

export default function SearchFilter({ onFilter }) {
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [tags, setTags] = useState('');

  const handleFilter = () => {
    onFilter({ search, status, tags });
  };

  return (
    <div className="flex gap-4 p-4 bg-gray-100 dark:bg-gray-700 rounded">
      <input
        type="text"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search airdrops..."
        className="p-2 border rounded"
      />
      <select value={status} onChange={(e) => setStatus(e.target.value)} className="p-2 border rounded">
        <option value="">All Status</option>
        <option value="Ongoing">Ongoing</option>
        <option value="Over">Over</option>
      </select>
      <input
        type="text"
        value={tags}
        onChange={(e) => setTags(e.target.value)}
        placeholder="Tags (comma-separated)"
        className="p-2 border rounded"
      />
      <button onClick={handleFilter} className="p-2 bg-blue-500 text-white rounded">Filter</button>
    </div>
  );
}