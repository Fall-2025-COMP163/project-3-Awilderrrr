"""Custom exception classes for Quest Chronicles.

NOTE: Your instructor likely provided their own version of this file.
If so, use that one instead of this template. The other modules in this
project expect exceptions with these names.
"""

class GameDataError(Exception):
    """Raised when there is a problem loading or saving game data."""
    pass


class CharacterCreationError(Exception):
    """Raised when creating or loading a character fails."""
    pass


class InventoryError(Exception):
    """Raised when inventory operations fail (missing item, unknown item, etc.)."""
    pass


class QuestError(Exception):
    """Raised when starting or completing a quest fails."""
    pass


class CombatError(Exception):
    """Raised when an error occurs in the combat system."""
    pass
