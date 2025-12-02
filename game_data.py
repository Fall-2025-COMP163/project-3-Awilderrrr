import os
from custom_exceptions import (
    DataError,
    InvalidDataFormatError,
    MissingDataFileError,
)


def load_quests(path="data/quests.txt"):
    """
    Load quests from a file.

    Expected line format (non-empty, not starting with '#'):
        quest_id|title|description|reward_xp|reward_gold|required_level|prerequisite

    Returns:
        dict mapping quest_id -> quest_dict

    Raises:
        MissingDataFileError, InvalidDataFormatError
    """
    if not os.path.exists(path):
        raise MissingDataFileError("Quest file not found: " + path)

    quests = {}
    try:
        with open(path, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split("|")
                if len(parts) != 7:
                    raise InvalidDataFormatError(
                        "Invalid quest format on line " + str(line_num)
                    )

                quest_id, title, desc, xp_str, gold_str, lvl_str, prereq = parts
                try:
                    reward_xp = int(xp_str)
                    reward_gold = int(gold_str)
                    required_level = int(lvl_str)
                except ValueError:
                    raise InvalidDataFormatError(
                        "Non-numeric quest values on line " + str(line_num)
                    )

                quest = {
                    "quest_id": quest_id,
                    "title": title,
                    "description": desc,
                    "reward_xp": reward_xp,
                    "reward_gold": reward_gold,
                    "required_level": required_level,
                    "prerequisite": prereq,
                }
                quests[quest_id] = quest
    except OSError:
        raise DataError("Error reading quest file: " + path)

    return quests


def load_items(path="data/items.txt"):
    """
    Load items from a file.

    Expected line format:
        item_id,name,type,effect,cost,description

    Returns:
        dict mapping item_id -> item_dict

    Raises:
        MissingDataFileError, InvalidDataFormatError
    """
    if not os.path.exists(path):
        raise MissingDataFileError("Item file not found: " + path)

    items = {}
    try:
        with open(path, "r") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")
                if len(parts) != 6:
                    raise InvalidDataFormatError(
                        "Invalid item format on line " + str(line_num)
                    )

                item_id, name, item_type, effect, cost_str, desc = parts
                try:
                    cost = int(cost_str)
                except ValueError:
                    raise InvalidDataFormatError(
                        "Non-numeric item cost on line " + str(line_num)
                    )

                item = {
                    "item_id": item_id,
                    "name": name,
                    "type": item_type,
                    "effect": effect,
                    "cost": cost,
                    "description": desc,
                }
                items[item_id] = item
    except OSError:
        raise DataError("Error reading item file: " + path)

    return items


def validate_quest_data(data):
    """
    Validate quest data.

    The tests pass a *single* quest dict, e.g.:

        {
            'quest_id': 'test',
            'title': 'Test',
            'description': 'Test',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }

    Returns:
        True if valid.

    Raises:
        InvalidDataFormatError otherwise.
    """
    if not isinstance(data, dict):
        raise InvalidDataFormatError("Quest data must be a dict.")

    required_keys = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite",
    ]
    for key in required_keys:
        if key not in data:
            raise InvalidDataFormatError("Quest missing key: " + key)

    try:
        int(data["reward_xp"])
        int(data["reward_gold"])
        int(data["required_level"])
    except (ValueError, TypeError):
        raise InvalidDataFormatError("Quest has non-numeric reward or level.")

    return True


def validate_item_data(data):
    """
    Validate item data.

    The tests pass a single item dict, e.g.:

        {
            'item_id': 'test',
            'name': 'Test',
            'type': 'consumable',
            'effect': 'health:20',
            'cost': 25,
            'description': 'Test'
        }

    Returns:
        True if valid.

    Raises:
        InvalidDataFormatError otherwise.
    """
    if not isinstance(data, dict):
        raise InvalidDataFormatError("Item data must be a dict.")

    required_keys = [
        "item_id",
        "name",
        "type",
        "effect",
        "cost",
        "description",
    ]
    for key in required_keys:
        if key not in data:
            raise InvalidDataFormatError("Item missing key: " + key)

    try:
        int(data["cost"])
    except (ValueError, TypeError):
        raise InvalidDataFormatError("Item cost must be numeric.")

    return True
