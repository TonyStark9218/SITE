import os
import json

# Define project directory
project_dir = "airdrop-platform"

# Define project structure and file contents
project_structure = {
    "public": {
        "favicon.ico": ""  # Placeholder; replace with actual favicon if needed
    },
    "src": {
        "components": {
            "AirdropCard.js": """
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
""",
            "AirdropForm.js": """
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
""",
            "SearchFilter.js": """
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
""",
            "Discussion.js": """
import { useState } from 'react';
import axios from 'axios';

export default function Discussion({ airdropId, comments, userId }) {
  const [text, setText] = useState('');
  const [inputUserId, setInputUserId] = useState(userId || '');

  const handleComment = async () => {
    if (!text || !inputUserId) return;
    await axios.post(`/api/airdrops/${airdropId}/comment`, { userId: inputUserId, text });
    setText('');
  };

  return (
    <div className="mt-4">
      <h4 className="text-lg font-semibold">Discussion</h4>
      <div className="space-y-2">
        {comments.map((comment, i) => (
          <div key={i} className="p-2 border-b">
            <p>{comment.text}</p>
            <p className="text-sm text-gray-500">Posted on {new Date(comment.createdAt).toLocaleDateString()}</p>
          </div>
        ))}
      </div>
      <div className="mt-2">
        {!userId && (
          <input
            type="text"
            value={inputUserId}
            onChange={(e) => setInputUserId(e.target.value)}
            placeholder="Enter your Telegram ID"
            className="w-full p-2 border rounded mb-2"
          />
        )}
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Add a comment..."
          className="w-full p-2 border rounded"
        />
        <button onClick={handleComment} className="mt-2 p-2 bg-blue-500 text-white rounded">
          Post Comment
        </button>
      </div>
    </div>
  );
}
"""
        },
        "pages": {
            "api": {
                "airdrops.js": """
import fs from 'fs/promises';
import path from 'path';

const storagePath = path.join(process.cwd(), 'src', 'data', 'storage.json');

async function getStorage() {
  try {
    const data = await fs.readFile(storagePath, 'utf8');
    return JSON.parse(data);
  } catch {
    return { airdrops: [], users: {} };
  }
}

async function saveStorage(data) {
  await fs.writeFile(storagePath, JSON.stringify(data, null, 2));
}

export default async function handler(req, res) {
  const { method, query, body } = req;

  if (method === 'GET') {
    const { status, tags, search, approved } = query;
    const storage = await getStorage();
    let airdrops = storage.airdrops;
    if (approved === 'false') airdrops = airdrops.filter((a) => !a.approved);
    else airdrops = airdrops.filter((a) => a.approved);
    if (status) airdrops = airdrops.filter((a) => a.status === status);
    if (tags) airdrops = airdrops.filter((a) => tags.split(',').some((t) => a.tags.includes(t)));
    if (search) airdrops = airdrops.filter((a) => a.name.toLowerCase().includes(search.toLowerCase()));
    airdrops.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    res.json(airdrops);
  }

  if (method === 'POST') {
    const { name, links } = body;
    const storage = await getStorage();
    const existing = storage.airdrops.find((a) => a.name.toLowerCase() === name.toLowerCase() || a.links.some((l) => links.includes(l)));
    if (existing) return res.status(400).json({ error: 'Possible duplicate airdrop' });
    const id = Math.random().toString(36).slice(2);
    const airdrop = { id, ...body, createdAt: new Date(), rating: 0, ratingCount: 0, comments: [], approved: !body.userSubmitted };
    storage.airdrops.push(airdrop);
    await saveStorage(storage);
    if (body.userSubmitted) {
      const bot = require('node-telegram-bot-api')(process.env.TELEGRAM_TOKEN);
      bot.sendMessage(process.env.OWNER_ID, `New airdrop submitted: ${name}`);
    }
    res.json(airdrop);
  }

  if (method === 'PUT') {
    const { id } = query;
    const storage = await getStorage();
    const index = storage.airdrops.findIndex((a) => a.id === id);
    if (index === -1) return res.status(404).json({ error: 'Airdrop not found' });
    storage.airdrops[index] = { ...storage.airdrops[index], ...body };
    await saveStorage(storage);
    res.json(storage.airdrops[index]);
  }

  if (method === 'POST' && query.id && query.action === 'rate') {
    const { rating } = body;
    const storage = await getStorage();
    const airdrop = storage.airdrops.find((a) => a.id === query.id);
    if (!airdrop) return res.status(404).json({ error: 'Airdrop not found' });
    const newCount = airdrop.ratingCount + 1;
    airdrop.rating = (airdrop.rating * airdrop.ratingCount + rating) / newCount;
    airdrop.ratingCount = newCount;
    await saveStorage(storage);
    res.json(airdrop);
  }

  if (method === 'POST' && query.id && query.action === 'comment') {
    const { userId, text } = body;
    const storage = await getStorage();
    const airdrop = storage.airdrops.find((a) => a.id === query.id);
    if (!airdrop) return res.status(404).json({ error: 'Airdrop not found' });
    airdrop.comments.push({ userId, text, createdAt: new Date() });
    await saveStorage(storage);
    res.json(airdrop);
  }
}
""",
                "users.js": """
import fs from 'fs/promises';
import path from 'path';

const storagePath = path.join(process.cwd(), 'src', 'data', 'storage.json');

async function getStorage() {
  try {
    const data = await fs.readFile(storagePath, 'utf8');
    return JSON.parse(data);
  } catch {
    return { airdrops: [], users: {} };
  }
}

async function saveStorage(data) {
  await fs.writeFile(storagePath, JSON.stringify(data, null, 2));
}

export default async function handler(req, res) {
  const { method, query, body } = req;
  const { userId } = query;

  if (method === 'GET') {
    const storage = await getStorage();
    const user = storage.users[userId] || { watchlist: [], completedTasks: [], badges: [], telegramId: userId };
    const airdrops = storage.airdrops;
    user.watchlist = user.watchlist.map((id) => airdrops.find((a) => a.id === id)).filter(Boolean);
    res.json(user);
  }

  if (method === 'POST' && query.action === 'watchlist') {
    const { airdropId } = body;
    const storage = await getStorage();
    let user = storage.users[userId] || { watchlist: [], completedTasks: [], badges: [], telegramId: userId };
    if (!user.watchlist.includes(airdropId)) user.watchlist.push(airdropId);
    storage.users[userId] = user;
    await saveStorage(storage);
    res.json(user);
  }

  if (method === 'POST' && query.action === 'complete-task') {
    const { airdropId, taskIndex } = body;
    const storage = await getStorage();
    let user = storage.users[userId] || { watchlist: [], completedTasks: [], badges: [], telegramId: userId };
    if (!user.completedTasks.some((t) => t.airdropId === airdropId && t.taskIndex === taskIndex)) {
      user.completedTasks.push({ airdropId, taskIndex });
      const taskCount = user.completedTasks.length;
      if (taskCount === 1) user.badges.push('Airdrop Rookie');
      if (taskCount === 5) user.badges.push('Airdrop Pro');
    }
    storage.users[userId] = user;
    await saveStorage(storage);
    res.json(user);
  }

  if (method === 'POST' && query.action === 'telegram') {
    const { telegramId } = body;
    const storage = await getStorage();
    let user = storage.users[userId] || { watchlist: [], completedTasks: [], badges: [], telegramId };
    user.telegramId = telegramId;
    storage.users[userId] = user;
    await saveStorage(storage);
    res.json(user);
  }
}
""",
                "telegram.js": """
import TelegramBot from 'node-telegram-bot-api';
import fs from 'fs/promises';
import path from 'path';

const storagePath = path.join(process.cwd(), 'src', 'data', 'storage.json');

async function getStorage() {
  try {
    const data = await fs.readFile(storagePath, 'utf8');
    return JSON.parse(data);
  } catch {
    return { airdrops: [], users: {} };
  }
}

async function saveStorage(data) {
  await fs.writeFile(storagePath, JSON.stringify(data, null, 2));
}

const bot = new TelegramBot(process.env.TELEGRAM_TOKEN);

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const update = req.body;
    if (update.message) {
      const { chat, text } = update.message;
      if (text === '/start') {
        bot.sendMessage(chat.id, 'Welcome! Your Telegram ID is linked for airdrop tracking.');
      }
      if (text.startsWith('/link')) {
        const userId = text.split(' ')[1] || chat.id.toString();
        const storage = await getStorage();
        storage.users[userId] = { ...(storage.users[userId] || {}), telegramId: chat.id.toString() };
        await saveStorage(storage);
        bot.sendMessage(chat.id, 'Account linked! You’ll get deadline notifications.');
      }
    }
    res.status(200).send('OK');
  }

  if (req.method === 'GET') {
    const storage = await getStorage();
    const now = new Date();
    const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
    const airdrops = storage.airdrops.filter(
      (a) => a.deadline && new Date(a.deadline) >= now && new Date(a.deadline) <= tomorrow && a.approved
    );

    for (const airdrop of airdrops) {
      for (const userId in storage.users) {
        const user = storage.users[userId];
        if (user.watchlist.includes(airdrop.id) && user.telegramId) {
          bot.sendMessage(
            user.telegramId,
            `⏰ Airdrop "${airdrop.name}" deadline is tomorrow! Complete tasks: ${airdrop.links[0]}`
          );
        }
      }
    }
    res.status(200).send('Notifications sent');
  }
}
"""
            },
            "_app.js": """
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
""",
            "index.js": """
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
""",
            "airdrops.js": """
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
""",
            "admin.js": """
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
""",
            "airdrop": {
                "[id].js": """
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
"""
            }
        },
        "styles": {
            "globals.css": """
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --bg-light: #ffffff;
  --bg-dark: #1a202c;
  --text-light: #1a202c;
  --text-dark: #e2e8f0;
}

body {
  @apply bg-[var(--bg-light)] text-[var(--text-light)] dark:bg-[var(--bg-dark)] dark:text-[var(--text-dark)];
}

.airdrop-card {
  @apply p-4 rounded-lg shadow-md hover:shadow-lg transition-shadow bg-white dark:bg-gray-800;
}

.tag-chip {
  @apply px-2 py-1 rounded-full text-sm bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200;
}
"""
        },
        "data": {
            "storage.json": json.dumps({"airdrops": [], "users": {}}, indent=2)
        }
    },
    "package.json": json.dumps({
        "name": "airdrop-platform",
        "version": "1.0.0",
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start"
        },
        "dependencies": {
            "axios": "^1.4.0",
            "framer-motion": "^10.12.16",
            "next": "^13.4.0",
            "node-telegram-bot-api": "^0.61.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "tailwindcss": "^3.3.2"
        }
    }, indent=2),
    "vercel.json": json.dumps({
        "rewrites": [
            {"source": "/api/:path*", "destination": "/api/:path*"}
        ],
        "functions": {
            "src/pages/api/airdrops.js": {"memory": 128},
            "src/pages/api/users.js": {"memory": 128},
            "src/pages/api/telegram.js": {"memory": 128}
        }
    }, indent=2),
    ".env.example": """
TELEGRAM_TOKEN=your_telegram_bot_token
OWNER_ID=your_telegram_owner_id
""",
    "README.md": """
# Airdrop Platform

A minimal airdrop tracking platform deployed on Vercel, requiring only a Telegram bot token and owner ID.

## Setup

1. **Create a GitHub Repository**:
   - Create a new repository (e.g., `airdrop-platform`) on [github.com](https://github.com).
   - Copy all files from this project into the repository.
   - Commit and push to GitHub.

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com), sign in, and click "New Project".
   - Import your GitHub repository.
   - Add environment variables in Vercel’s "Settings" > "Environment Variables":
     - `TELEGRAM_TOKEN`: Get from [@BotFather](https://t.me/BotFather).
     - `OWNER_ID`: Get from [@userinfobot](https://t.me/userinfobot).
   - Click "Deploy".

3. **Set Up Telegram Bot**:
   - Set the webhook: `https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=<your-vercel-domain>/api/telegram`.

4. **Test**:
   - Visit your Vercel domain (e.g., `your-project.vercel.app`).
   - Browse airdrops, submit airdrops, or access `/admin` with your Telegram owner ID.
   - Send `/start` or `/link <your-telegram-id>` to the bot for personalization.

## Features
- Animated airdrop cards (Framer Motion).
- Search, filter, and sort airdrops.
- Admin controls (add/approve airdrops via Telegram owner ID).
- User features (submit airdrops, watchlist, badges).
- Telegram notifications for deadlines and submissions.
- Discussion forum per airdrop.
- Light/dark mode, responsive design.

## Note
- Data resets on Vercel redeploys (uses local JSON storage).
"""
}

