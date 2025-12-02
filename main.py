"""Main entry point and menu system for Quest Chronicles.."""

from character_manager import create_character, describe_character, level_up
from game_data import load_items, load_quests, save_game, load_game
from inventory_system import add_item, use_item, list_inventory
from quest_handler import start_quest, complete_quest, list_active_quests
from combat_system import battle
from custom_exceptions import (
    GameDataError,
    CharacterCreationError,
    InventoryError,
    QuestError,
    CombatError,
)


def main():
    # Load static game data.
    try:
        items_db = load_items()
        quests_db = load_quests()
    except GameDataError as e:
        print("Error loading game data:", e)
        return

    print("=== Welcome to Quest Chronicles ===")
    name = input("Enter your hero's name: ").strip()
    print("Choose a class: Warrior, Mage, Rogue, Cleric")
    class_name = input("Class: ").strip()

    try:
        character = create_character(name, class_name)
    except CharacterCreationError as e:
        print("Error creating character:", e)
        return

    # Simple demo: give the player one healing potion to start.
    try:
        if "healing_potion" in items_db:
            add_item(character, "healing_potion", items_db)
    except InventoryError:
        # If items_db is different, just ignore this.
        pass

    while True:
        print("\n--- Main Menu ---")
        print("1. View character")
        print("2. View inventory")
        print("3. Start a quest")
        print("4. Complete a quest")
        print("5. Fight an enemy")
        print("6. Use an item")
        print("7. Save game")
        print("8. Load game")
        print("0. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        try:
            if choice == "1":
                print("\n" + describe_character(character))

            elif choice == "2":
                inventory = list_inventory(character)
                if not inventory:
                    print("Your inventory is empty.")
                else:
                    print("Your inventory:")
                    for item_name in inventory:
                        print("-", item_name)

            elif choice == "3":
                quest_name = input("Enter quest name to start: ").strip()
                start_quest(character, quest_name, quests_db)

            elif choice == "4":
                quest_name = input("Enter quest name to complete: ").strip()
                complete_quest(character, quest_name, quests_db)

            elif choice == "5":
                enemy_name = input("Choose enemy (goblin, orc, dragon, slime): ").strip()
                won = battle(character, enemy_name)
                if won:
                    # Tiny, simple XP reward for any win.
                    character["xp"] = character.get("xp", 0) + 20
                    print("You gain 20 XP!")

                    # Example level-up check: 100 XP per level.
                    while character.get("xp", 0) >= character.get("level", 1) * 100:
                        print("You feel stronger! You level up!")
                        level_up(character)
                # If lost, just end battle; player could heal or load game.

            elif choice == "6":
                inventory = list_inventory(character)
                if not inventory:
                    print("You have no items to use.")
                else:
                    print("Your items:")
                    for item_name in inventory:
                        print("-", item_name)
                    item_to_use = input("Enter item name to use: ").strip()
                    use_item(character, item_to_use, items_db)

            elif choice == "7":
                save_game(character.get("name", "player"), character)
                print("Game saved.")

            elif choice == "8":
                loaded = load_game(character.get("name", "player"))
                character = loaded
                print("Game loaded.")

            else:
                print("Invalid choice. Please try again.")

        except (InventoryError, QuestError, CombatError, GameDataError) as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
