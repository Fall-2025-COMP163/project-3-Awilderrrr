import os
from custom_exceptions import (
    CharacterError,
    InvalidCharacterClassError,
    CharacterNotFoundError,
    CharacterDeadError,
    DataError,
)

SAVE_DIR = os.path.join(os.path.dirname(__file__), "data", "save_games")

def add_gold(character, amount):
    # Add or subtract gold.

    #Raises ValueError if the resulting gold would be negative.

    gold = character.get("gold", 0) + amount
    if gold < 0:
        raise ValueError("Not enough gold.")
    character["gold"] = gold


# Base stats for required classes
CLASS_STATS = {
    "Warrior": {"max_health": 120, "strength": 15, "magic": 3},
    "Mage": {"max_health": 80, "strength": 4, "magic": 18},
    "Rogue": {"max_health": 100, "strength": 12, "magic": 6},
    "Cleric": {"max_health": 90, "strength": 8, "magic": 12},
}


def create_character(name, class_name):
    # Create and return a new character dictionary.
    if class_name not in CLASS_STATS:
        raise InvalidCharacterClassError("Invalid class: " + class_name)

    stats = CLASS_STATS[class_name]

    return {
        "name": name,
        "class": class_name,
        "level": 1,
        "experience": 0,
        "health": stats["max_health"],
        "max_health": stats["max_health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
    }


def _get_save_path(name):
    if not os.path.isdir(SAVE_DIR):
        os.makedirs(SAVE_DIR, exist_ok=True)
    return os.path.join(SAVE_DIR, name + ".txt")


def save_character(character):
    # Save character to a file. Return True on success.
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
    # Load character by name raise CharacterNotFoundError if missing.
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
    # Delete a saved character file.
    path = _get_save_path(name)
    if not os.path.exists(path):
        raise CharacterNotFoundError("No saved character named '" + name + "'")
    os.remove(path)
    return True


def gain_experience(character, amount):
    # Add XP, level up if needed, restore full health on level up.
    if character.get("health", 0) <= 0:
        raise CharacterDeadError("Dead characters cannot gain XP.")

    if amount < 0:
        raise CharacterError("XP amount cannot be negative.")


    xp_before = character.get("experience", 0)
    xp_after = xp_before + amount

    if xp_after >= 100:
        # Level up once
        xp_after -= 100
        character["level"] += 1
        character["max_health"] += 10
        character["health"] = character["max_health"]

    character["experience"] = xp_after
    return True

def heal_character(character, amount):
    # Heal character up to max_health.
    if amount < 0:
        raise CharacterError("Heal amount cannot be negative.")

    health = character.get("health", 0) + amount
    max_h = character.get("max_health", 0)
    character["health"] = min(health, max_h)
    return True

