import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import aiohttp
from datetime import datetime
from flask import Flask

# flask config

app = Flask(__name__)

@app.route('/')
def home():
  return "<h1> Bot is running </h1>"

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Bot setup
client = commands.Bot(command_prefix='&', intents=intents)

# Global variables
check_task = None
last_seen_titles = set()
notification_channel = None

# Functions
async def fetch_recent_episodes():
    global last_seen_titles, notification_channel

    # Jikan API endpoints - multiple sources for better coverage
    apis = [
        {
            "name": "Current Season",
            "url": "https://api.jikan.moe/v4/seasons/now",
            "key": "data"
        },
        {
            "name": "Currently Airing",
            "url": "https://api.jikan.moe/v4/top/anime?filter=airing&limit=25",
            "key": "data"
        }
    ]

    async with aiohttp.ClientSession() as session:
        new_episodes = []
        
        for api in apis:
            try:
                print(f"🔍 Fetching from {api['name']}: {api['url']}")
                
                async with session.get(api['url'], timeout=15) as res:
                    if res.status != 200:
                        print(f"⚠️ Failed to fetch from {api['name']} (Status: {res.status})")
                        continue

                    data = await res.json()
                    anime_list = data.get(api['key'], [])
                    
                    if not anime_list:
                        print(f"⚠️ No anime found in {api['name']}")
                        continue

                    # Process anime entries
                    for anime in anime_list[:10]:  # Limit to prevent spam
                        title = anime.get('title', 'Unknown Anime')
                        title_english = anime.get('title_english') or title
                        mal_id = anime.get('mal_id')
                        
                        # Create unique identifier
                        unique_id = f"{mal_id}_{title}"
                        
                        # Check if this is new
                        if unique_id not in last_seen_titles:
                            episode_info = {
                                'title': title_english,
                                'title_jp': title,
                                'mal_id': mal_id,
                                'score': anime.get('score'),
                                'status': anime.get('status'),
                                'aired_from': anime.get('aired', {}).get('from'),
                                'episodes': anime.get('episodes'),
                                'url': anime.get('url'),
                                'image': anime.get('images', {}).get('jpg', {}).get('image_url', ''),
                                'synopsis': anime.get('synopsis', '')[:200] + '...' if anime.get('synopsis') else 'No synopsis available'
                            }
                            
                            new_episodes.append(episode_info)
                            last_seen_titles.add(unique_id)

                # Rate limiting - Jikan has rate limits
                await asyncio.sleep(1)
                
            except asyncio.TimeoutError:
                print(f"⏰ Timeout accessing {api['name']}")
            except aiohttp.ClientError as e:
                print(f"🌐 Network error accessing {api['name']}: {e}")
            except Exception as e:
                print(f"❌ Error with {api['name']}: {e}")

        # Send notifications if new episodes found
        if new_episodes:
            print(f"🎉 {len(new_episodes)} new anime found!")
            
            if notification_channel:
                # Create embed with better formatting
                embed = discord.Embed(
                    title="🎉 New Anime Updates!",
                    color=0x00ff00,
                    description="Recently updated anime from MyAnimeList",
                    timestamp=datetime.utcnow()
                )
                
                for anime in new_episodes[:5]:  # Limit to 5 to avoid spam
                    field_value = f"**Status:** {anime['status']}\n"
                    
                    if anime['score']:
                        field_value += f"**Score:** {anime['score']}/10\n"
                    
                    if anime['episodes']:
                        field_value += f"**Episodes:** {anime['episodes']}\n"
                    
                    field_value += f"**Synopsis:** {anime['synopsis']}\n"
                    field_value += f"[View on MAL]({anime['url']})"
                    
                    embed.add_field(
                        name=f"📺 {anime['title']}",
                        value=field_value,
                        inline=False
                    )
                
                if len(new_episodes) > 5:
                    embed.add_field(
                        name="And more...",
                        value=f"{len(new_episodes) - 5} additional anime updates!",
                        inline=False
                    )
                
                embed.set_footer(text="Powered by Jikan API (MyAnimeList)")
                
                # Set thumbnail if available
                if new_episodes[0]['image']:
                    embed.set_thumbnail(url=new_episodes[0]['image'])
                
                await notification_channel.send(embed=embed)
            
            # Console output
            for anime in new_episodes:
                print(f"📺 {anime['title']}")
                print(f"🔗 {anime['url']}")
                print(f"⭐ Score: {anime['score']}/10" if anime['score'] else "⭐ Score: Not rated")
                print("-" * 50)
        
        else:
            print("😴 No new anime updates found")

