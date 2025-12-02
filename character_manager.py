import os
from custom_exceptions import (
    CharacterError,
    InvalidCharacterClassError,
    CharacterNotFoundError,
    CharacterDeadError,
    DataError,
)

SAVE_DIR = os.path.join(os.path.dirname(__file__), "data", "save_games")

# Base stats for required classes
CLASS_STATS = {
    "Warrior": {"max_health": 120, "strength": 15, "magic": 3},
    "Mage": {"max_health": 80, "strength": 4, "magic": 18},
    "Rogue": {"max_health": 100, "strength": 12, "magic": 6},
    "Cleric": {"max_health": 90, "strength": 8, "magic": 12},
}


def create_character(name, class_name):
    if class_name not in CLASS_STATS:
        raise InvalidCharacterClassError("Invalid class: " + class_name)

    stats = CLASS_STATS[class_name]
    char = {
        "name": name,
        "class": class_name,
        "level": 1,
        "health": stats["max_health"],
        "max_health": stats["max_health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 0,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
    }
    return char


def _get_save_path(name):
    if not os.path.isdir(SAVE_DIR):
        os.makedirs(SAVE_DIR, exist_ok=True)
    return os.path.join(SAVE_DIR, name + ".txt")


def save_character(character):
    """Save character to a file. Return True on success."""
    name = character.get("name")
    if not name:
        raise CharacterError("Character must have a name to save.")

    path = _get_save_path(name)
    try:
        with open(path, "w") as f:
            f.write(str(character) + "\n")
        return True
    except OSError:
        raise DataError("Failed to save character: " + name)


def load_character(name):
    """Load character by name; raise CharacterNotFoundError if missing."""
    path = _get_save_path(name)
    if not os.path.exists(path):
        raise CharacterNotFoundError("No saved character named '" + name + "'")

    try:
        with open(path, "r") as f:
            text = f.read().strip()
        character = eval(text)
        return character
    except OSError:
        raise DataError("Failed to read character file for '" + name + "'")


def delete_character(name):
    """Delete a saved character file."""
    path = _get_save_path(name)
    if not os.path.exists(path):
        raise CharacterNotFoundError("No saved character named '" + name + "'")
    os.remove(path)
    return True


def gain_experience(character, amount):
    """Add XP and level up when crossing thresholds.

    Raises CharacterDeadError if health == 0.
    """
    if character.get("health", 0) <= 0:
        raise CharacterDeadError("Cannot gain experience while dead.")

    if amount < 0:
        raise CharacterError("Experience amount cannot be negative.")

    xp = character.get("experience")
