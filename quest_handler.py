"""Quest system for Quest Chronicles."""

from custom_exceptions import QuestError


def start_quest(character, quest_name, quests_db):
    """Add a quest to the character's active list.

    Raises:
        QuestError if the quest does not exist or is already active.
    """
    if quest_name not in quests_db:
        raise QuestError("Unknown quest: " + quest_name)

    active = character.get("quests", [])
    if quest_name in active:
        raise QuestError("Quest already active: " + quest_name)

    active.append(quest_name)
    character["quests"] = active
    print("Quest started:", quest_name)


def complete_quest(character, quest_name, quests_db):
    """Complete an active quest and grant rewards.

    Raises:
        QuestError if the quest is not active or unknown.
    """
    active = character.get("quests", [])
    if quest_name not in active:
        raise QuestError("Quest not active: " + quest_name)

    if quest_name not in quests_db:
        raise QuestError("Unknown quest: " + quest_name)

    quest = quests_db[quest_name]
    active.remove(quest_name)
    character["quests"] = active

    xp_reward = quest.get("xp", 0)
    gold_reward = quest.get("gold", 0)

    character["xp"] = character.get("xp", 0) + xp_reward
    character["gold"] = character.get("gold", 0) + gold_reward

    print("Quest completed:", quest_name)
    print("You gain", xp_reward, "XP and", gold_reward, "gold.")


def list_active_quests(character, quests_db):
    """Return descriptions of active quests."""
    active = character.get("quests", [])
    descriptions = []
    for q in active:
        if q in quests_db:
            info = quests_db[q]
            line = q + ": " + info.get("description", "No description.")
        else:
            line = q + ": (missing quest data)"
        descriptions.append(line)
    return descriptions
