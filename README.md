Py-Trail (Modular Version)

Py-Trail is a Python reimagining of the classic Oregon Trail, built as a text-based terminal game.
This branch contains the modular refactor: the codebase is split into multiple files for easier maintenance, with added save/load functionality and unit tests.

📂 Project Structure

pytrail/
• main.py – Entry point, intro + game loop
• player.py – Player dataclass, save/load helpers
• actions.py – Travel, rest, hunt, shop, change pace
• events.py – Random events, consumption, end checks
• ui.py – Menus, prompts, status display
• constants.py – Game constants (distances, prices, etc.)
• tests/ – Unit tests (pytest)
• test_player.py
• test_actions.py
• test_events.py

🎮 Gameplay

Travel – Move forward, consume food, risk illness or wagon damage

Rest – Recover health, spend time and food

Hunt – Spend ammo to gather food

Change Pace – Choose between steady, strenuous, or grueling travel

Shop – Visit trading posts to buy supplies

Status – Check inventory, health, and progress

Save/Load – Save progress to savegame.json and resume later

Win by reaching 2,000 miles to the Willamette Valley.
Lose if your health reaches 0.

▶️ Running the Game

Clone the repo and switch to the modular branch
git clone https://github.com/Das-Panda/pytrail.git
