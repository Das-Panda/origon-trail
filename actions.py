import random
from ui import prompt_int

def travel(p):
    """Advance the player by miles depending on pace, consume food, and increase day."""
    if p.pace == "steady":
        miles = random.randint(12, 20)
    elif p.pace == "strenuous":
        miles = random.randint(18, 30)
    elif p.pace == "grueling":
        miles = random.randint(25, 35)
    else:
        miles = random.randint(10, 15)

    p.miles_traveled += miles
    p.miles_remaining = max(0, p.miles_remaining - miles)
    p.day += 1

    food_used = (len(p.party) + 1) * 5  # 5 lbs per person including leader
    p.food = max(0, p.food - food_used)

    p.messages.append(f"Traveled {miles} miles. {p.miles_remaining} miles left.")


def rest(p):
    """Rest to regain some health but consume food."""
    heal = random.randint(1, 5)
    p.health = min(100, p.health + heal)
    p.day += 1

    food_used = (len(p.party) + 1) * 3
    p.food = max(0, p.food - food_used)

    p.messages.append(f"The party rested. Health +{heal}, food -{food_used}.")


def hunt(p):
    """Hunt for food using ammo. Food gain depends on success."""
    if p.ammo <= 0:
        p.messages.append("You have no ammo to hunt with.")
        return

    shots = min(p.ammo, 5)
    p.ammo -= shots

    food_gained = random.randint(20, 80)
    p.food += food_gained
    p.day += 1

    p.messages.append(f"You hunted using {shots} ammo and gained {food_gained} lbs of food.")


def choose_pace(p):
    """Change the party’s pace setting."""
    print("\nChoose a new pace:")
    print("1) Steady (12–20 miles/day, low risk)")
    print("2) Strenuous (18–30 miles/day, medium risk)")
    print("3) Grueling (25–35 miles/day, high risk)")

    choice = prompt_int("Enter choice", 1, 3)
    if choice == 1:
        p.pace = "steady"
    elif choice == 2:
        p.pace = "strenuous"
    else:
        p.pace = "grueling"

    p.messages.append(f"Pace set to {p.pace}.")


def shop(p):
    """Buy supplies with cash at a fort."""
    print("\nWelcome to the shop. You have ${:.2f}.".format(p.cash))
    print("Items for sale:")
    print("1) Food - $0.25 per lb")
    print("2) Ammo - $2 per 10 rounds")
    print("3) Med Kit - $15 each")
    print("4) Wagon Wheel - $20 each")

    while True:
        choice = prompt_int("What do you want to buy? (0 to exit)", 0, 4)
        if choice == 0:
            break
        elif choice == 1:
            qty = prompt_int("How many lbs of food?", 0)
            cost = qty * 0.25
            if p.cash >= cost:
                p.cash -= cost
                p.food += qty
                p.messages.append(f"Bought {qty} lbs food.")
            else:
                print("Not enough money!")
        elif choice == 2:
            qty = prompt_int("How many bundles of 10 ammo?", 0)
            cost = qty * 2
            if p.cash >= cost:
                p.cash -= cost
                p.ammo += qty * 10
                p.messages.append(f"Bought {qty*10} rounds of ammo.")
            else:
                print("Not enough money!")
        elif choice == 3:
            qty = prompt_int("How many med kits?", 0)
            cost = qty * 15
            if p.cash >= cost:
                p.cash -= cost
                p.med_kits += qty
                p.messages.append(f"Bought {qty} med kits.")
            else:
                print("Not enough money!")
        elif choice == 4:
            qty = prompt_int("How many wagon wheels?", 0)
            cost = qty * 20
            if p.cash >= cost:
                p.cash -= cost
                p.wheels += qty
                p.messages.append(f"Bought {qty} wagon wheels.")
            else:
                print("Not enough money!")
