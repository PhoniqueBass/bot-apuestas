import requests
import time

API_KEY = "5f6aa5301d344e7f85442368f479a416"
BOT_TOKEN = "8578581416:AAHgeKIJPc74pZGFYtj_-QEXIa0He9QGoU4"
CHAT_ID = "761289383"

HEADERS = {"X-Auth-Token": API_KEY}

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def analizar():
    url = "https://api.football-data.org/v4/matches"
    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        print("Error API")
        return

    data = r.json()
    matches = data.get("matches", [])

    for m in matches:
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]
        status = m["status"]

        # SOLO partidos en vivo
        if status == "IN_PLAY":
            mensaje = f"🔥 EN VIVO: {home} vs {away}\nPosible gol pronto"
            enviar_telegram(mensaje)
            print(mensaje)
            return  # solo una señal

def main():
    print("🚀 BOT CORRIENDO EN RENDER...")

    while True:
        try:
            analizar()
        except Exception as e:
            print("ERROR:", e)

        time.sleep(60)  # cada 60 segundos

if __name__ == "__main__":
    main()