import json
from datetime import datetime

MEMORY_FILE = "query_history.json"

def save_memory(command, response, context=None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "response": response,
        "context": context or {}
    }
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(entry)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data[-20:], f, indent=2)

def get_last_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            return data[-1] if data else None
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def clear_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)
    return "🧠 Memory wiped clean!"

def summarize_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            return "\n".join([
                f"{i+1}. {entry['command']} → {entry['response']}"
                for i, entry in enumerate(data[-5:])
            ]) or "🧠 Nothing remembered yet."
    except:
        return "🧠 Error fetching memory history."

def get_context():
    last = get_last_memory()
    return last["context"] if last and "context" in last else {}

