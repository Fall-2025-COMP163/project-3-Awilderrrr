"""Inventory and equipment management for Quest Chronicles."""

from custom_exceptions import InventoryError


def add_item(character, item_name, items_db):
    """Add an item to a character's inventory.

    Raises:
        InventoryError if the item is unknown.
    """
    if item_name not in items_db:
        raise InventoryError("Unknown item: " + item_name)
    inventory = character.get("inventory", [])
    inventory.append(item_name)
    character["inventory"] = inventory


def remove_item(character, item_name):
    """Remove an item from a character's inventory.

    Raises:
        InventoryError if the item is not present.
    """
    inventory = character.get("inventory", [])
    if item_name not in inventory:
        raise InventoryError("Item not in inventory: " + item_name)
    inventory.remove(item_name)
    character["inventory"] = inventory


def use_item(character, item_name, items_db):
    """Use an item and apply its effect to the character.

    Currently supports:
        type == "heal": restore HP based on item power.

    Raises:
        InventoryError if the item is not present or unknown.
    """
    inventory = character.get("inventory", [])
    if item_name not in inventory:
        raise InventoryError("Item not in inventory: " + item_name)

    if item_name not in items_db:
        raise InventoryError("Unknown item: " + item_name)

    item = items_db[item_name]
    item_type = item.get("type", "")

    if item_type == "heal":
        power = item.get("power", 0)
        max_hp = character.get("max_hp", 0)
        hp = character.get("hp", 0)
        hp += power
        if hp > max_hp:
            hp = max_hp
        character["hp"] = hp
        print("You use", item_name, "and restore", power, "HP.")
    else:
        # For this functional version, other item types do nothing special yet.
        print("You use", item_name + ". It has no special effect yet.")

    # Remove the item after use.
    inventory.remove(item_name)
    character["inventory"] = inventory


def list_inventory(character):
    """Return a list of item names in the inventory."""
    return list(character.get("inventory", []))
