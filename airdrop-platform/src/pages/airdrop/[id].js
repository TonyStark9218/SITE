import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import Discussion from '../../components/Discussion';

export default function AirdropDetails() {
  const router = useRouter();
  const { id } = router.query;
  const [airdrop, setAirdrop] = useState(null);
  const [rating, setRating] = useState(0);
  const [userId, setUserId] = useState('');

  useEffect(() => {
    if (id) {
      axios.get(`/api/airdrops/${id}`).then((res) => setAirdrop(res.data));
    }
  }, [id]);

  const handleRate = async () => {
    if (!userId) return alert('Enter your Telegram ID');
    await axios.post(`/api/airdrops/${id}/rate`, { rating });
    axios.get(`/api/airdrops/${id}`).then((res) => setAirdrop(res.data));
  };

  const handleWatchlist = async () => {
    if (!userId) return alert('Enter your Telegram ID');
    await axios.post(`/api/users/${userId}/watchlist`, { airdropId: id });
  };

  const handleCompleteTask = async (taskIndex) => {
    if (!userId) return alert('Enter your Telegram ID');
    await axios.post(`/api/users/${userId}/complete-task`, { airdropId: id, taskIndex });
  };

  if (!airdrop) return <div>Loading...</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">{airdrop.name}</h1>
      <p>Status: {airdrop.status}</p>
      <p>Difficulty: {airdrop.difficulty}</p>
      <p>Rating: {airdrop.rating.toFixed(1)}/5 ({airdrop.ratingCount} votes)</p>
      <div>
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="Enter your Telegram ID"
          className="p-2 border rounded mr-2"
        />
        <select value={rating} onChange={(e) => setRating(Number(e.target.value))}>
          {[1, 2, 3, 4, 5].map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
        <button onClick={handleRate} className="p-2 bg-blue-500 text-white rounded">
          Rate
        </button>
        <button onClick={handleWatchlist} className="p-2 bg-green-500 text-white rounded">
          Add to Watchlist
        </button>
      </div>
      <h2 className="text-xl mt-4">Tasks</h2>
      <ul>
        {airdrop.tasks.map((task, i) => (
          <li key={i}>
            {task.text} <a href={task.link} className="text-blue-500">{task.link}</a>
            <button
              onClick={() => handleCompleteTask(i)}
              className="p-1 bg-gray-200 rounded"
            >
              Mark Done
            </button>
          </li>
        ))}
      </ul>
      <Discussion airdropId={id} comments={airdrop.comments} userId={userId} />
    </div>
  );
}