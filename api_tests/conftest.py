import pytest

@pytest.fixture()
def parse_version():
    return [1, 2, 3]
from generators.players import Player
@pytest.fixture()
def get_player_generator():
    return Player()