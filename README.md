# Discord Poll Bot: Automated polls for your server

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)
![Discord](https://img.shields.io/badge/Discord-Native%20Polls-5865F2?style=flat-square&logo=discord)

A lightweight, Dockerized Discord bot that automatically posts a customizable daily poll using **Discord's native Polls feature**. 

---

## ✨ Features

* **📅 Daily Schedule:** Posts a poll at a specific time every day based on your local timezone.
* **📊 Native Polls:** Uses Discord's built-in poll UI for a clean, modern look.
* **🎨 Dynamic Answers:** Fully customizable poll answers via Environment Variables (add up to 10 options!).
* **🌍 Timezone Aware:** Respects your local time (via `TZ` variable) so "16:00" means *your* 4 PM.
* **🐳 Docker Ready:** Pre-built and optimized for easy deployment via Docker Compose.

---

## 🚀 Quick Start (Docker Compose)

Create a `docker-compose.yml` file and paste the configuration below.

```yaml
version: '3.8'

services:
  discord-poll-bot:
    image: wltrhndrsn/discord-poll-bot:latest
    container_name: discord-poll-bot
    restart: unless-stopped
    environment:
      # --- REQUIRED SETTINGS ---
      - DISCORD_TOKEN=your_bot_token_here
      - CHANNEL_ID=123456789012345678
      - TZ=America/Chicago  # Set your local timezone (e.g. Europe/London)
      - TARGET_TIME=16:00   # 24-Hour format (e.g. 16:00 is 4 PM)

      # --- POLL CONFIGURATION ---
      - POLL_QUESTION=your_poll_question_here # emojis allowed

      # --- ANSWERS (Min 2, Max 10) ---
      # Note: Use standard emojis (🍕), NOT shortcodes (:pizza:)
      - ANSWER_1_TEXT=Yes
      - ANSWER_1_EMOJI=✅
      - ANSWER_2_TEXT=Maybe
      - ANSWER_2_EMOJI=🤔
      - ANSWER_3_TEXT=No
      - ANSWER_3_EMOJI=❌ # Add up to 10 answers
````
## 🔑 How to Get your Discord Keys
To use this bot, you first need to create an app in the Discord Developer Portal:
1. **Create App:** Go to the [Discord Developer Portal](https://discord.com/developers/) and create a new application.
2. **Get Token:** Go to **Bot -> Reset Token** to get your `DISCORD_TOKEN`.
3. **Enable Intents:** Scroll down to **Privileged Gateway Intents** and enable **Message Content Intent**.
4. **Invite Bot to your server:** Go to **OAuth2 -> URL Generator.**
   - **Scopes:** Check `bot`.
   - **Permissions:** Check `Send Messages`, `View Channels`, `Send Polls`.
   - Copy and paste the URL into a web browser to add the bot to your server.
5. **Add the bot to the channel:** In Discord, navigate to your channel and make sure the bot user is added.
6. **Get Channel ID:** In Discord, turn on **Developer Mode** (Settings -> Advanced), then right-click your desired channel, and click **Copy Channel ID.**

## Miscellaneous
This project is currently only compiled for amd64/linux.

## Known Issues
Discord is very strict about emoji in Polls. Emoji used in this program must be **Unicode** emoji characters. Sometimes, specific OS emoji have variant selectors or hidden bytes that the poll API doesn't like. If you run into issues, try removing or replacing obscure emoji with a more standard character.

## License
This project is open-source under the MIT License.
