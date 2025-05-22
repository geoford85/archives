from datetime import datetime

def get_time_based_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "☀️ Good morning!"
    elif 12 <= hour < 18:
        return "🌤️ Good afternoon!"
    elif 18 <= hour < 22:
        return "🌙 Good evening!"
    else:
        return "🌌 Burning the midnight oil, are we?"

