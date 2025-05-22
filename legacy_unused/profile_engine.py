import json
import os

PROFILE_FILE = "user_profile.json"

def load_profile():
    if not os.path.exists(PROFILE_FILE):
        return {"current_profile": "default", "profiles": {"default": {}}}
    with open(PROFILE_FILE, "r") as f:
        return json.load(f)

def save_profile(data):
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_current_profile():
    profile_data = load_profile()
    return profile_data.get("current_profile", "default")

def switch_profile(name):
    profile_data = load_profile()
    if name not in profile_data["profiles"]:
        profile_data["profiles"][name] = {}
    profile_data["current_profile"] = name
    save_profile(profile_data)
    return f"👤 Switched to profile: {name}"

