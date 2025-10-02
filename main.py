import random
from dataclasses import dataclass, field

# ------------- Game Constants -------------
TOTAL_MILES = 2000
SHOP_PRICES = {"food": 0.5, "ammo": 2, "med_kit": 25, "wheel": 30}
PACE_TO_MILES = {"steady": 15, "strenuous": 25, "grueling": 35}
PACE_TO_FOOD = {"steady": 2, "strenuous": 3, "grueling": 5}  # food per person/day (we’ll assume 1 traveler for MVP)
ILLNESS_NAMES = ["dysentery", "cholera", "snakebite", "flu"]

# ------------- Data Models -------------
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

    @property
    def miles_remaining(self) -> int:
        return max(0, TOTAL_MILES - self.miles_traveled)

# ------------- Utility -------------
def prompt_choice(prompt, options):
    opts = "/".join(options)
    while True:
        choice = input(f"{prompt} [{opts}]: ").strip().lower()
        if choice in options:
            return choice
        print("Invalid choice.")

def prompt_int(prompt, min_val=0, max_val=None):
    while True:
        s = input(f"{prompt}: ").strip()
        if s.isdigit():
            n = int(s)
            if (max_val is None or n <= max_val) and n >= min_val:
                return n
        print("Invalid number.")

def print_status(p: Player):
    print("\n=== STATUS ===")
    print(f"Day: {p.day}")
    print(f"Miles traveled: {p.miles_traveled} / {TOTAL_MILES}  (remaining {p.miles_remaining})")
    print(f"Health: {p.health}")
    print(f"Food: {p.food} lbs")
    print(f"Ammo: {p.ammo} rounds")
    print(f"Med Kits: {p.med_kits}")
    print(f"Wagon Wheels: {p.wheels}")
    print(f"Cash: ${p.cash:.2f}")
    print(f"Pace: {p.pace}")
    if p.messages:
        print("\nRecent events:")
        for m in p.messages[-3:]:
            print(" -", m)
    print("==============\n")

# ------------- Core Actions -------------
def choose_pace(p: Player):
    pace = prompt_choice("Choose pace", list(PACE_TO_MILES.keys()))
    p.pace = pace
    p.messages.append(f"You set pace to {pace}.")

def travel(p: Player):
    if p.wheels <= 0:
        p.messages.append("You cannot travel—no wagon wheels! Buy one at the next shop.")
        return
    # miles covered
    miles = PACE_TO_MILES[p.pace] + random.randint(-5, 5)
    miles = max(5, miles)
    p.miles_traveled += miles
    # food consumption
    food_use = PACE_TO_FOOD[p.pace] + random.randint(0, 2)
    p.food -= food_use
    # health impact
    health_delta = -random.randint(0, 3) if p.pace != "steady" else -random.randint(0, 2)
    p.health += health_delta
    p.day += 1
    p.messages.append(f"Traveled {miles} miles; used {food_use} food; health {health_delta}.")

def rest(p: Player):
    # regain health; small food usage
    gain = random.randint(5, 12)
    p.health = min(100, p.health + gain)
    p.food -= 2
    p.day += 1
    p.messages.append(f"Rested and recovered {gain} health.")

def hunt(p: Player):
    # simple hunt mini-game: spend ammo, quick skill check for yield
    if p.ammo <= 0:
        p.messages.append("No ammo to hunt!")
        return
    rounds = min(10, p.ammo)
    spend = prompt_int(f"You have {p.ammo} rounds. How many to use for hunting (max {rounds})", 1, rounds)
    p.ammo -= spend

    print("\nHUNT: You’ll get 3 quick shots. Type ENTER fast when you see 'FIRE!'")
    hits = 0
    for i in range(3):
        # lightweight timing without imports: simulate reflex by random chance boosted by spend
        # More ammo => better odds (abstracted)
        base_chance = 0.35 + 0.02 * spend
        if random.random() < base_chance:
            print("FIRE!")
            input()  # user presses enter
            if random.random() < 0.7:
                hits += 1
                print("  Hit!")
            else:
                print("  Miss!")
        else:
            print("...no shot opportunity this moment.")

    meat = hits * random.randint(15, 35)
    if meat > 0:
        p.food += meat
        p.messages.append(f"Hunt success! {hits} hits, gained {meat} lbs of food.")
    else:
        p.messages.append("Hunt failed. No food gained.")
    p.day += 1
    # light health impact from exertion
    p.health -= random.randint(0, 2)

