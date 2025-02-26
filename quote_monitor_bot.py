from dotenv import load_dotenv
import os

# Carica le variabili dal file .env
load_dotenv()

# Legge le chiavi dal file .env
TELEGRAM_TOKEN = os.getenv("7586561608:AAHFEJpFQLEL4scHPUrdyB34-azNUz6XVOQ")
CHAT_ID = os.getenv("6146221712")
API_KEY = os.getenv("a5e03878c41b43724fae135d2eb62d22")
import requests
import time
import pandas as pd
import telegram
from bs4 import BeautifulSoup
from datetime import datetime

# Configura il bot Telegram
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# API per ottenere le quote da Betfair o altri bookmaker
API_URL = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
API_KEY = "YOUR_ODDS_API_KEY"

# Funzione per ottenere quote e rilevare variazioni significative
def get_odds():
    params = {
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal",
        "apiKey": API_KEY
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Errore nell'acquisizione delle quote:", response.status_code)
        return None

# Funzione per analizzare il movimento delle quote
def analyze_odds(odds_data, threshold=5):
    alerts = []
    for match in odds_data:
        teams = match["home_team"] + " vs " + match["away_team"]
        for bookmaker in match["bookmakers"]:
            for market in bookmaker["markets"]:
                initial_odds = market["outcomes"][0]["price"]
                latest_odds = market["outcomes"][1]["price"]
                change = ((latest_odds - initial_odds) / initial_odds) * 100
                
                if abs(change) >= threshold:
                    alerts.append(f"📉 **Movimento quota!** {teams}\n" 
                                  f"Bookmaker: {bookmaker['title']}\n" 
                                  f"Quota iniziale: {initial_odds} -> Quota attuale: {latest_odds} ({change:.2f}%)\n")
    return alerts

# Funzione per inviare notifiche su Telegram
def send_alerts(alerts):
    for alert in alerts:
        bot.send_message(chat_id=CHAT_ID, text=alert, parse_mode=telegram.ParseMode.MARKDOWN)

# Funzione principale per eseguire il bot
if __name__ == "__main__":
    print("Inizio monitoraggio delle quote...")
    while True:
        odds_data = get_odds()
        if odds_data:
            alerts = analyze_odds(odds_data)
            if alerts:
                send_alerts(alerts)
        time.sleep(600)  # Controlla ogni 10 minuti
import os
import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Porta finta per Render
    app.run(host="0.0.0.0", port=port)import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Simuliamo una porta aperta
    app.run(host="0.0.0.0", port=port)
