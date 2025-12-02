"""
Custom exception classes for Quest Chronicles.
"""


class GameError(Exception):
    """Base class for all game-related errors."""
    pass


# ---------------- DATA ----------------

class DataError(GameError):
    """Errors related to game data (files, formats)."""
    pass


class InvalidDataFormatError(DataError):
    """Raised when data in a file doesn't match the expected format."""
    pass


class MissingDataFileError(DataError):
    """Raised when a required data file cannot be found."""
    pass


# ---------------- CHARACTER ----------------

class CharacterError(GameError):
    """Errors related to character operations."""
    pass


class InvalidCharacterClassError(CharacterError):
    """Raised when trying to create a character with an invalid class."""
    pass


class CharacterNotFoundError(CharacterError):
    """Raised when a saved character cannot be found."""
    pass


class CharacterDeadError(CharacterError):
    """Raised when performing character actions while dead."""
    pass


# ---------------- INVENTORY ----------------

class InventoryError(GameError):
    """Errors related to inventory operations."""
    pass


class InventoryFullError(InventoryError):
    """Raised when trying to add an item to a full inventory."""
    pass


class ItemNotFoundError(InventoryError):
    """Raised when trying to access/remove an item that is not present."""
    pass


class InsufficientResourcesError(InventoryError):
    """Raised when the player does not have enough gold/resources."""
    pass


class InvalidItemTypeError(InventoryError):
    """Raised when using or equipping an item in an invalid way."""
    pass


# ---------------- QUESTS ----------------

class QuestError(GameError):
    """Errors related to quests."""
    pass


class QuestNotFoundError(QuestError):
    """Raised when a quest id cannot be found in quest data."""
    pass


class InsufficientLevelError(QuestError):
    """Raised when the character's level is too low for a quest."""
    pass


class QuestRequirementsNotMetError(QuestError):
    """Raised when quest prerequisites are not met."""
    pass


class QuestAlreadyCompletedError(QuestError):
    """Raised when trying to accept a quest already completed."""
    pass


class QuestNotActiveError(QuestError):
    """Raised when trying to complete/abandon a quest that is not active."""
    pass


# ---------------- COMBAT ----------------

class CombatError(GameError):
    """Errors related to combat."""
    pass


class InvalidTargetError(CombatError):
    """Raised when creating or attacking an invalid enemy type/target."""
    pass


class CombatNotActiveError(CombatError):
    """Raised when trying to act in combat when it isn't active."""
    pass
