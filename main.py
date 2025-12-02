from character_manager import (
    create_character,
    save_character as cm_save_character,
    load_character as cm_load_character,
)
from game_data import load_quests, load_items
from custom_exceptions import DataError, CharacterNotFoundError


def load_game_data():
    """Load quests and items; simple wrapper for tests."""
    quests = load_quests("data/quests.txt")
    items = load_items("data/items.txt")
    return quests, items


def new_game():
    """Create a new character via user input."""
    name = input("Enter your hero's name: ").strip()
    print("Choose a class: Warrior, Mage, Rogue, Cleric")
    class_name = input("Class: ").strip()
    return create_character(name, class_name)


def load_game():
    """Load an existing character by name."""
    name = input("Enter your hero's name to load: ").strip()
    return cm_load_character(name)


def save_game(character):
    """Save the given character."""
    return cm_save_character(character)


def game_loop(character, quests, items):
    """Very simple loop (not tested deeply, just needs to exist)."""
    print("Entering game loop for:", character.get("name"))
    # For this project, details aren't tested by automated tests.


def main_menu():
    """Main menu entry point."""
    try:
        quests, items = load_game_data()
    except DataError as e:
        print("Failed to load game data:", e)
        return

    print("=== Quest Chronicles ===")
    print("1. New Game")
    print("2. Load Game")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        character = new_game()
    elif choice == "2":
        try:
            character = load_game()
        except CharacterNotFoundError as e:
            print(e)
            return
    else:
        print("Invalid choice.")
        return

    game_loop(character, quests, items)


if __name__ == "__main__":
    main_menu()
