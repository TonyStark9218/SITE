import { useState } from 'react';
import axios from 'axios';

export default function AirdropForm({ airdrop, onSubmit, isAdmin }) {
  const [form, setForm] = useState(airdrop || {
    name: '', links: [''], deadline: '', status: 'Ongoing', tasks: [{ text: '', link: '' }],
    funding: '', source: '', tags: [], priority: 'Medium', difficulty: 'Moderate', userSubmitted: !isAdmin,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/api/airdrops', form);
      onSubmit(res.data);
    } catch (err) {
      alert(err.response?.data?.error || 'Error submitting airdrop');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
        placeholder="Airdrop Name"
        className="w-full p-2 border rounded"
        required
      />
      <input
        type="text"
        value={form.links[0]}
        onChange={(e) => setForm({ ...form, links: [e.target.value] })}
        placeholder="Link"
        className="w-full p-2 border rounded"
        required
      />
      <input
        type="date"
        value={form.deadline ? new Date(form.deadline).toISOString().split('T')[0] : ''}
        onChange={(e) => setForm({ ...form, deadline: e.target.value })}
        className="w-full p-2 border rounded"
      />
      <select
        value={form.difficulty}
        onChange={(e) => setForm({ ...form, difficulty: e.target.value })}
        className="w-full p-2 border rounded"
      >
        <option value="High">High</option>
        <option value="Moderate">Moderate</option>
        <option value="Low">Low</option>
      </select>
      <input
        type="text"
        value={form.tasks[0].text}
        onChange={(e) => setForm({ ...form, tasks: [{ text: e.target.value, link: form.tasks[0].link }] })}
        placeholder="Task"
        className="w-full p-2 border rounded"
      />
      <input
        type="text"
        value={form.source}
        onChange={(e) => setForm({ ...form, source: e.target.value })}
        placeholder="Source"
        className="w-full p-2 border rounded"
        required
      />
      <button type="submit" className="p-2 bg-blue-500 text-white rounded">
        {isAdmin ? 'Submit' : 'Submit for Review'}
      </button>
    </form>
  );
}