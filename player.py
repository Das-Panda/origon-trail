from dataclasses import dataclass, field, asdict
import json
from constants import TOTAL_MILES, SAVE_FILE

@dataclass
class PartyMember:
    name: str
    health: int = 100
    alive: bool = True

    def apply_damage(self, dmg: int):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False
            self.health = 0

@dataclass
class Player:
    name: str
    health: int = 100
    food: int = 200
    ammo: int = 30
    med_kits: int = 1
    wheels: int = 1
    cash: float = 200.0
    miles_traveled: int = 0
    day: int = 1
    pace: str = "steady"
    alive: bool = True
    messages: list = field(default_factory=list)
    party: list = field(default_factory=list)  # NEW: companions

    @property
    def miles_remaining(self) -> int:
        return max(0, TOTAL_MILES - self.miles_traveled)

    def to_dict(self):
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

# ---------------- Save/Load ----------------
def save_game(p: Player):
    with open(SAVE_FILE, "w") as f:
        json.dump(p.to_dict(), f, indent=2)

def load_game() -> Player | None:
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        return Player.from_dict(data)
    except FileNotFoundError:
        return None
