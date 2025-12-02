import os
from custom_exceptions import (
    DataError,
    InvalidDataFormatError,
    MissingDataFileError,
)


def load_quests(path="data/quests.txt"):

    if not os.path.exists(path):
        raise MissingDataFileError("Quest file not found: " + path)

    quests = {}
    current = {}

    # add processed quest if valid
    def commit_current(line_num):
        if not current:
            return
        required_fields = [
            "QUEST_ID",
            "TITLE",
            "DESCRIPTION",
            "REWARD_XP",
            "REWARD_GOLD",
            "REQUIRED_LEVEL",
            "PREREQUISITE",
        ]

        # Must contain all fields
        if all(k in current for k in required_fields):
            try:
                qid = current["QUEST_ID"]
                quests[qid] = {
                    "quest_id": qid,
                    "title": current["TITLE"],
                    "description": current["DESCRIPTION"],
                    "reward_xp": int(current["REWARD_XP"]),
                    "reward_gold": int(current["REWARD_GOLD"]),
                    "required_level": int(current["REQUIRED_LEVEL"]),
                    "prerequisite": current["PREREQUISITE"],
                }
            except ValueError:

                pass

        # Reset for next block
        current.clear()

    try:
        with open(path, "r") as f:
            for line_num, raw in enumerate(f, start=1):
                line = raw.strip()

                # Blank line = end of block
                if line == "":
                    commit_current(line_num)
                    continue

                if ":" not in line:

                    continue

                key, value = line.split(":", 1)
                key = key.strip().upper()
                value = value.strip()

                current[key] = value


            commit_current(line_num)

    except OSError:
        raise DataError("Error reading quest file: " + path)

    if not quests:
        raise InvalidDataFormatError(
            "No valid quest entries found in: " + path
        )

    return quests



def load_items(path="data/items.txt"):


    if not os.path.exists(path):
        raise MissingDataFileError("Item file not found: " + path)

    items = {}
    current = {}

    def commit_current(line_num):
        # Validate and store current item block if valid then reset.
        if not current:
            return

        required_fields = [
            "ITEM_ID",
            "NAME",
            "TYPE",
            "EFFECT",
            "COST",
            "DESCRIPTION",
        ]

        if all(k in current for k in required_fields):
            try:
                item_id = current["ITEM_ID"]
                items[item_id] = {
                    "item_id": item_id,
                    "name": current["NAME"],
                    "type": current["TYPE"],
                    "effect": current["EFFECT"],
                    "cost": int(current["COST"]),
                    "description": current["DESCRIPTION"],
                }
            except ValueError:
                # bad COST value skip this block
                pass

        current.clear()

    try:
        with open(path, "r") as f:
            for line_num, raw in enumerate(f, start=1):
                line = raw.strip()

                # Blank line end of an item block
                if line == "":
                    commit_current(line_num)
                    continue


                if ":" not in line:

                    continue

                key, value = line.split(":", 1)
                key = key.strip().upper()
                value = value.strip()
                current[key] = value


            commit_current(line_num)

    except OSError:
        raise DataError("Error reading item file: " + path)

    if not items:
        raise InvalidDataFormatError("No valid item data found in: " + path)

    return items


def validate_quest_data(data):

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