def shop(p: Player):
    print("\n=== GENERAL STORE ===")
    print("Prices per unit:")
    for k, v in SHOP_PRICES.items():
        print(f" - {k}: ${v}")
    print(f"Cash: ${p.cash:.2f}")
    print("(Enter 0 to skip an item)\n")

    for item, price in SHOP_PRICES.items():
        qty = prompt_int(f"Buy how many {item}", 0)
        cost = qty * price
        if cost > p.cash:
            print("  Not enough cash. Purchase skipped.")
            continue
        if item == "food":
            p.food += qty
        elif item == "ammo":
            p.ammo += qty
        elif item == "med_kit":
            p.med_kits += qty
        elif item == "wheel":
            p.wheels += qty
        p.cash -= cost
        print(f"  Bought {qty} {item} for ${cost:.2f}.")
    p.messages.append("You visited a trading post.")
    # shopping takes a day
    p.day += 1

# ------------- Random Events -------------
def random_event(p: Player):
    # Higher chance of bad events at higher pace, and when food is low
    bad_bias = 0
    if p.pace == "grueling":
        bad_bias += 1
    if p.food <= 0:
        bad_bias += 2

    roll = random.randint(1, 10) + bad_bias
    # 1-3 good, 4-7 neutral, 8-12 bad-ish
    if roll <= 3:
        found = random.choice(["food", "ammo", "cash"])
        if found == "food":
            gain = random.randint(10, 35)
            p.food += gain
            p.messages.append(f"Lucky find: +{gain} lbs food.")
        elif found == "ammo":
            gain = random.randint(3, 10)
            p.ammo += gain
            p.messages.append(f"Lucky find: +{gain} ammo.")
        else:
            gain = random.randint(5, 30)
            p.cash += gain
            p.messages.append(f"Lucky find: +${gain}.")
    elif roll >= 8:
        event = random.choice(["illness", "wheel_break", "lost_food", "robbed"])
        if event == "illness":
            illness = random.choice(ILLNESS_NAMES)
            dmg = random.randint(8, 20)
            p.health -= dmg
            used_kit = False
            if p.med_kits > 0 and p.health < 75 and random.random() < 0.6:
                p.med_kits -= 1
                heal = random.randint(10, 20)
                p.health = min(100, p.health + heal)
                used_kit = True
            msg = f"You fell ill with {illness} (-{dmg} health)."
            if used_kit:
                msg += " You used a med kit and recovered some health."
            p.messages.append(msg)
        elif event == "wheel_break":
            if p.wheels > 0:
                p.wheels -= 1
                p.messages.append("A wheel broke! You used one spare.")
            else:
                p.messages.append("A wheel broke—but you have no spares. Travel blocked until you buy one.")
        elif event == "lost_food":
            loss = min(p.food, random.randint(10, 40))
            p.food -= loss
            p.messages.append(f"Vermin raided your supplies: -{loss} food.")
        elif event == "robbed":
            loss = min(p.cash, float(random.randint(5, 30)))
            p.cash -= loss
            p.messages.append(f"Bandits! You lost ${loss:.2f}.")

# ------------- Turn Engine -------------
def consume_basics(p: Player):
    # starvation/health drain if out of food
    if p.food <= 0:
        p.health -= random.randint(3, 8)

def check_end(p: Player) -> bool:
    if p.health <= 0:
        p.alive = False
        print("\nYou have perished on the trail. 💀")
        return True
    if p.miles_traveled >= TOTAL_MILES:
        print("\n🎉 You made it to the Willamette Valley! Congratulations!")
        return True
    return False

def main_menu(p: Player):
    print_status(p)
    print("Actions:")
    print(" 1) travel")
    print(" 2) rest")
    print(" 3) hunt")
    print(" 4) pace")
    print(" 5) shop (trading post)")
    print(" 6) status")
    print(" 7) quit")
    choice = prompt_choice("Choose", ["1","2","3","4","5","6","7"])
    return choice

def game_loop(p: Player):
    print(f"\nWelcome, {p.name}. You have {TOTAL_MILES} miles to travel.\n")
    while True:
        choice = main_menu(p)
        if choice == "1":
            travel(p)
        elif choice == "2":
            rest(p)
        elif choice == "3":
            hunt(p)
        elif choice == "4":
            choose_pace(p)
        elif choice == "5":
            shop(p)
        elif choice == "6":
            print_status(p)
            continue
        elif choice == "7":
            print("Goodbye!")
            break

        # daily upkeep
        consume_basics(p)
        random_event(p)

        if check_end(p):
            break

def intro() -> Player:
    print("==== PY-TRAIL ====")
    print("A lightweight Oregon Trail–style terminal game.\n")
    name = input("Traveler, what is your name? ").strip() or "Traveler"
    print("\nStarting loadout:")
    print(" - 200 lbs food")
    print(" - 30 ammo")
    print(" - 1 med kit")
    print(" - 1 spare wheel")
    print(" - $200 cash\n")
    return Player(name=name)

if __name__ == "__main__":
    random.seed()  # allow true randomness
    player = intro()
    game_loop(player)
