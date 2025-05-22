import json
from datetime import datetime

QUERY_LOG_FILE = "query_log.json"

def track_query(user_input, response):
    log = []
    try:
        with open(QUERY_LOG_FILE, "r") as f:
            log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log = []

    log.append({
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "response": response
    })

    # Only keep the last 10 queries
    log = log[-10:]

    with open(QUERY_LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def get_last_query():
    try:
        with open(QUERY_LOG_FILE, "r") as f:
            log = json.load(f)
        if log:
            last = log[-1]
            return f"🕰️ Last query was:\n\n📥 {last['user_input']}\n📤 {last['response']}"
        return "📭 No query history found yet."
    except Exception:
        return "⚠️ Couldn’t retrieve last query."

