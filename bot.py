import discord
import os
from discord.ext import tasks, commands
from datetime import time
from zoneinfo import ZoneInfo  # Built-in to Python 3.9+

# --- CONFIGURATION ---
# These are loaded from the Docker environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
# Default to 0 if not set, to prevent crash on int() conversion
CHANNEL_ID = int(os.getenv('CHANNEL_ID', '0'))
# Default to Chicago time so you don't have to do math
TIMEZONE_STR = os.getenv('TZ', 'America/Chicago') 

# Define when the message sends (24-hour format)
TARGET_HOUR = 16  # 4:00 PM
TARGET_MINUTE = 0

# --- SETUP ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- THE TASK ---
# We set the time with explicit timezone info
schedule_time = time(hour=TARGET_HOUR, minute=TARGET_MINUTE, tzinfo=ZoneInfo(TIMEZONE_STR))

@tasks.loop(time=schedule_time)
async def daily_poll():
    # Ensure the bot waits until it is fully ready before running the first loop
    await bot.wait_until_ready()
    
    channel = bot.get_channel(CHANNEL_ID)
    
    if channel:
        # Create the message design (Embed)
        embed = discord.Embed(
            title="🎮 Gaming Roll Call 📣",
            description="Who is available to play tonight?",
            color=0x5865F2 # Discord Blurple
        )
        embed.add_field(name="Status", value="✅ = I'm in!\n❌ = Busy\n🤔 = Maybe")
        embed.set_footer(text="React below to vote")

        # Send the message
        message = await channel.send(embed=embed)
        
        # Add reactions for voting
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await message.add_reaction("🤔")
    else:
        print(f"Error: Could not find channel with ID {CHANNEL_ID}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Target Time: {TARGET_HOUR}:{TARGET_MINUTE:02d} {TIMEZONE_STR}')
    
    # Start the loop if it is not already running
    if not daily_poll.is_running():
        daily_poll.start()

# --- RUN ---
if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN environment variable not set.")
    else:
        bot.run(TOKEN)