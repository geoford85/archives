import json
import os

SETTINGS_FILE = "user_settings.json"

DEFAULT_SETTINGS = {
    "whiskerly_enabled": True,
    "theme": "cozy gothic"
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=2)
        return DEFAULT_SETTINGS.copy()
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def toggle_setting(key):
    settings = load_settings()
    if key not in settings:
        return f"⚠️ Unknown setting: {key}"
    settings[key] = not settings[key]
    save_settings(settings)
    status = "enabled" if settings[key] else "disabled"
    return f"🪄 Setting '{key}' is now {status}."

def set_theme(theme_name):
    settings = load_settings()
    settings["theme"] = theme_name
    save_settings(settings)
    return f"🎨 Theme updated to '{theme_name}'. Archie approves."

def get_settings_summary():
    settings = load_settings()
    summary = "\n".join([f"- {k}: {v}" for k, v in settings.items()])
    return f"🛠️ Current settings:\n{summary}"

