import requests
import time
from flask import Flask
import threading

# =========================
# CONFIGURACIÓN
# =========================

TOKEN = "8578581416:AAHgeKIJPc74pZGFYtj_-QEXIa0He9QGoU4"
CHAT_ID = "761289383"
API_KEY = "5f6aa5301d344e7f85442368f479a416"

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
        print("📩 Enviado a Telegram")
    except Exception as e:
        print("❌ Error Telegram:", e)

# =========================
# BOT PRINCIPAL
# =========================

def loop_bot():
    print("🔥 BOT INICIADO")

    enviados = set()

    while True:
        try:
            print("🚀 ANALIZANDO...")

            # ENDPOINT CORRECTO PARA API-FOOTBALL
            url = "https://v3.football.api-sports.io/fixtures"

            headers = {
                "x-apisports-key": API_KEY
            }

            params = {
                "live": "all"
            }

            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            for partido in data.get("response", []):
                fixture = partido.get("fixture", {})
                teams = partido.get("teams", {})

                minuto = fixture.get("status", {}).get("elapsed")

                # FILTRO DE MINUTO
                if minuto is None or minuto < 20 or minuto > 40:
                    continue

                fixture_id = fixture.get("id")

                # =========================
                # OBTENER ESTADÍSTICAS
                # =========================

                stats_url = "https://v3.football.api-sports.io/fixtures/statistics"

                stats_response = requests.get(
                    stats_url,
                    headers=headers,
                    params={"fixture": fixture_id}
                )

                stats_data = stats_response.json()

                tiros = 0

                for equipo in stats_data.get("response", []):
                    for s in equipo.get("statistics", []):
                        if s.get("type") == "Total Shots" and s.get("value"):
                            tiros += int(s["value"])

                local = teams.get("home", {}).get("name", "Local")
                visitante = teams.get("away", {}).get("name", "Visitante")

                key = f"{fixture_id}"

                if key in enviados:
                    continue

                # =========================
                # CONDICIÓN DE ALERTA
                # =========================

                if tiros >= 10:
                    mensaje = f"""⚽ {local} vs {visitante}
⏱ Minuto: {minuto}
🔥 Tiros totales: {tiros}

👉 POSIBLE GOL EN 1ER TIEMPO"""

                    enviar_telegram(mensaje)
                    enviados.add(key)

            time.sleep(120)

        except Exception as e:
            print("❌ ERROR:", e)
            time.sleep(20)

# =========================
# FLASK (RENDER)
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "BOT ACTIVO"

# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    hilo = threading.Thread(target=loop_bot)
    hilo.start()

    app.run(host="0.0.0.0", port=10000)