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
        requests.post(url, data=data)
    except Exception as e:
        print("Error enviando mensaje:", e)

# =========================
# LOGICA DEL BOT
# =========================
def analizar_partidos():
    enviados = set()

    while True:
        print("🚀 ANALIZANDO...")

        # PRUEBA SIMPLE
        partido = "TEST BOT FUNCIONANDO"

        if partido not in enviados:
            mensaje = f"✅ {partido}"
            enviar_telegram(mensaje)
            enviados.add(partido)

        time.sleep(60)

# =========================
# SERVIDOR WEB (RENDER)
# =========================
app = Flask(__name__)

@app.route('/')
def home():
    return "BOT ACTIVO"

def run_bot():
    analizar_partidos()

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)