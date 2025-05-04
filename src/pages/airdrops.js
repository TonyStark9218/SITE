// All airdrops page 
import { useEffect, useState } from 'react';
import axios from 'axios';
import AirdropCard from '../components/AirdropCard';
import SearchFilter from '../components/SearchFilter';

export default function Airdrops() {
  const [airdrops, setAirdrops] = useState([]);
  const [filters, setFilters] = useState({});

  useEffect(() => {
    axios.get('/api/airdrops', { params: filters })
      .then((res) => setAirdrops(res.data));
  }, [filters]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">All Airdrops</h1>
      <SearchFilter onFilter={setFilters} />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        {airdrops.map((airdrop) => (
          <AirdropCard key={airdrop.id} airdrop={airdrop} />
        ))}
      </div>
    </div>
  );
}