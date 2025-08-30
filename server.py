from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# seznam všech zpráv s jejich koncem platnosti
messages = []

@app.route("/", methods=["GET", "POST"])
def index():
    global messages
    if request.method == "POST":
        msg = request.form.get("msg", "")
        end = request.form.get("end_time", "")
        if msg and end:
            end_dt = datetime.strptime(end, "%Y-%m-%dT%H:%M")
            messages.append({
                "text": msg,
                "end_time": end_dt,
                "start_time": datetime.now()
            })
        return redirect(url_for('index'))

    now = datetime.now()
    active_messages = [m for m in messages if m["end_time"] > now]

    return render_template("index.html", active_messages=active_messages)

@app.route("/notification", methods=["GET"])
def get_notification():
    now = datetime.now()
    active_messages = [m for m in messages if m["end_time"] > now]
    # sloučí všechny aktivní zprávy do jednoho textu odděleného \n
    if not active_messages:
        return ""
    combined = "\n".join([f"{m['text']} (do {m['end_time'].strftime('%H:%M %d.%m.%Y')})"
                          for m in active_messages])
    return combined

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
