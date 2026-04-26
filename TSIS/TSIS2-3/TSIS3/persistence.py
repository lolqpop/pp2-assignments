import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_settings():
    default = {
        "sound": True,
        "car_color": "blue",
        "difficulty": "normal"
    }

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default)
        return default

    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []

    with open(LEADERBOARD_FILE, "r") as file:
        return json.load(file)


def save_leaderboard(data):
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)