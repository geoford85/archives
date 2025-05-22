import json
from time_engine import get_time_of_day

MOOD_FILE = "user_settings.json"

MOODS = {
    "default": "neutral",
    "cozy": "cozy",
    "dramatic": "dramatic",
    "whimsical": "whimsical"
}

def get_current_mood():
    try:
        with open(MOOD_FILE, "r") as f:
            settings = json.load(f)
        return settings.get("mood", "default")
    except (FileNotFoundError, json.JSONDecodeError):
        return "default"

def set_mood(mood):
    mood = mood.lower()
    if mood not in MOODS:
        return f"⚠️ '{mood}' isn’t a known mood. Try: cozy, dramatic, whimsical, or default."
    try:
        with open(MOOD_FILE, "r") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}
    settings["mood"] = mood
    with open(MOOD_FILE, "w") as f:
        json.dump(settings, f, indent=2)
    return f"🧠 Mood set to '{mood}'!"

def get_dynamic_greeting():
    time_of_day = get_time_of_day()
    mood = get_current_mood()

    # Default mood auto-switching
    if mood == "default":
        if time_of_day == "morning":
            return "☀️ Good morning! Time for an adventure?"
        elif time_of_day == "afternoon":
            return "📚 Good afternoon! Fancy something thrilling?"
        else:
            return "🌙 Good evening! Let's snuggle up with a story 🌙📚"

    # Manual override mood-based greetings
    if mood == "cozy":
        return f"{time_of_day.title()} vibes and blankets. Let’s find a comforting read 🫖"
    elif mood == "dramatic":
        return f"{time_of_day.title()} darkness looms… but there is still time for one more chapter. 🗡️"
    elif mood == "whimsical":
        return f"{time_of_day.title()} mischief detected! Let’s follow a flying book 🐾📖"

    return f"{time_of_day.title()} vibes ahead… what tale shall we pursue?"


