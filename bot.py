import requests
import time
from flask import Flask
import threading

# =========================
# CONFIGURACIÓN
# =========================

TOKEN = "8578581416:AAHgeKIJPc74pZGFYtj_-QEXIa0He9QGoU4"
CHAT_ID = "761289383"
API_KEY = "TU_API_KEY_AQUI"

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
    except:
        print("Error enviando mensaje")

# =========================
# BOT PRINCIPAL
# =========================

def loop_bot():
    print("🔥 BOT INICIADO")

    enviados = set()

    while True:
        try:
            print("🚀 ANALIZANDO...")

            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            headers = {
                "X-RapidAPI-Key": API_KEY,
                "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
            }

            params = {
                "live": "all"
            }

            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            for partido in data["response"]:
                fixture = partido["fixture"]
                teams = partido["teams"]
                stats = partido["statistics"]

                minuto = fixture["status"]["elapsed"]

                # FILTRO MINUTOS
                if minuto is None or minuto < 20 or minuto > 40:
                    continue

                local = teams["home"]["name"]
                visitante = teams["away"]["name"]

                # ID único para evitar spam
                key = f"{local}-{visitante}"

                if key in enviados:
                    continue

                tiros = 0

                # SUMAR TIROS
                for equipo in stats:
                    for s in equipo["statistics"]:
                        if s["type"] == "Total Shots" and s["value"]:
                            tiros += int(s["value"])

                # CONDICIÓN DE ALERTA
                if tiros >= 10:
                    mensaje = f"""⚽ {local} vs {visitante}
⏱ Minuto: {minuto}
🔥 Tiros totales: {tiros}

👉 POSIBLE GOL EN 1ER TIEMPO"""

                    enviar_telegram(mensaje)
                    enviados.add(key)

            time.sleep(120)

        except Exception as e:
            print("ERROR:", e)
            time.sleep(20)

# =========================
# FLASK (para mantener activo en Render)
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "BOT ACTIVO"

# =========================
# INICIO
# =========================

if __name__ == "__main__":
    t = threading.Thread(target=loop_bot)
    t.start()

    app.run(host="0.0.0.0", port=10000)