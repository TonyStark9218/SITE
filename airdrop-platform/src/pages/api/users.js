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