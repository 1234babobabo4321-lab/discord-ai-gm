import discord
import openai
import os

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# 채널 ID (디스코드에서 우클릭 → ID 복사)
GM_CHANNEL_ID = 111111111111111111   # #gm-commands
PUBLIC_CHANNEL_ID = 222222222222222222  # #game-room

@client.event
async def on_ready():
    print(f"✅ 로그인 성공: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # GM 명령어 채널에서만 처리
    if message.channel.id == GM_CHANNEL_ID:
        # !draw → 이미지 생성
        if message.content.startswith("!draw"):
            prompt = message.content[5:].strip()
            await message.channel.send(f"🎨 `{prompt}` 준비 중...")

            response = openai.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="512x512"
            )
            image_url = response.data[0].url

            public_channel = client.get_channel(PUBLIC_CHANNEL_ID)
            await public_channel.send(f"🎨 {prompt}")
            await public_channel.send(image_url)

        # !gm → AI 텍스트 출력
        if message.content.startswith("!gm"):
            prompt = message.content[3:].strip()
            await message.channel.send(f"📜 `{prompt}` 처리 중...")

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "너는 TRPG 게임 마스터다."},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content

            public_channel = client.get_channel(PUBLIC_CHANNEL_ID)
            await public_channel.send(reply)

client.run(DISCORD_TOKEN)
