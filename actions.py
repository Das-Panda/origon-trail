import random
from ui import prompt_int
from constants import PACE_TO_MILES, PACE_TO_FOOD, SHOP_PRICES

def choose_pace(p):
    from ui import prompt_choice
    pace = prompt_choice("Choose pace", list(PACE_TO_MILES.keys()))
    p.pace = pace
    p.messages.append(f"You set pace to {pace}.")

def travel(p):
    if p.wheels <= 0:
        p.messages.append("You cannot travel—no wagon wheels!")
        return
    miles = PACE_TO_MILES[p.pace] + random.randint(-5, 5)
    miles = max(5, miles)
    p.miles_traveled += miles
    food_use = PACE_TO_FOOD[p.pace] + random.randint(0, 2)
    p.food -= food_use
    p.health -= random.randint(0, 3) if p.pace != "steady" else random.randint(0, 2)
    p.day += 1
    p.messages.append(f"Traveled {miles} miles; used {food_use} food.")

def rest(p):
    gain = random.randint(5, 12)
    p.health = min(100, p.health + gain)
    p.food -= 2
    p.day += 1
    p.messages.append(f"Rested and recovered {gain} health.")

def hunt(p):
    if p.ammo <= 0:
        p.messages.append("No ammo to hunt!")
        return
    rounds = min(10, p.ammo)
    spend = prompt_int(f"You have {p.ammo} rounds. How many to use (max {rounds})", 1, rounds)
    p.ammo -= spend
    hits = random.randint(0, 3)
    meat = hits * random.randint(15, 35)
    if meat > 0:
        p.food += meat
        p.messages.append(f"Hunt success! {hits} hits, gained {meat} lbs of food.")
    else:
        p.messages.append("Hunt failed. No food gained.")
    p.day += 1
    p.health -= random.randint(0, 2)

def shop(p):
    print("\n=== GENERAL STORE ===")
    for k, v in SHOP_PRICES.items():
        print(f" - {k}: ${v}")
    print(f"Cash: ${p.cash:.2f}\n")
    for item, price in SHOP_PRICES.items():
        qty = prompt_int(f"Buy how many {item}", 0)
        cost = qty * price
        if cost > p.cash:
            print("  Not enough cash.")
            continue
        if item == "food": p.food += qty
        elif item == "ammo": p.ammo += qty
        elif item == "med_kit": p.med_kits += qty
        elif item == "wheel": p.wheels += qty
        p.cash -= cost
        print(f"  Bought {qty} {item} for ${cost:.2f}.")
    p.messages.append("You visited a trading post.")
    p.day += 1
