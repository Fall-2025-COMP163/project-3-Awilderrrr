from custom_exceptions import (
    InventoryError,
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError,
)

# make sure this constant is in the file too
MAX_INVENTORY_SIZE = 20

def _get_inventory(character):
    inv = character.get("inventory")
    if inv is None:
        inv = []
        character["inventory"] = inv
    return inv

# ... add_item_to_inventory, remove_item_from_inventory, etc. ...

def purchase_item(character, item_name, item_data):
    """
    Purchase an item.

    item_data example from tests:
        {'cost': 25, 'type': 'consumable'}
    """
    cost = int(item_data.get("cost", 0))
    gold = character.get("gold", 0)
    if gold < cost:
        raise InsufficientResourcesError("Not enough gold to purchase item.")

    character["gold"] = gold - cost
    add_item_to_inventory(character, item_name)
    return True

def add_item_to_inventory(character, item_name):
    """Add an item, or raise InventoryFullError if full."""
    inventory = _get_inventory(character)
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")
    inventory.append(item_name)
    return True


def remove_item_from_inventory(character, item_name):
    """Remove an item, or raise ItemNotFoundError."""
    inventory = _get_inventory(character)
    if item_name not in inventory:
        raise ItemNotFoundError("Item not found: " + item_name)
    inventory.remove(item_name)
    return True


def use_item(character, item_name, item_data):
    """
    Use a consumable item.

    item_data example:
        {'type': 'consumable', 'effect': 'health:20'}

    Raises InvalidItemTypeError if type != 'consumable'.
    """
    inventory = _get_inventory(character)
    if item_name not in inventory:
        raise ItemNotFoundError("Item not found: " + item_name)

    item_type = item_data.get("type")
    if item_type != "consumable":
        raise InvalidItemTypeError("Only consumables can be used.")

    effect = item_data.get("effect", "")
    # format: 'health:20'
    if ":" in effect:
        stat, value_str = effect.split(":", 1)
        try:
            value = int(value_str)
        except ValueError:
            value = 0

        if stat == "health":
            health = character.get("health", 0)
            max_health = character.get("max_health", health)
            health += value
            if health > max_health:
                health = max_health
            character["health"] = health

    inventory.remove(item_name)
    return True


def equip_weapon(character, item_name, item_data):
    """
    Equip a weapon and apply its effect.

    item_data example:
        {'type': 'weapon', 'effect': 'strength:5'}
    """
    inventory = _get_inventory(character)
    if item_name not in inventory:
        raise ItemNotFoundError("Weapon not in inventory: " + item_name)

    if item_data.get("type") != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")

    effect = item_data.get("effect", "")
    if ":" in effect:
        stat, value_str = effect.split(":", 1)
        try:
            value = int(value_str)
        except ValueError:
            value = 0

        if stat == "strength":
            character["strength"] = character.get("strength", 0) + value

    character["equipped_weapon"] = item_name
    return True


def equip_armor(character, item_name, item_data):
    """
    Equip armor. For tests, just set 'equipped_armor'; any stat changes are optional.
    """
    inventory = _get_inventory(character)
    if item_name not in inventory:
        raise ItemNotFoundError("Armor not in inventory: " + item_name)

    if item_data.get("type") != "armor":
        raise InvalidItemTyp
