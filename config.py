# config.py
import os

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.getenv("8623750363:AAGHdc0t4HCBmV8fvgWrMaTH9xKD0JbzEyk", "PASTE_YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("6716942872", "PASTE_YOUR_CHAT_ID_HERE")

# --- Bybit: публичный endpoint списка спотовых тикеров (не нужен API-ключ) ---
BYBIT_TICKERS_URL = "https://api.bybit.com/v5/market/tickers?category=spot"

# --- Новостные RSS-источники ---
NEWS_RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cryptopanic.com/news/rss/",
    "https://decrypt.co/feed",
]

POLL_INTERVAL_SECONDS = 300  # опрос раз в 5 минут
NOTIFY_THRESHOLD = 5         # минимальный балл для уведомления (0-10)

# Ключевые слова и их вес влияния (0-10)
IMPACT_KEYWORDS = {
    "hack": 9, "hacked": 9, "exploit": 9,
    "delist": 9, "delisting": 9,
    "bankrupt": 10, "bankruptcy": 10,
    "sec lawsuit": 10, "sec sues": 10,
    "regulation": 7, "regulatory": 7,
    "ban": 8, "banned": 8,
    "investigation": 7, "fraud": 9,
    "rug pull": 10, "insolvency": 10,
    "listing": 6, "listed": 6,
    "partnership": 5, "integration": 4,
    "upgrade": 5, "mainnet": 6,
    "hard fork": 6, "airdrop": 5,
    "funding round": 5, "investment": 4,
    "roadmap": 3, "update": 2,
    "announcement": 2, "collaboration": 3, "testnet": 2,
}
