from player import Player
import actions

def test_travel_reduces_food_and_increases_miles():
    p = Player(name="Traveler")
    start_miles = p.miles_traveled
    start_food = p.food
    actions.travel(p)
    assert p.miles_traveled > start_miles
    assert p.food < start_food

def test_rest_increases_health():
    p = Player(name="Traveler", health=50)
    actions.rest(p)
    assert p.health >= 50  # should not drop

def test_hunt_consumes_ammo_and_may_add_food(monkeypatch):
    p = Player(name="Traveler", ammo=10)

    # Monkeypatch prompt_int to always spend 5 ammo
    monkeypatch.setattr("actions.prompt_int", lambda *a, **k: 5)

    start_food = p.food
    actions.hunt(p)

    assert p.ammo <= 5
    assert p.food >= start_food  # should not lose food
