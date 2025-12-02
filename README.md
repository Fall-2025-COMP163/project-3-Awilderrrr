# Quest Chronicles

A simple multi-module text RPG built for COMP 163 Project 3.

## Modules

- `main.py`  
  Handles the main menu, user input, and top-level exception handling.

- `game_data.py`  
  Loads items and quests from text files in `data/`, and saves/loads the
  player character to/from `data/save_games/`.

- `character_manager.py`  
  Creates and manages the player character. Supports the four required
  classes: Warrior, Mage, Rogue, Cleric. Also handles level-ups.

- `inventory_system.py`  
  Manages items in the player's inventory and simple item usage
  (healing items).

- `quest_handler.py`  
  Starts and completes quests, granting XP and gold rewards.

- `combat_system.py`  
  Runs a basic turn-based battle between the player and an enemy.
  Required enemies `goblin`, `orc`, and `dragon` are present, plus one
  extra enemy (`slime`). Includes a simple critical hit mechanic and an
  upgraded dragon attack.

- `custom_exceptions.py`  
  Defines custom exception types used by all other modules. If your
  instructor provided this file, use their version instead of this one.

## Exception Strategy

Each subsystem raises a specific custom exception:

- `GameDataError` for problems with files and data.
- `CharacterCreationError` for invalid class choices.
- `InventoryError` for invalid inventory actions.
- `QuestError` for invalid quest actions.
- `CombatError` for invalid enemies or combat issues.

`main.py` catches these exceptions and prints friendly messages instead
of letting the game crash.

## How to Run

From the project folder:

```bash
python main.py
```

Follow the on-screen menu to view your character, manage quests, fight
enemies, and save/load your game.

## AI Usage

AI helped me understand my errors in my code. It helped me debug certain issues in my code that I didn't understand. AI also helped me with organizing my files. 
