# ~/Desktop/archives/config_loader.py

import json
import os

CONFIG_FILE = "config.json"

# Default settings (can be modified later)
DEFAULT_CONFIG = {
    "theme": "dark",                # Options: "dark", "light", "auto"
    "mode": "cozy",                 # Options: "cozy", "dramatic", "snarky"
    "whiskerly_verbosity": "medium",  # Options: "silent", "low", "medium", "chaotic"
    "auto_export": False,           # If True, export tools run after each update
    "day_night_splash": True        # Enables time-based splash screen theme
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def update_config_field(key, value):
    config = load_config()
    config[key] = value
    save_config(config)
    print(f"⚙️ Updated '{key}' to: {value}")

# Example usage
if __name__ == "__main__":
    cfg = load_config()
    print("🧭 Current Configuration:")
    for k, v in cfg.items():
        print(f"  {k}: {v}")

    # Example change:
    update_config_field("whiskerly_verbosity", "chaotic")

