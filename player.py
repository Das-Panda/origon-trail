import json
import os

BAD_WORDS = {
    "fuck", "shit", "bitch", "asshole", "bastard", "dick", "cunt",
    "pussy", "fart", "cock", "balls", "slut", "whore", "dildo",
    "rape", "cum", "jizz", "penis", "vagina", "tits", "boobs"
}

class Player:
    def __init__(self, name="Leader"):
        clean_name, replaced = self._sanitize_name(name)
        self.name = clean_name
        self.party = []
        self.health = 100
        self.food = 500
        self.ammo = 100
        self.med_kits = 2
        self.wheels = 1
        self.cash = 100.0
        self.pace = "steady"
        self.day = 1
        self.miles_traveled = 0
        self.miles_remaining = 2000
        self.messages = []
        if replaced:
            msg = f"Leader name not allowed. Set to '{self.name}' instead."
            print(msg)  # immediate feedback
            self.messages.append(msg)

    def _sanitize_name(self, name: str):
        clean = name.strip()
        lower = clean.lower()
        if any(bad in lower for bad in BAD_WORDS):
            return "Traveler", True
        return (clean if clean else "Traveler"), (clean == "")

    def add_party_member(self, name):
        member_name, replaced = self._sanitize_name(name)
        self.party.append({
            "name": member_name,
            "health": 100,
            "alive": True
        })
        if replaced:
            msg = f"A party member name was not allowed and was replaced with '{member_name}'."
            print(msg)  # immediate feedback
            self.messages.append(msg)

    def to_dict(self):
        return {
            "name": self.name,
            "party": self.party,
            "health": self.health,
            "food": self.food,
            "ammo": self.ammo,
            "med_kits": self.med_kits,
            "wheels": self.wheels,
            "cash": self.cash,
            "pace": self.pace,
            "day": self.day,
            "miles_traveled": self.miles_traveled,
            "miles_remaining": self.miles_remaining,
            "messages": self.messages
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(name=data["name"])
        obj.party = data["party"]
        obj.health = data["health"]
        obj.food = data["food"]
        obj.ammo = data["ammo"]
        obj.med_kits = data["med_kits"]
        obj.wheels = data["wheels"]
        obj.cash = data["cash"]
        obj.pace = data["pace"]
        obj.day = data["day"]
        obj.miles_traveled = data["miles_traveled"]
        obj.miles_remaining = data["miles_remaining"]
        obj.messages = data["messages"]
        return obj


SAVE_FILE = "savegame.json"

def save_game(player):
    with open(SAVE_FILE, "w") as f:
        json.dump(player.to_dict(), f)
    print("Game saved!")

def load_game():
    if not os.path.exists(SAVE_FILE):
        print("No saved game found.")
        return None
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
        return Player.from_dict(data)
