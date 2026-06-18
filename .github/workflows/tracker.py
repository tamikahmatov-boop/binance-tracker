import json
import time
import requests
from datetime import datetime

BOT_TOKEN = "8626739818:AAFt7kmdfTgTVlXD-5FnKOVYq1fvNW9hUAw"
CHAT_ID = "6716942872"

print("START")

# Получаем цены
r = requests.get('https://api.binance.com/api/v3/ticker/price', timeout=15)
prices = r.json()
print("Prices loaded:", len(prices))

# История
try:
    with open('history.json', 'r') as f:
        history = json.load(f)
except:
    history = {}

now = time.time()
up_list = []
down_list = []

for item in prices:
    sym = item['symbol']
    if not sym.endswith('USDT'):
        continue
    
    price = float(item['price'])
    
    if sym not in history:
        history[sym] = []
    
    history[sym].append({'t': now, 'p': price})
    
    # Оставляем 2 часа
    history[sym] = [x for x in history[sym] if x['t'] > now - 7200]
    
    if len(history[sym]) >= 2:
        old_price = history[sym][0]['p']
        age_min = (now - history[sym][0]['t']) / 60
        
        if age_min >= 30:
            change = (price - old_price) / old_price * 100
            
            if change >= 10:
                up_list.append(f"🟢 {sym}: +{change:.2f}%")
            elif change <= -10:
                down_list.append(f"🔴 {sym}: {change:.2f}%")

# Сохраняем историю
with open('history.json', 'w') as f:
    json.dump(history, f)

# Отправка в Telegram
if up_list or down_list:
    msg = f"📊 {datetime.now().strftime('%H:%M')}\n\n"
    
    if up_list:
        msg += "🟢 РОСТ 10%+ за час:\n" + "\n".join(up_list[:10])
    
    if down_list:
        if up_list:
            msg += "\n\n"
        msg += "🔴 ПАДЕНИЕ 10%+ за час:\n" + "\n".join(down_list[:10])
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': CHAT_ID, 'text': msg}, timeout=10)
    print("SENT")
else:
    print("No signals")
