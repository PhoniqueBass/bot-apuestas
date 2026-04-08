import requests
import time

API_KEY = "5f6aa5301d344e7f85442368f479a416"
TELEGRAM_TOKEN = "8578581416:AAHgeKIJPc74pZGFYtj_-QEXIa0He9QGoU4"
CHAT_ID = "761289383"

ENVIADO = False  # Controla que solo mande una señal


def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje
    }
    requests.post(url, json=payload)


def obtener_partidos():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()
    return data.get("matches", [])


def analizar_partido(match):
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]

    # 🔥 LÓGICA BASE (puedes mejorar luego)
    # De momento señal simple
    return f"⚠️ {home} vs {away}\nPosible GOL en 1ER TIEMPO"


def main():
    global ENVIADO

    print("🚀 BOT INICIADO...")

    while True:
        if ENVIADO:
            time.sleep(60)
            continue

        partidos = obtener_partidos()

        for match in partidos:
            estado = match["status"]

            # Solo partidos en vivo
            if estado == "IN_PLAY":
                mensaje = analizar_partido(match)

                enviar_telegram(mensaje)
                print("📩 Señal enviada a Telegram")

                ENVIADO = True
                break

        time.sleep(30)


if __name__ == "__main__":
    main()