import discord
import openai
import os

# 환경 변수에서 토큰 불러오기
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ {client.user} 로그인 성공!')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith("!gm"):
        prompt = message.content[3:].strip()
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 TRPG 게임 마스터다. 플레이어의 입력과 주사위 결과에 맞춰 상황을 묘사해라."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        await message.channel.send(reply)

client.run(DISCORD_TOKEN)
