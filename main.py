# main.py
import time
import requests
import config
from analyzer import get_bybit_altcoins, analyze_news

seen_links = set()  # чтобы не слать повторные уведомления по одной и той же новости


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": config.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
    except Exception as ex:
        print(f"[main] Ошибка отправки в Telegram: {ex}")


def format_notification(result):
    coins_str = ", ".join(sorted(result["coins"]))
    keywords_str = ", ".join(result["keywords"])
    return (
        f"⚠️ <b>Новость может повлиять на монету(ы): {coins_str}</b>\n"
        f"Балл влияния: <b>{result['score']}/10</b>\n"
        f"Триггеры: {keywords_str}\n"
        f"Заголовок: {result['title']}\n"
        f"Ссылка: {result['link']}"
    )


def run_cycle():
    print("[main] Получаю список альткоинов с Bybit...")
    coins = get_bybit_altcoins()
    print(f"[main] Найдено {len(coins)} альткоинов")

    print("[main] Анализирую новости...")
    results = analyze_news(coins)

    for result in results:
        if result["link"] in seen_links:
            continue
        seen_links.add(result["link"])

        if result["score"] >= config.NOTIFY_THRESHOLD:
            msg = format_notification(result)
            print("[main] Отправляю уведомление:\n", msg)
            send_telegram_message(msg)


def main():
    print("[main] Бот запущен. Отслеживание новостного фона альткоинов Bybit...")
    while True:
        try:
            run_cycle()
        except Exception as ex:
            print(f"[main] Ошибка в цикле: {ex}")
        time.sleep(config.POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
