
import json
import os

LOG_FILE = "query_log.json"

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_log(log):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

def add_log_entry(entry):
    log = load_log()
    log.append(entry)
    save_log(log)
    return f"📘 Logged: {entry}"

def get_log():
    log = load_log()
    if not log:
        return "📭 No reading log entries yet."
    return "\n".join([f"- {e}" for e in log[-20:]])
