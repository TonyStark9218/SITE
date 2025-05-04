import { useEffect, useState } from 'react';
import axios from 'axios';
import AirdropForm from '../components/AirdropForm';

export default function Admin() {
  const [airdrops, setAirdrops] = useState([]);
  const [pending, setPending] = useState([]);
  const [ownerId, setOwnerId] = useState('');

  useEffect(() => {
    axios.get('/api/airdrops').then((res) => setAirdrops(res.data));
    axios.get('/api/airdrops', { params: { approved: false } }).then((res) => setPending(res.data));
  }, []);

  const handleApprove = async (id) => {
    await axios.put(`/api/airdrops/${id}`, { approved: true });
    setPending(pending.filter((a) => a.id !== id));
  };

  if (!ownerId || ownerId !== process.env.OWNER_ID) {
    return (
      <div className="p-4">
        <input
          type="text"
          value={ownerId}
          onChange={(e) => setOwnerId(e.target.value)}
          placeholder="Enter Telegram Owner ID"
          className="p-2 border rounded"
        />
      </div>
    );
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Admin Dashboard</h1>
      <AirdropForm isAdmin onSubmit={() => axios.get('/api/airdrops').then((res) => setAirdrops(res.data))} />
      <h2 className="text-xl mt-4">Pending Airdrops</h2>
      {pending.map((airdrop) => (
        <div key={airdrop.id} className="p-2 border-b">
          <p>{airdrop.name} {airdrop.userSubmitted && '(User Submitted)'}</p>
          <button
            onClick={() => handleApprove(airdrop.id)}
            className="p-2 bg-green-500 text-white rounded"
          >
            Approve
          </button>
        </div>
      ))}
    </div>
  );
}