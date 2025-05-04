import { motion } from 'framer-motion';
import Link from 'next/link';

export default function AirdropCard({ airdrop }) {
  return (
    <motion.div
      className="airdrop-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.05 }}
    >
      <h3 className="text-lg font-bold">{airdrop.name}</h3>
      <p className="text-sm text-gray-600 dark:text-gray-400">
        Deadline: {airdrop.deadline ? new Date(airdrop.deadline).toLocaleDateString() : 'None'}
      </p>
      <p className="text-sm">
        Status: <span className={airdrop.status === 'Ongoing' ? 'text-green-500' : 'text-red-500'}>
          {airdrop.status}
        </span>
      </p>
      <p>Difficulty: {airdrop.difficulty}</p>
      <p>Rating: {airdrop.rating.toFixed(1)}/5 ({airdrop.ratingCount} votes)</p>
      <div className="flex flex-wrap gap-2 mt-2">
        {airdrop.tags.map((tag) => (
          <span key={tag} className="tag-chip">{tag}</span>
        ))}
      </div>
      <Link href={`/airdrop/${airdrop.id}`}>
        <a className="mt-2 inline-block text-blue-500">View Details</a>
      </Link>
    </motion.div>
  );
}