import os
import discord
from openai import OpenAI
from dotenv import load_dotenv
from prompts import shadowheart_prompt

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client_openai = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()

intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower().startswith("poll:"):
        poll_content = message.content[5:].strip()

        chat_response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": shadowheart_prompt},
                {"role": "user", "content": f"The party must choose: {poll_content}. What would you pick?"}
            ],
            temperature=0.7
        )

        vote = chat_response.choices[0].message.content.strip()
        await message.channel.send(f"🖤 Shadowheart votes: **{vote}**")


client.run(DISCORD_TOKEN)