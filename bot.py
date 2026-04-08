import requests
import time
from flask import Flask
import threading

# =========================
# CONFIG
# =========================
TOKEN = "8578581416:AAHgeKIJPc74pZGFYtj_-QEXIa0HeQGoU4"
CHAT_ID = "761289383"

# =========================
# TELEGRAM
# =========================
def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mensaje
    }
    try:
        r = requests.post(url, data=data)
        print("Telegram response:", r.text)
    except Exception as e:
        print("Error Telegram:", e)

# =========================
# BOT LOOP
# =========================
def analizar_partidos():
    enviados = set()

    while True:
        try:
            print("🚀 ANALIZANDO...")

            partido = "TEST BOT FUNCIONANDO"

            if partido not in enviados:
                mensaje = f"✅ {partido}"
                enviar_telegram(mensaje)
                enviados.add(partido)

            time.sleep(60)

        except Exception as e:
            print("Error en loop:", e)
            time.sleep(10)

# =========================
# FLASK (RENDER)
# =========================
app = Flask(__name__)

@app.route('/')
def home():
    return "BOT ACTIVO"

# =========================
# START BOT (IMPORTANTE)
# =========================
threading.Thread(target=analizar_partidos, daemon=True).start()

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)