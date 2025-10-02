import random
from constants import ILLNESS_NAMES, TOTAL_MILES

def random_event(p):
    # chance no event
    if random.random() < 0.2:
        return

    # illness can strike anyone
    if random.random() < 0.5:
        target = None
        if p.party and random.random() < 0.6:  # 60% chance illness hits companion
            target = random.choice(p.party)
        else:
            target = p  # leader

        illness = random.choice(ILLNESS_NAMES)
        dmg = random.randint(5, 15)
        if isinstance(target, dict):  # if loaded from save
            target["health"] -= dmg
            if target["health"] <= 0:
                target["alive"] = False
                p.messages.append(f"{target['name']} has died from {illness}.")
            else:
                p.messages.append(f"{target['name']} fell ill with {illness} (-{dmg} health).")
        else:
            target.health -= dmg
            if target.health <= 0:
                target.alive = False
                p.messages.append(f"{target.name} has died from {illness}.")
            else:
                p.messages.append(f"{target.name} fell ill with {illness} (-{dmg} health).")

def consume_basics(p):
    # all party members eat
    eaters = 1 + len(p.party)
    if p.food >= eaters:
        p.food -= eaters
    else:
        # starvation damage
        for member in p.party:
            if member.get("alive", True):
                member["health"] -= random.randint(2, 5)
                if member["health"] <= 0:
                    member["alive"] = False
                    p.messages.append(f"{member['name']} starved to death.")
        p.health -= random.randint(3, 8)

def check_end(p):
    if p.health <= 0:
        p.alive = False
        print("\n💀 You have perished on the trail.")
        return True
    if all(m.get("alive", True) is False for m in p.party) and not p.alive:
        print("\n💀 All party members have died.")
        return True
    if p.miles_traveled >= TOTAL_MILES:
        print("\n🎉 You made it to the Willamette Valley! Congratulations!")
        return True
    return False
