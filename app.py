from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bot WhatsApp funcionando"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    return "Webhook activo", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
