import discord
import os
import datetime # Needed for poll duration
from discord.ext import tasks, commands
from datetime import time
from zoneinfo import ZoneInfo  # Built-in to Python 3.9+

# --- CONFIGURATION ---
# These are loaded from the Docker environment variables
# Discord bot token
token = os.getenv('DISCORD_TOKEN')
# Default to 0 if not set, to prevent crash on int() conversion
channel_id = int(os.getenv('CHANNEL_ID', '0'))
# Default to America/Chicago if missing
timezone_str = os.getenv('TZ', 'America/Chicago') 
# Define when the bot should post the poll & get time from ENV (Default to 16:00/4 PM if missing)
target_time_str = os.getenv('TARGET_TIME', '16:00')
# Define the poll question from ENV
poll_question = os.getenv('POLL_QUESTION', "Error: please enter a question in container ENV")

try:
    target_hour, target_minute = map(int, target_time_str.split(':'))
# Defaults to 16:00/4 PM if errors
except ValueError:
    target_hour, target_minute = 16, 0

# --- SETUP ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- THE TASK ---
# We set the time with explicit timezone info
schedule_time = time(hour=target_hour, minute=target_minute, tzinfo=ZoneInfo(timezone_str))

@tasks.loop(time=schedule_time)
async def daily_poll():
    # Ensure the bot waits until it is fully ready before running the first loop
    await bot.wait_until_ready()
    
    channel = bot.get_channel(channel_id)
    
    if channel:
        # Create the Native Poll
        poll = discord.Poll(
            question=discord.PollMedia(text=poll_question, emoji=None),
            duration=datetime.timedelta(hours=8), # Poll automatically closes after 8 hours
            multiple=False, # People can only pick one option
        )
        
        # Up to 10 answers from ENV; ignores if ENV blank
        for i in range(1, 11):
            # Look for ANSWER_1_TEXT, ANSWER_1_EMOJI, up to 'ANSWER_10*'. Emoji not required.
            text = os.getenv(f'ANSWER_{i}_TEXT')
            emoji = os.getenv(f'ANSWER_{i}_EMOJI')

            # Only add the answer if the TEXT variable exists
            if text:
                clean_emoji = emoji.strip() if emoji else None
                poll.add_answer(text=text, emoji=clean_emoji)
            
        # Validation: Discord polls require at least 2 answers
        if len(poll.answers) < 2:
            print("Error: Poll needs at least 2 answers. Check container ENV variables.")
            return
        # Send it
        await channel.send(poll=poll)
        print(f"Poll sent to {channel.name} at {datetime.datetime.now()}")
    else:
        print(f"Error: Could not find channel {channel_id}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Schedule set for: {target_hour:02d}:{target_minute:02d} {timezone_str}')
    
    # Start the loop if it is not already running
    if not daily_poll.is_running():
        daily_poll.start()

# --- RUN ---
if __name__ == "__main__":
    if not token:
        print("Error: DISCORD_TOKEN environment variable not set.")
    else:
        bot.run(token)