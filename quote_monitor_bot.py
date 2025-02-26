import asyncio
from dotenv import load_dotenv
import os
import requests
import time
import pandas as pd
import telegram
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask
from telegram.constants import ParseMode

# Carica le variabili dal file .env
load_dotenv()

# Legge le chiavi dal file .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")

# Configura il bot Telegram
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# API per ottenere le quote da Betfair o altri bookmaker
API_URL = "https://api.the-odds-api.com/v4/sports/soccer/odds/"

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
                    alerts.append(f"\U0001F4C9 **Movimento quota!** {teams}\n" 
                                  f"Bookmaker: {bookmaker['title']}\n" 
                                  f"Quota iniziale: {initial_odds} -> Quota attuale: {latest_odds} ({change:.2f}%)\n")
    return alerts

# Funzione per inviare notifiche su Telegram
async def send_alerts(alerts):
    if not alerts:
        print("⚠️ Nessun alert da inviare.")
        return  # Esce dalla funzione se alerts è vuoto
    
    for alert in alerts:
        await bot.send_message(chat_id=CHAT_ID, text=alert, parse_mode=ParseMode.MARKDOWN)

# Avvio del monitoraggio delle quote
async def main():
    print("Inizio monitoraggio delle quote...")
    while True:
        odds_data = get_odds()
        if odds_data:
            alerts = analyze_odds(odds_data)
            if alerts:
                await send_alerts(alerts)  # Ora è atteso correttamente
        await asyncio.sleep(600)  # Attende senza bloccare il processo

if __name__ == "__main__":
    asyncio.run(main())  # Avvia il loop asincrono


# Creazione del server Flask per Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Simuliamo una porta aperta
    app.run(host="0.0.0.0", port=port)
