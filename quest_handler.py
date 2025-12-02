from custom_exceptions import (
    QuestError,
    QuestNotFoundError,
    InsufficientLevelError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
)


def _ensure_quest_lists(character):
    if "active_quests" not in character:
        character["active_quests"] = []
    if "completed_quests" not in character:
        character["completed_quests"] = []
    return character["active_quests"], character["completed_quests"]


def accept_quest(character, quest_id, quests):
    if quest_id not in quests:
        raise QuestNotFoundError("Quest not found: " + quest_id)

    active, completed = _ensure_quest_lists(character)
    quest = quests[quest_id]

    required_level = quest.get("required_level", 1)
    if character.get("level", 1) < required_level:
        raise InsufficientLevelError("Level too low for quest: " + quest_id)

    prereq = quest.get("prerequisite", "NONE")
    if prereq not in ("NONE", "None", "", None) and prereq not in completed:
        raise QuestRequirementsNotMetError("Prerequisite not met for quest: " + quest_id)

    if quest_id in completed:
        raise QuestAlreadyCompletedError("Quest already completed: " + quest_id)

    if quest_id not in active:
        active.append(quest_id)


def complete_quest(character, quest_id, quests):
    active, completed = _ensure_quest_lists(character)
    if quest_id not in active:
        raise QuestNotActiveError("Quest is not active: " + quest_id)

    if quest_id not in quests:
        raise QuestNotFoundError("Quest not found: " + quest_id)

    quest = quests[quest_id]
    active.remove(quest_id)
    if quest_id not in completed:
        completed.append(quest_id)


    xp = quest.get("reward_xp", 0)
    gold = quest.get("reward_gold", 0)
    character["experience"] = character.get("experience", 0) + xp
    character["gold"] = character.get("gold", 0) + gold
    return True


def abandon_quest(character, quest_id):
    active, _ = _ensure_quest_lists(character)
    if quest_id not in active:
        raise QuestNotActiveError("Quest is not active: " + quest_id)
    active.remove(quest_id)


def get_active_quests(character):
    active, _ = _ensure_quest_lists(character)
    return list(active)


def get_available_quests(character, quests):
    active, completed = _ensure_quest_lists(character)
    available = []
    for quest_id in quests.keys():
        if quest_id not in active and quest_id not in completed:
            available.append(quest_id)
    return available