# Function to create directories and files
def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, content)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content.strip())

# Create project
if os.path.exists(project_dir):
    print(f"Directory '{project_dir}' already exists. Please delete it or choose another name.")
else:
    os.makedirs(project_dir)
    create_project_structure(project_dir, project_structure)
    print(f"Project created successfully in '{project_dir}'!")

    # Print deployment instructions
    print("\nNext Steps:")
    print("1. Navigate to the project directory:")
    print(f"   cd {project_dir}")
    print("2. Initialize a Git repository:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("3. Create a new repository on GitHub (e.g., 'airdrop-platform') and push:")
    print("   git remote add origin <your-repo-url>")
    print("   git push -u origin main")
    print("4. Deploy to Vercel:")
    print("   - Go to https://vercel.com, sign in, and click 'New Project'.")
    print("   - Import your GitHub repository.")
    print("   - Add environment variables in Vercel’s 'Settings' > 'Environment Variables':")
    print("     - TELEGRAM_TOKEN: Get from @BotFather (https://t.me/BotFather)")
    print("     - OWNER_ID: Get from @userinfobot (https://t.me/userinfobot)")
    print("   - Click 'Deploy'.")
    print("5. Set up Telegram bot webhook:")
    print("   - After deployment, get your Vercel domain (e.g., your-project.vercel.app).")
    print("   - Visit: https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=<your-vercel-domain>/api/telegram")
    print("6. Test the platform:")
    print("   - Visit your Vercel domain.")
    print("   - Access /admin with your Telegram owner ID.")
    print("   - Send /start or /link <your-telegram-id> to the bot for personalization.")