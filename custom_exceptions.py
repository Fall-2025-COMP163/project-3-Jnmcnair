"""
COMP 163 - Project 3: Quest Chronicles
Custom Exception Definitions

This module defines all custom exceptions used throughout the game.
"""

# ============================================================================
# BASE GAME EXCEPTIONS
# ============================================================================

class GameError(Exception):
    """Base exception for all game-related errors"""
    pass

class DataError(GameError):
    """Base exception for data-related errors"""
    pass

class CharacterError(GameError):
    """Base exception for character-related errors"""
    pass

class CombatError(GameError):
    """Base exception for combat-related errors"""
    pass

class QuestError(GameError):
    """Base exception for quest-related errors"""
    pass

class InventoryError(GameError):
    """Base exception for inventory-related errors"""
    pass

# ============================================================================
# SPECIFIC EXCEPTIONS
# ============================================================================

# Data Loading Exceptions
class InvalidDataFormatError(DataError):
    """Raised when data file has incorrect format"""
    def __init__(self, filename, expected_format=""):
        super().__init__(f"Data file '{filename}' has an invalid format. {expected_format}")

class MissingDataFileError(DataError):
    """Raised when required data file is not found"""
    def __init__(self, filename):
        super().__init__(f"Required data file '{filename}' not found.")

class CorruptedDataError(DataError):
    """Raised when data file is corrupted or unreadable"""
    def __init__(self, filename):
        super().__init__(f"Data file '{filename}' is corrupted or unreadable.")

# Character Exceptions
class InvalidCharacterClassError(CharacterError):
    """Raised when an invalid character class is specified"""
    def __init__(self, class_name, valid_classes):
        valid_list = ", ".join(valid_classes)
        super().__init__(f"Invalid character class '{class_name}'. Must be one of: {valid_list}")

class CharacterNotFoundError(CharacterError):
    """Raised when trying to load a character that doesn't exist"""
    def __init__(self, name_or_id):
        super().__init__(f"Character '{name_or_id}' could not be found.")

class CharacterDeadError(CharacterError):
    """Raised when trying to perform actions with a dead character"""
    def __init__(self, character_name):
        super().__init__(f"Action failed. The character '{character_name}' is currently defeated (HP <= 0).")

class InsufficientLevelError(CharacterError):
    """Raised when character level is too low for an action"""
    def __init__(self, required_level, current_level):
        super().__init__(f"Insufficient level (Lvl {current_level}). Requires level {required_level} to perform this action.")

# Combat Exceptions
class InvalidTargetError(CombatError):
    """Raised when trying to target an invalid enemy"""
    def __init__(self, target_name, available_targets=None):
        msg = f"Invalid target '{target_name}'."
        if available_targets:
            msg += f" Available targets are: {', '.join(available_targets)}."
        super().__init__(msg)

class CombatNotActiveError(CombatError):
    """Raised when trying to perform combat actions outside of battle"""
    def __init__(self):
        super().__init__("Combat is not currently active.")

class AbilityOnCooldownError(CombatError):
    """Raised when trying to use an ability that's on cooldown"""
    def __init__(self, ability_name):
        super().__init__(f"Ability '{ability_name}' is currently on cooldown.")

# Quest Exceptions
class QuestNotFoundError(QuestError):
    """Raised when trying to access a quest that doesn't exist"""
    def __init__(self, quest_id):
        super().__init__(f"Quest with ID '{quest_id}' could not be found.")

class QuestRequirementsNotMetError(QuestError):
    """Raised when trying to start a quest without meeting requirements"""
    def __init__(self, quest_id, reason="requirements not met"):
        super().__init__(f"Cannot start Quest '{quest_id}': {reason}.")

class QuestAlreadyCompletedError(QuestError):
    """Raised when trying to accept an already completed quest"""
    def __init__(self, quest_id):
        super().__init__(f"Quest '{quest_id}' is already completed.")

class QuestNotActiveError(QuestError):
    """Raised when trying to complete a quest that isn't active"""
    def __init__(self, quest_id):
        super().__init__(f"Quest '{quest_id}' is not currently active.")

# Inventory Exceptions
class InventoryFullError(InventoryError):
    """Raised when trying to add items to a full inventory"""
    def __init__(self):
        super().__init__("Inventory is full. Cannot add new items.")

class ItemNotFoundError(InventoryError):
    """Raised when trying to use an item that doesn't exist"""
    def __init__(self, item_name):
        super().__init__(f"Item '{item_name}' not found in inventory.")

class InsufficientResourcesError(InventoryError):
    """Raised when player doesn't have enough gold or items"""
    def __init__(self, resource_name, needed, owned):
        super().__init__(f"Insufficient {resource_name}. Needed: {needed}, Owned: {owned}.")

class InvalidItemTypeError(InventoryError):
    """Raised when item type is not recognized"""
    def __init__(self, item_type):
        super().__init__(f"Item type '{item_type}' is not recognized or supported.")

# Save/Load Exceptions
class SaveFileCorruptedError(GameError):
    """Raised when save file cannot be loaded due to corruption"""
    def __init__(self, filename):
        super().__init__(f"Save file '{filename}' is corrupted and cannot be loaded.")

class InvalidSaveDataError(GameError):
    """Raised when save file contains invalid data"""
    def __init__(self, filename, detail="unknown error"):
        super().__init__(f"Save file '{filename}' contains invalid data: {detail}.")