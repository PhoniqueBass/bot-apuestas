import requests
import time
import threading
from flask import Flask

TOKEN = "8578581416:AAHgeKIJPc74pZGFYtj_-QEXIa0He9QGoU4"
CHAT_ID = "761289383"

app = Flask(__name__)

# =========================
# TELEGRAM
# =========================
def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": mensaje
        })
        print("Telegram:", r.text)
    except Exception as e:
        print("Error Telegram:", e)

# =========================
# LOOP PRINCIPAL
# =========================
def loop_bot():
    print("🔥 BOT INICIADO")

    enviados = set()

    while True:
        try:
            print("🚀 ANALIZANDO...")

            partido = "BOT ACTIVO EN RENDER"

            if partido not in enviados:
                enviar_telegram(f"✅ {partido}")
                enviados.add(partido)

            time.sleep(60)

        except Exception as e:
            print("ERROR LOOP:", e)
            time.sleep(10)

# =========================
# ARRANQUE FORZADO
# =========================
def iniciar_bot():
    t = threading.Thread(target=loop_bot)
    t.daemon = True
    t.start()

# IMPORTANTE: forzar inicio SIEMPRE
iniciar_bot()

# =========================
# FLASK
# =========================
@app.route('/')
def home():
    return "BOT FUNCIONANDO"

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)