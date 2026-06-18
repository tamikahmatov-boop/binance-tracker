import json
import time
import requests
from datetime import datetime

# ============================================
# ВСТАВЬТЕ СВОИ ДАННЫЕ СЮДА:
# ============================================
BOT_TOKEN = "8626739818:AAFt7kmdfTgTVlXD-5FnKOVYq1fvNW9hUAw"
CHAT_ID = "6716942872"
# ============================================

THRESHOLD = 10
HISTORY_FILE = 'history.json'

def load_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_history(h):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(h, f)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'HTML'}, timeout=10)

print(f"Start: {datetime.now().strftime('%H:%M:%S')}")

try:
    prices = requests.get('https://api.binance.com/api/v3/ticker/price', timeout=15).json()
except:
    print("Error fetching prices")
    exit(1)

print(f"Got {len(prices)} tickers")

history = load_history()
now = time.time()
up_signals = []
down_signals = []

for item in prices:
    symbol = item['symbol']
    if not symbol.endswith('USDT'):
        continue
    
    try:
        price = float(item['price'])
    except:
        continue
    
    if symbol not in history:
        history[symbol] = []
    
    history[symbol].append({'t': now, 'p': price})
    history[symbol] = [e for e in history[symbol] if e['t'] > now - 7200]
    
    if len(history[symbol]) >= 2:
        old = history[symbol][0]['p']
        age = (now - history[symbol][0]['t']) / 60
        
        if age >= 30:
            change = (price - old) / old * 100
            
            if change >= THRESHOLD:
                up_signals.append(f"🟢 {symbol}: +{change:.2f}%")
            elif change <= -THRESHOLD:
                down_signals.append(f"🔴 {symbol}: {change:.2f}%")

save_history(history)

if up_signals or down_signals:
    msg = f"📊 {datetime.now().strftime('%H:%M')}\n\n"
    if up_signals:
        msg += "🟢 РОСТ 10%+ за час:\n" + "\n".join(up_signals[:10])
    if down_signals:
        if up_signals:
            msg += "\n\n"
        msg += "🔴 ПАДЕНИЕ 10%+ за час:\n" + "\n".join(down_signals[:10])
    
    send_telegram(msg)
    print(f"Sent: {len(up_signals)} up, {len(down_signals)} down")
else:
    print("No signals")
