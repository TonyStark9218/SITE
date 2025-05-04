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