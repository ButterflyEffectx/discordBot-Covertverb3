import os
import nextcord
import random
import json

from myserver import server_on

intents = nextcord.Intents.default()
intents.message_content = True
client = nextcord.Client(intents=intents)

# คำกิริยาและรูปแบบช่องที่ 3
verbs = {
    "be": "been",
    "begin": "begun",
    "break": "broken",
    "bring": "brought",
    "build": "built",
    "buy": "bought",
    "catch": "caught",
    "choose": "chosen",
    "come": "come",
    "do": "done",
    "drink": "drunk",
    "drive": "driven",
    "eat": "eaten",
    "fall": "fallen",
    "find": "found",
    "fly": "flown",
    "forget": "forgotten",
    "get": "gotten",
    "give": "given",
    "go": "gone",
    "have": "had",
    "hear": "heard",
    "know": "known",
    "learn": "learned/learnt",
    "leave": "left",
    "lose": "lost",
    "make": "made",
    "meet": "met",
    "pay": "paid",
    "put": "put",
    "read": "read",
    "ride": "ridden",
    "ring": "rung",
    "run": "run",
    "say": "said",
    "see": "seen",
    "sell": "sold",
    "send": "sent",
    "sing": "sung",
    "sit": "sat",
    "sleep": "slept",
    "speak": "spoken",
    "spend": "spent",
    "stand": "stood",
    "swim": "swum",
    "take": "taken",
    "teach": "taught",
    "tell": "told",
    "think": "thought",
    "throw": "thrown",
    "understand": "understood",
    "wake": "woken",
    "wear": "worn",
    "win": "won",
    "write": "written"
}

user_active = {}
user_scores = {}
high_scores = {}

# Load high scores from a file
def load_high_scores():
    global high_scores
    try:
        with open('high_scores.json', 'r') as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = {}

# Save high scores to a file
def save_high_scores():
    with open('high_scores.json', 'w') as f:
        json.dump(high_scores, f)

@client.event
async def on_ready():
    load_high_scores()
    print(f'เข้าสู่ระบบเป็น {client.user} แล้วจ้า')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/Verb'):
        if user_active.get(message.author.id):
            embed = nextcord.Embed(
                title="เกมเริ่มแล้ว!",
                description="เฮ้ย! เริ่มเกมไปแล้วนะ จะหยุดก็ใช้คำสั่ง `/StopVerb` นะจ๊ะ",
                color=nextcord.Color.orange()
            )
            await message.channel.send(embed=embed)
            return

        user_active[message.author.id] = True
        user_scores[message.author.id] = 0
        verb, past_participle = random.choice(list(verbs.items()))
        user_active[message.author.id] = verb

        embed = nextcord.Embed(
            title="ทดสอบคำกิริยา!",
            description=f"แปลกิริยา 'ช่องสาม' ของ '{verb}' มาเร็ว!",
            color=nextcord.Color.blue()
        )
        await message.channel.send(embed=embed)

    elif message.content.startswith('/StopVerb'):
        if user_active.get(message.author.id):
            score = user_scores.pop(message.author.id, 0)
            user_active.pop(message.author.id, None)
            # Update high score
            if message.author.id in high_scores:
                high_scores[message.author.id] = max(high_scores[message.author.id], score)
            else:
                high_scores[message.author.id] = score
            save_high_scores()

            embed = nextcord.Embed(
                title="จบเกม!",
                description=f"โอเค จบเกม! สกอร์ของคุณคือ {score} ไว้เจอกันใหม่นะเฟรน!",
                color=nextcord.Color.red()
            )
            await message.channel.send(embed=embed)
        else:
            embed = nextcord.Embed(
                title="ยังไม่ได้เริ่มเกม",
                description="ยังไม่ได้เล่นเกมเลยนะ! จะหยุดทำไมเนี่ย",
                color=nextcord.Color.yellow()
            )
            await message.channel.send(embed=embed)
            
    elif message.content.startswith('/ScoreVerb'):
        score = user_scores.get(message.author.id, 0)
        high_score = high_scores.get(message.author.id, 0)

        embed = nextcord.Embed(
            title="คะแนนของคุณ",
            description=f"คะแนนปัจจุบันของคุณ: {score}\nคะแนนสูงสุดที่บันทึก: {high_score}",
            color=nextcord.Color.gold()
        )
        await message.channel.send(embed=embed)

    elif user_active.get(message.author.id):
        verb = user_active[message.author.id]
        past_participle = verbs[verb]

        if message.content.lower() == past_participle:
            user_scores[message.author.id] += 1
            score = user_scores[message.author.id]

            embed = nextcord.Embed(
                title="ถูกต้อง!",
                description=f"โห ใช่เลย! '{verb}' -> '{past_participle}' เก่งเวอร์! สกอร์ของคุณตอนนี้คือ {score}",
                color=nextcord.Color.green()
            )
            await message.channel.send(embed=embed)
            verb, past_participle = random.choice(list(verbs.items()))
            user_active[message.author.id] = verb
            embed = nextcord.Embed(
                title="ทดสอบคำกิริยาใหม่!",
                description=f"แปลกิริยา 'ช่องสาม' ของ '{verb}' มาเร็ว!",
                color=nextcord.Color.purple()
            )
            await message.channel.send(embed=embed)
        else:
            embed = nextcord.Embed(
                title="ไม่ถูกต้อง",
                description=f"ไม่ใช่อ่ะ ลองอีกที! กิริยา 'ช่องสาม' ของ '{verb}' คืออะไรนะ?",
                color=nextcord.Color.red()
            )
            await message.channel.send(embed=embed)
            
server_on()
            
client.run(os.getenv('TOKEN'))