async def check_loop():
    print("✅ Anime release checker started. Checking every 60 minutes.")
    # Initial check
    await fetch_recent_episodes()
    
    while True:
        try:
            await asyncio.sleep(3600)  # 60 minutes (Jikan rate limits)
            await fetch_recent_episodes()
        except asyncio.CancelledError:
            print("🛑 Anime release checker stopped.")
            break
        except Exception as e:
            print(f"❌ Error in check loop: {e}")
            await asyncio.sleep(600)  # Wait 10 minutes before retrying

# Event: Bot is ready
@client.event
async def on_ready():
    print(f'✅ {client.user} is online!')
    print(f'📊 Connected to {len(client.guilds)} server(s)')

# Commands
@client.command()
async def start(ctx):
    global check_task, notification_channel
    
    if check_task and not check_task.done():
        await ctx.send("❌ Anime checker is already running!")
        return
    
    notification_channel = ctx.channel
    check_task = asyncio.create_task(check_loop())
    
    embed = discord.Embed(
        title="✅ Anime Checker Started!",
        description="Using Jikan API (MyAnimeList) for reliable anime updates",
        color=0x00ff00
    )
    embed.add_field(
        name="📍 Channel Set",
        value=f"Notifications will be sent to {ctx.channel.mention}",
        inline=False
    )
    embed.add_field(
        name="⏰ Check Interval",
        value="Every 60 minutes (respects API rate limits)",
        inline=False
    )
    
    await ctx.send(embed=embed)

@client.command()
async def stop(ctx):
    global check_task
    
    if check_task and not check_task.done():
        check_task.cancel()
        try:
            await check_task
        except asyncio.CancelledError:
            pass
        await ctx.send("🛑 Anime release checker stopped.")
    else:
        await ctx.send("❌ Anime checker is not running!")

@client.command()
async def status(ctx):
    global check_task, notification_channel
    
    embed = discord.Embed(title="📊 Bot Status", color=0x0099ff)
    
    if check_task and not check_task.done():
        embed.add_field(name="🟢 Checker Status", value="Running", inline=True)
    else:
        embed.add_field(name="🔴 Checker Status", value="Stopped", inline=True)
    
    if notification_channel:
        embed.add_field(name="📍 Notification Channel", value=notification_channel.mention, inline=True)
    else:
        embed.add_field(name="📍 Notification Channel", value="Not set", inline=True)
    
    embed.add_field(name="📈 Anime Tracked", value=len(last_seen_titles), inline=True)
    embed.add_field(name="🌐 API Source", value="Jikan (MyAnimeList)", inline=True)
    
    await ctx.send(embed=embed)

@client.command()
async def setchannel(ctx):
    global notification_channel
    notification_channel = ctx.channel
    
    embed = discord.Embed(
        title="✅ Channel Updated!",
        description=f"Notifications will now be sent to {ctx.channel.mention}",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

@client.command()
async def test(ctx):
    """Test the API connection"""
    await ctx.send("🔍 Testing API connection...")
    await fetch_recent_episodes()
    await ctx.send("✅ Test completed! Check console for results.")

@client.command()
async def clear(ctx):
    """Clear the tracking cache"""
    global last_seen_titles
    count = len(last_seen_titles)
    last_seen_titles.clear()
    await ctx.send(f"🗑️ Cleared {count} tracked anime from cache. Next check will show all current anime as 'new'.")

# Error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Unknown command! Use `&help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing required arguments! Check the command usage.")
    else:
        print(f"Error: {error}")
        await ctx.send("❌ An error occurred while processing the command.")

# Run the bot
if __name__ == "__main__":
    import threading

    # Run Flask in a thread
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

    if not TOKEN:
        print("❌ Discord token not found! Please set DISCORD_TOKEN in your .env file")
    else:
        client.run(TOKEN)
