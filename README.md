# discord-poll-bot
Discord bot that posts a customizable daily poll to a text channel on your server using Discord's native polls feature.

## Features

* Daily Schedule: Posts a poll at a specific time every day (e.g., 4:00 PM) based on your local timezone.
* Native Polls: Uses Discord's built-in poll UI for a clean, modern look.
* Dynamic Answers: Fully customizable poll answers via container Environment Variables (add up to 10 options!).
* Timezone Aware: Respects your local time (via `TZ` variable) so "16:00" means *your* 4 PM.
* Docker Ready: Pre-built and optimized for easy deployment via Docker.

---

## Quick Start (Docker Compose)

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
      - POLL_QUESTION=your_poll_question_here # emojis allowed!

      # --- ANSWERS (Min 2, Max 10) ---
      # Note: Use standard emojis (🍕), NOT shortcodes (:pizza:)
      - ANSWER_1_TEXT=Yes
      - ANSWER_1_EMOJI=✅
      - ANSWER_2_TEXT=Maybe
      - ANSWER_2_EMOJI=🤔
      - ANSWER_3_TEXT=No
      - ANSWER_3_EMOJI=❌

## 