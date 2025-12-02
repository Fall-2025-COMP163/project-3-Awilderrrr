"""Combat mechanics for Quest Chronicles.

Functional version with a couple of simple creative additions:
- A fourth enemy type (slime) beyond the required goblin/orc/dragon.
- A deterministic "critical hit" every 3rd player attack that deals double damage.
- Dragon deals double damage every 2nd enemy turn.
"""

from custom_exceptions import CombatError

# Required enemies plus one extra.
ENEMIES = {
    "goblin": {"hp": 30, "strength": 5},
    "orc": {"hp": 60, "strength": 10},
    "dragon": {"hp": 120, "strength": 18},
    "slime": {"hp": 40, "strength": 4},  # simple extra enemy
}


def get_enemy(enemy_name):
    """Return a fresh enemy dict for the given name.

    Raises:
        CombatError if the enemy is unknown.
    """
    if enemy_name not in ENEMIES:
        raise CombatError("Unknown enemy: " + enemy_name)

    base = ENEMIES[enemy_name]
    enemy = {
        "name": enemy_name,
        "hp": base["hp"],
        "strength": base["strength"],
    }
    return enemy


def player_attack(character, enemy, turn_number):
    """Perform a player attack on the enemy.

    Every 3rd player attack is a critical hit and deals double strength damage.
    """
    strength = character.get("strength", 0)
    damage = strength

    # Simple deterministic critical hit: every 3rd turn.
    if turn_number % 3 == 0:
        damage = strength * 2
        print("Critical hit! You deal", damage, "damage.")
    else:
        print("You attack and deal", damage, "damage.")

    enemy["hp"] -= damage
    if enemy["hp"] < 0:
        enemy["hp"] = 0

    return damage


def enemy_attack(character, enemy, turn_number):
    """Enemy attacks the character.

    Creative twist:
        Dragon deals double damage every 2nd enemy attack.
    """
    strength = enemy.get("strength", 0)
    damage = strength

    if enemy.get("name") == "dragon" and turn_number % 2 == 0:
        damage = strength * 2
        print("The dragon unleashes a fierce strike for", damage, "damage!")
    else:
        print(enemy.get("name", "Enemy"), "hits you for", damage, "damage.")

    character["hp"] = character.get("hp", 0) - damage
    if character["hp"] < 0:
        character["hp"] = 0

    return damage


def battle(character, enemy_name):
    """Run a simple turn-based battle.

    Returns:
        True if the player wins, False if the player is defeated.

    Raises:
        CombatError for invalid enemy names.
    """
    enemy = get_enemy(enemy_name)

    print("A wild", enemy_name, "appears!")
    player_turn = 1
    enemy_turn = 1

    # Battle loop
    while character.get("hp", 0) > 0 and enemy.get("hp", 0) > 0:
        print("\nYour HP:", character.get("hp", 0))
        print(enemy["name"], "HP:", enemy.get("hp", 0))

        # Player always attacks in this functional version.
        player_attack(character, enemy, player_turn)
        player_turn += 1

        # Check if enemy is defeated.
        if enemy.get("hp", 0) <= 0:
            print("You defeated the", enemy["name"] + "!")
            return True

        # Enemy turn.
        enemy_attack(character, enemy, enemy_turn)
        enemy_turn += 1

        # Check if player is defeated.
        if character.get("hp", 0) <= 0:
            print("You were defeated by the", enemy["name"] + "...")
            return False

    return character.get("hp", 0) > 0
