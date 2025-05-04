# Airdrop Platform

A minimal airdrop tracking platform deployed on Vercel, requiring only a Telegram bot token and owner ID.

## Setup

1. **Create a GitHub Repository**:
   - Create a new repository (e.g., `airdrop-platform`).
   - Copy all files from this codebase into the repository.
   - Commit and push to GitHub.

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com), sign in, and click "New Project".
   - Import your GitHub repository.
   - Add environment variables in Vercel’s "Settings" > "Environment Variables":
     - `TELEGRAM_TOKEN`: Get from [@BotFather](https://t.me/BotFather).
     - `OWNER_ID`: Get from [@userinfobot](https://t.me/userinfobot).
   - Click "Deploy".

3. **Set Up Telegram Bot**:
   - After deployment, set the webhook: `https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=<your-vercel-domain>/api/telegram`.

4. **Test**:
   - Visit your Vercel domain (e.g., `your-project.vercel.app`).
   - Use Telegram `/start` to link your user ID for personalization.
   - Admin features are accessible via the owner ID at `/admin`.

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