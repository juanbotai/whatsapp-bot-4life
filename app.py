from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "juan123"

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = "1086651537871868"


@app.route("/")
def inicio():
    return "Bot WhatsApp funcionando"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":

        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200

        return "Token incorrecto", 403

    if request.method == "POST":

        data = request.get_json()

        print("MENSAJE RECIBIDO:")
        print(data)

        try:
            mensaje = data["entry"][0]["changes"][0]["value"]["messages"][0]
            remitente = mensaje["from"]
            texto = mensaje["text"]["body"]

            respuesta = f"Hola Juan recibió tu mensaje: {texto}"

            url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

            headers = {
                "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": remitente,
                "type": "text",
                "text": {
                    "body": respuesta
                }
            }

            r = requests.post(url, headers=headers, json=payload)

            print("RESPUESTA META:")
            print(r.text)

        except Exception as e:
            print("ERROR:", str(e))

        return "EVENT_RECEIVED", 200

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
