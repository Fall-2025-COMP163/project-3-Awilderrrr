"""Character creation and management for Quest Chronicles."""

from custom_exceptions import CharacterCreationError

# Base stats for the four required classes.
CLASSES = {
    "Warrior": {
        "hp": 120,
        "strength": 15,
        "magic": 3,
    },
    "Mage": {
        "hp": 80,
        "strength": 4,
        "magic": 18,
    },
    "Rogue": {
        "hp": 100,
        "strength": 12,
        "magic": 6,
    },
    "Cleric": {
        "hp": 90,
        "strength": 8,
        "magic": 12,
    },
}


def create_character(name, class_name):
    """Create a new character.

    Args:
        name (str): Player's chosen name.
        class_name (str): One of "Warrior", "Mage", "Rogue", "Cleric".

    Returns:
        dict representing the character.

    Raises:
        CharacterCreationError if class_name is invalid.
    """
    if class_name not in CLASSES:
        raise CharacterCreationError("Invalid class: " + class_name)

    base = CLASSES[class_name]

    character = {
        "name": name,
        "class": class_name,
        "level": 1,
        "hp": base["hp"],
        "max_hp": base["hp"],
        "strength": base["strength"],
        "magic": base["magic"],
        "xp": 0,
        "gold": 0,
        "inventory": [],
        "quests": [],
        # used to control some per-battle abilities, reset in combat
        "ability_used": False,
    }
    return character


def level_up(character):
    """Increase a character's level and stats.

    Simple, slightly creative rules:

    Warrior: more HP and strength
    Mage:    more magic and some HP
    Rogue:   more strength and HP
    Cleric:  more magic and HP
    """
    character["level"] += 1
    cls = character.get("class", "Warrior")

    if cls == "Warrior":
        character["max_hp"] += 15
        character["strength"] += 3
    elif cls == "Mage":
        character["max_hp"] += 8
        character["magic"] += 4
    elif cls == "Rogue":
        character["max_hp"] += 10
        character["strength"] += 2
    elif cls == "Cleric":
        character["max_hp"] += 9
        character["magic"] += 3
    else:
        # Fallback, though this should not happen with valid classes.
        character["max_hp"] += 5

    # Heal to full on level up.
    character["hp"] = character["max_hp"]


def describe_character(character):
    """Return a multi-line string describing the character."""
    lines = []
    lines.append("Name: " + character.get("name", "Unknown"))
    lines.append("Class: " + character.get("class", "Unknown"))
    lines.append("Level: " + str(character.get("level", 1)))
    lines.append("HP: " + str(character.get("hp", 0)) + "/" + str(character.get("max_hp", 0)))
    lines.append("Strength: " + str(character.get("strength", 0)))
    lines.append("Magic: " + str(character.get("magic", 0)))
    lines.append("XP: " + str(character.get("xp", 0)))
    lines.append("Gold: " + str(character.get("gold", 0)))
    return "\n".join(lines)
