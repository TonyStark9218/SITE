// Telegram bot webhook 
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