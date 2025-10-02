import random
from constants import ILLNESS_NAMES, TOTAL_MILES

def random_event(p):
    if random.random() < 0.2:
        return
    if random.random() < 0.5:
        illness = random.choice(ILLNESS_NAMES)
        dmg = random.randint(5, 15)
        p.health -= dmg
        p.messages.append(f"You fell ill with {illness} (-{dmg} health).")

def consume_basics(p):
    if p.food <= 0:
        p.health -= random.randint(3, 8)

def check_end(p):
    if p.health <= 0:
        p.alive = False
        print("\n💀 You have perished on the trail.")
        return True
    if p.miles_traveled >= TOTAL_MILES:
        print("\n🎉 You made it to the Willamette Valley! Congratulations!")
        return True
    return False
