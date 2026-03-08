# ============================================================
#  app.py  –  Flask Web UI with Conversation Memory
# ============================================================

from flask import Flask, render_template, request, jsonify, session
from router import handle_message
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # for session management

@app.route("/")
def index():
    session['history'] = []  # reset history on page load
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data    = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Empty message"}), 400

    # ── Get conversation history from session ──
    history = session.get('history', [])

    # ── Get response ──
    result = handle_message(message, history)

    # ── Update history ──
    history.append({"role": "user",      "content": message})
    history.append({"role": "assistant", "content": result["response"]})

    # ── Keep last 20 messages only ──
    if len(history) > 20:
        history = history[-20:]

    session['history'] = history

    return jsonify(result)

@app.route("/reset", methods=["POST"])
def reset():
    session['history'] = []
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)