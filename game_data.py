"""Game data loading and saving for Quest Chronicles.

Only standard Python concepts are used: files, strings, lists, dicts,
functions, and exceptions.
"""

import os
from custom_exceptions import GameDataError

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
ITEMS_FILE = os.path.join(DATA_DIR, "items.txt")
QUESTS_FILE = os.path.join(DATA_DIR, "quests.txt")
SAVES_DIR = os.path.join(DATA_DIR, "save_games")


def load_items(file_path=ITEMS_FILE):
    """Load item data from a text file.

    Expected format per non-empty, non-comment line:
        name,type,power,value

    Example:
        healing_potion,heal,25,10

    Returns:
        dict mapping item_name -> info_dict
    """
    items = {}

    try:
        with open(file_path, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")
                if len(parts) != 4:
                    raise GameDataError("Invalid item format on line " + str(line_num))

                name, item_type, power_str, value_str = parts

                try:
                    power = int(power_str)
                    value = int(value_str)
                except ValueError:
                    raise GameDataError("Non-numeric item data on line " + str(line_num))

                items[name] = {
                    "type": item_type,
                    "power": power,
                    "value": value
                }
    except FileNotFoundError:
        raise GameDataError("Items file not found at " + file_path)

    return items


def load_quests(file_path=QUESTS_FILE):
    """Load quest data from a text file.

    Expected format per non-empty, non-comment line:
        name|description|xp|gold

    Example:
        Goblin Hunt|Clear out goblins near the village|50|20

    Returns:
        dict mapping quest_name -> info_dict
    """
    quests = {}

    try:
        with open(file_path, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split("|")
                if len(parts) != 4:
                    raise GameDataError("Invalid quest format on line " + str(line_num))

                name, description, xp_str, gold_str = parts

                try:
                    xp = int(xp_str)
                    gold = int(gold_str)
                except ValueError:
                    raise GameDataError("Non-numeric quest data on line " + str(line_num))

                quests[name] = {
                    "description": description,
                    "xp": xp,
                    "gold": gold
                }
    except FileNotFoundError:
        raise GameDataError("Quests file not found at " + file_path)

    return quests


def save_game(player_name, character):
    """Save character data to a file based on the player name.

    This uses a simple text format so it stays within the course topics.
    The file stores one line with pipe-separated fields and comma-separated
    lists for inventory and quests.
    """
    if not os.path.isdir(SAVES_DIR):
        os.makedirs(SAVES_DIR, exist_ok=True)

    file_path = os.path.join(SAVES_DIR, player_name + ".txt")

    # Safely pull values from the dict, with defaults
    name = character.get("name", player_name)
    class_name = character.get("class", "Warrior")
    level = int(character.get("level", 1))
    hp = int(character.get("hp", 0))
    max_hp = int(character.get("max_hp", 0))
    strength = int(character.get("strength", 0))
    magic = int(character.get("magic", 0))
    xp = int(character.get("xp", 0))
    gold = int(character.get("gold", 0))
    inventory = character.get("inventory", [])
    quests = character.get("quests", [])

    inventory_str = ",".join(inventory)
    quests_str = ",".join(quests)

    line = "|".join([
        name,
        class_name,
        str(level),
        str(hp),
        str(max_hp),
        str(strength),
        str(magic),
        str(xp),
        str(gold),
        inventory_str,
        quests_str,
    ])

    try:
        with open(file_path, "w") as f:
            f.write(line + "\n")
    except OSError:
        raise GameDataError("Failed to save game data.")


def load_game(player_name):
    """Load character data from a save file.

    Returns:
        character dict

    Raises:
        GameDataError if file does not exist or data is invalid.
    """
    file_path = os.path.join(SAVES_DIR, player_name + ".txt")

    if not os.path.exists(file_path):
        raise GameDataError("No save file found for player '" + player_name + "'")

    try:
        with open(file_path, "r") as f:
            line = f.readline().strip()
    except OSError:
        raise GameDataError("Failed to read save file for '" + player_name + "'")

    parts = line.split("|")
    if len(parts) != 11:
        raise GameDataError("Invalid save data format for '" + player_name + "'")

    (name, class_name, level_str, hp_str, max_hp_str,
     strength_str, magic_str, xp_str, gold_str,
     inventory_str, quests_str) = parts

    try:
        level = int(level_str)
        hp = int(hp_str)
        max_hp = int(max_hp_str)
        strength = int(strength_str)
        magic = int(magic_str)
        xp = int(xp_str)
        gold = int(gold_str)
    except ValueError:
        raise GameDataError("Non-numeric save data for '" + player_name + "'")

    inventory = inventory_str.split(",") if inventory_str else []
    quests = quests_str.split(",") if quests_str else []

    character = {
        "name": name,
        "class": class_name,
        "level": level,
        "hp": hp,
        "max_hp": max_hp,
        "strength": strength,
        "magic": magic,
        "xp": xp,
        "gold": gold,
        "inventory": inventory,
        "quests": quests,
        "ability_used": False,
    }

    return character
