import os
from player import Player, save_game, load_game
from constants import SAVE_FILE

def test_save_and_load(tmp_path):
    """Save and load should restore the same player state"""
    # Use temp save file
    save_file = tmp_path / "savegame.json"

    p = Player(name="Tester", health=75, food=123)
    with open(save_file, "w") as f:
        pass  # ensure file exists

    # Override SAVE_FILE for this test
    import constants
    constants.SAVE_FILE = str(save_file)

    save_game(p)
    loaded = load_game()

    assert loaded is not None
    assert loaded.name == "Tester"
    assert loaded.health == 75
    assert loaded.food == 123
