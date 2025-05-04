// Home page 
import { useEffect, useState } from 'react';
import axios from 'axios';
import AirdropCard from '../components/AirdropCard';
import SearchFilter from '../components/SearchFilter';

export default function Home() {
  const [airdrops, setAirdrops] = useState([]);
  const [filters, setFilters] = useState({});

  useEffect(() => {
    axios.get('/api/airdrops', { params: { status: 'Ongoing', ...filters } })
      .then((res) => setAirdrops(res.data));
  }, [filters]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Airdrop Platform</h1>
      <SearchFilter onFilter={setFilters} />
      <div className="mt-4">
        <h2 className="text-xl font-semibold">Featured Airdrops</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2">
          {airdrops.slice(0, 3).map((airdrop) => (
            <AirdropCard key={airdrop.id} airdrop={airdrop} />
          ))}
        </div>
      </div>
    </div>
  );
}