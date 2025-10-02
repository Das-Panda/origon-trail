Py-Trail (Party System Version)

Py-Trail is a Python reimagining of the classic Oregon Trail, built as a text-based terminal game.
This branch introduces a party system: you now travel with companions who have their own health, can fall ill, consume food, and may die along the journey.

📂 Project Structure

pytrail/
• main.py – Entry point, intro, and game loop
• player.py – Player and PartyMember data models, save/load helpers
• actions.py – Travel, rest, hunt, shop, change pace
• events.py – Random events, illness, starvation, end checks
• ui.py – Menus, prompts, and status display
• constants.py – Game constants (distances, prices, illnesses, etc.)
• tests/ – Unit tests (pytest)

🎮 Gameplay

Travel – Move forward, consume food, risk illness or wagon damage

Rest – Recover health, spend time and food

Hunt – Spend ammo to gather food

Change Pace – Switch between steady, strenuous, or grueling travel

Shop – Buy supplies at trading posts

Status – Check inventory, health, and progress

Save/Load – Save progress to a file and resume later

Party System – Companions join your journey, consume food, can fall ill, and may die

Win by reaching 2,000 miles to the Willamette Valley.
Lose if all members of your party, including the leader, die.

▶️ Running the Game

Clone the repository and switch to the party-system branch

Run the game with python main.py

At startup you can choose:
• new → start a fresh game and recruit companions
• load → resume from a previous save

🧪 Running Tests

The tests cover save/load, core actions, events, and the new party mechanics.

Install pytest with pip install pytest
Run tests with pytest

✨ Features in Party System Version

Party members with individual health values

Companions consume food each day

Illness and starvation can affect any member

Companions can die during the journey

Game ends if all travelers perish

Modular structure with unit tests

🚀 Roadmap / Possible Enhancements

Individual traits for companions (strength, hunting skill, resistance to illness)

Events that target or involve specific companions

Morale system (party health affected by deaths or food shortages)

Expanded landmark and river crossing challenges

Difficulty settings and expanded random events
