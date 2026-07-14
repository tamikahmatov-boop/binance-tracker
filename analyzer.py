# analyzer.py
import re
import requests
import feedparser
import config


def get_bybit_altcoins():
    """Возвращает множество базовых символов альткоинов, торгуемых на Bybit spot (без BTC/ETH/стейблов)."""
    resp = requests.get(config.BYBIT_TICKERS_URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    symbols = set()
    exclude = {"BTC", "ETH", "USDT", "USDC", "DAI", "FDUSD"}
    for item in data.get("result", {}).get("list", []):
        base = item.get("symbol", "").replace("USDT", "").replace("USDC", "")
        if base and base not in exclude:
            symbols.add(base)
    return symbols


def fetch_news_entries():
    """Собирает записи новостей из всех RSS-источников."""
    entries = []
    for url in config.NEWS_RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries:
                title = e.get("title", "")
                summary = e.get("summary", "")
                link = e.get("link", "")
                entries.append({"title": title, "summary": summary, "link": link})
        except Exception as ex:
            print(f"[analyzer] Ошибка чтения фида {url}: {ex}")
    return entries


def find_mentioned_coins(text, coins):
    """Ищет упоминания тикеров монет в тексте (по словам, с границами)."""
    found = set()
    upper_text = text.upper()
    for coin in coins:
        pattern = r"\b" + re.escape(coin) + r"\b"
        if re.search(pattern, upper_text):
            found.add(coin)
    return found


def calculate_impact_score(text):
    """Считает балл влияния 0-10 на основе ключевых слов из config.IMPACT_KEYWORDS."""
    text_lower = text.lower()
    total = 0
    matched = []
    for keyword, weight in config.IMPACT_KEYWORDS.items():
        if keyword in text_lower:
            total += weight
            matched.append(keyword)
    score = min(10, total)  # ограничиваем сверху 10
    return score, matched


def analyze_news(coins):
    """Основная функция: проходит по новостям, ищет монеты и считает балл влияния.
    Возвращает список словарей с результатами анализа (только с ненулевым влиянием)."""
    results = []
    entries = fetch_news_entries()
    for entry in entries:
        full_text = f"{entry['title']} {entry['summary']}"
        mentioned = find_mentioned_coins(full_text, coins)
        if not mentioned:
            continue
        score, matched_keywords = calculate_impact_score(full_text)
        if score == 0:
            continue
        results.append({
            "coins": mentioned,
            "score": score,
            "keywords": matched_keywords,
            "title": entry["title"],
            "link": entry["link"],
        })
    return results
