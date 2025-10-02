import random
from actions import shop

LANDMARKS = [
    {"mile": 200, "name": "Kansas River Crossing", "type": "river", "width": 600}, 
    {"mile": 500, "name": "Fort Kearny", "type": "fort"},
    {"mile": 800, "name": "Platte River", "type": "river", "width": 1000},
    {"mile": 1200, "name": "Fort Laramie", "type": "fort"},
    {"mile": 1600, "name": "Snake River Crossing", "type": "river", "width": 1400},
    {"mile": 2000, "name": "Willamette Valley", "type": "end"}
]

def check_landmark(player):
    """Check if player has reached or passed a new landmark."""
    for lm in LANDMARKS:
        if player.miles_traveled >= lm["mile"] and lm["name"] not in player.messages:
            player.messages.append(f"Reached {lm['name']}")
            return lm
    return None

def handle_fort(player, landmark):
    """Handle arriving at a fort."""
    print(f"\nYou have reached {landmark['name']} (mile {landmark['mile']}).")
    print("At the fort you may rest and resupply.")
    while True:
        print("\nFort options:")
        print(" 1) Visit trading post")
        print(" 2) Rest at the fort ($5 per person, restores health)")
        print(" 3) Leave fort")
        choice = input("Choose [1/2/3]: ").strip()

        if choice == "1":
            # Prices increase the further west you go
            inflation = 1 + (landmark["mile"] / 2000)  
            shop(player, inflation=inflation)
        elif choice == "2":
            cost = 5 * (1 + len(player.party))
            if player.cash >= cost:
                player.cash -= cost
                healed = random.randint(5, 15)
                player.health = min(100, player.health + healed)
                for member in player.party:
                    if member["alive"]:
                        member["health"] = min(100, member["health"] + healed)
                print(f"Your party rested. Everyone recovered about {healed} health.")
                player.day += 1
            else:
                print("Not enough cash to rest.")
        elif choice == "3":
            break

def handle_river(player, landmark):
    """Handle river crossing choices."""
    print(f"\nYou have reached the {landmark['name']} (about {landmark['width']} feet wide).")
    print("Choices:")
    print(" 1) Ford the river (risk drowning and losing supplies)")
    print(" 2) Caulk the wagon and float (less risk, wagon may be damaged)")
    print(" 3) Pay for a ferry ($10)")
    choice = input("Choose [1/2/3]: ").strip()

    if choice == "1":  # Ford
        if random.random() < 0.5:
            loss_food = random.randint(20, 60)
            player.food = max(0, player.food - loss_food)
            injured = random.choice(player.party) if player.party else None
            if injured and injured["alive"]:
                injured["health"] -= random.randint(10, 25)
                if injured["health"] <= 0:
                    injured["alive"] = False
                    player.messages.append(f"{injured['name']} drowned while fording {landmark['name']}.")
            player.messages.append(f"Disaster! You lost {loss_food} food fording {landmark['name']}.")
        else:
            player.messages.append(f"You forded {landmark['name']} successfully.")
    elif choice == "2":  # Float
        if random.random() < 0.2:
            player.wheels = max(0, player.wheels - 1)
            player.messages.append(f"The wagon was damaged while floating across {landmark['name']}.")
        else:
            player.messages.append(f"You floated safely across {landmark['name']}.")
    elif choice == "3":  # Ferry
        if player.cash >= 10:
            player.cash -= 10
            player.messages.append(f"You paid $10 for the ferry and crossed {landmark['name']} safely.")
        else:
            player.messages.append("You didn’t have enough cash for the ferry, forced to ford!")
            handle_river(player, {"name": landmark["name"], "width": landmark["width"], "type": "river"})
