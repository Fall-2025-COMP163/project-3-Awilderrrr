from custom_exceptions import InvalidTargetError, CombatNotActiveError

ENEMY_TYPES = {
    "goblin": {"name": "Goblin", "health": 30, "xp_reward": 20, "gold_reward": 10},
    "orc": {"name": "Orc", "health": 60, "xp_reward": 40, "gold_reward": 20},
    "dragon": {"name": "Dragon", "health": 150, "xp_reward": 100, "gold_reward": 50},
}


def create_enemy(enemy_type):
    if enemy_type not in ENEMY_TYPES:
        raise InvalidTargetError("Unknown enemy type: " + enemy_type)

    base = ENEMY_TYPES[enemy_type]
    # return a fresh copy
    return {
        "name": base["name"],
        "health": base["health"],
        "xp_reward": base["xp_reward"],
        "gold_reward": base["gold_reward"],
    }


def get_victory_rewards(enemy):
    # Return rewards based on enemy info.
    return {
        "xp": enemy.get("xp_reward", 0),
        "gold": enemy.get("gold_reward", 0),
    }


class SimpleBattle:


    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True

    def start_battle(self):
        # just ensure combat is marked active.
        self.combat_active = True

    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        # Simple damage model player uses strength if present else 10
        damage = self.character.get("strength", 10)
        self.enemy["health"] = max(0, self.enemy.get("health", 0) - damage)
        if self.enemy["health"] <= 0:
            self.combat_active = False

    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")

        # Simple damage model enemy deals 5 damage
        dmg = 5
        self.character["health"] = max(0, self.character.get("health", 0) - dmg)
        if self.character["health"] <= 0:
            self.combat_active = False
