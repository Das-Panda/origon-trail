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

def print_status(p):
    from constants import TOTAL_MILES
    print("\n=== STATUS ===")
    print(f"Day: {p.day}")
    print(f"Miles traveled: {p.miles_traveled} / {TOTAL_MILES} (remaining {p.miles_remaining})")
    print(f"Leader Health: {p.health}")
    print(f"Food: {p.food} lbs")
    print(f"Ammo: {p.ammo} rounds")
    print(f"Med Kits: {p.med_kits}")
    print(f"Wagon Wheels: {p.wheels}")
    print(f"Cash: ${p.cash:.2f}")
    print(f"Pace: {p.pace}")

    print("\nParty Members:")
    if not p.party:
        print("  (none)")
    else:
        for member in p.party:
            status = "Alive" if member["alive"] else "Deceased"
            print(f"  {member['name']}: {member['health']} hp ({status})")

    print("\nRecent events:")
    if p.messages:
        for m in p.messages[-3:]:
            print(" -", m)
    else:
        print("  None yet")
    print("==============\n")
