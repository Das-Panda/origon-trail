Py-Trail

A lightweight, Oregon Trail–style text adventure written in Python. You take on the role of a wagon leader guiding your party westward. Manage your food, supplies, and companions while facing random events, hunting, and river crossings.

This branch includes the new Party System and Profanity Filter milestone.

Features

Core game loop with actions: travel, rest, hunt, change pace, shop, check status, save/load, and quit.

Random events like sickness, resource loss, or accidents.

Landmarks including forts and rivers, with choices for crossing or resupplying.

Save/load system using JSON files.

Party system:

Create up to 4 companions in addition to the leader.

Each party member has health and a living/deceased status.

Food consumption scales with party size.

Profanity filter:

Prevents inappropriate names for the leader and party members.

Automatically replaces disallowed names with "Traveler."

Prints a live warning and logs an event in the status screen.

How to Play

Start the game with:
python main.py

Choose whether to start a new game or load a saved game.

Enter your name and add up to 4 companions. If a name is invalid, it will be replaced and a warning will be shown.

Each turn, choose from the menu of actions:

Travel to progress toward Oregon.

Rest to recover health (uses food).

Hunt for food (uses ammo).

Change pace to alter miles per day and risk.

Shop at forts for supplies.

View party status.

Save or load your game.

Quit at any time.

Requirements

Python 3.8+

Runs in a terminal (Windows PowerShell, macOS Terminal, Linux shell).

Current Branch: party-system

This branch represents the milestone with:

Companion party members

Expanded status screen

Profanity filter with live warnings

Updated save/load to store party data

Next Planned Enhancements

Party member health loss from random events and travel.

Expanded landmark interactions.

More diverse random events (weather, wagon damage).

Endgame scoring system based on survivors and supplies.
