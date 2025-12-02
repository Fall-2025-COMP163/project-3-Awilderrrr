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
        raise QuestRequirementsNotMetError("Prerequisite not met for quest: " + ques
