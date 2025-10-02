from landmarks import check_landmark, handle_river, handle_fort
from actions import travel, rest, hunt, choose_pace, shop
from ui import print_status, prompt_choice
from player import Player, save_game, load_game
from events import random_event, consume_basics, check_end
import random

def main_menu(p):
    print_status(p)
    print("Actions:")
    print(" 1) travel")
    print(" 2) rest")
    print(" 3) hunt")
    print(" 4) pace")
    print(" 5) shop")
    print(" 6) status")
    print(" 7) save game")
    print(" 8) load game")
    print(" 9) quit")
    return prompt_choice("Choose", [str(i) for i in range(1, 10)])

def game_loop(p):
    print(f"\nWelcome, {p.name}. You have {p.miles_remaining} miles to travel.\n")
    while True:
        choice = main_menu(p)
        if choice == "1":
            travel(p)
            lm = check_landmark(p)
            if lm:
                if lm["type"] == "fort":
                    handle_fort(p, lm)
                elif lm["type"] == "river":
                    handle_river(p, lm)
                elif lm["type"] == "end":
                    print("\n🎉 You’ve reached the Willamette Valley! The journey is over!")
                    break
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
            save_game(p)
            continue
        elif choice == "8":
            loaded = load_game()
            if loaded:
                p = loaded
            continue
        elif choice == "9":
            print("Goodbye!")
            break

        consume_basics(p)
        random_event(p)

        if check_end(p):
            break

def intro() -> Player:
    print("==== PY-TRAIL ====")
    print("A lightweight Oregon Trail–style terminal game.\n")

    name = input("Leader, what is your name? ").strip() or "Leader"
    player = Player(name=name)

    print("\nNow, let’s add your companions.")
    for i in range(1, 5):  # up to 4 companions
        cname = input(f"Enter name for companion {i} (leave blank to skip): ").strip()
        if not cname:
            break
        player.add_party_member(cname)

    return player

if __name__ == "__main__":
    random.seed()
    choice = prompt_choice("New game or load?", ["new", "load"])
    if choice == "load":
        player = load_game() or intro()
    else:
        player = intro()
    game_loop(player)
