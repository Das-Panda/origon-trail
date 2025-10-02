from player import Player
import events

def test_consume_basics_reduces_health_if_no_food():
    p = Player(name="Traveler", food=0, health=50)
    events.consume_basics(p)
    assert p.health < 50

def test_check_end_returns_true_on_death():
    p = Player(name="Traveler", health=0)
    ended = events.check_end(p)
    assert ended is True
    assert not p.alive

def test_check_end_returns_true_on_victory():
    p = Player(name="Traveler", miles_traveled=2000)
    ended = events.check_end(p)
    assert ended is True
