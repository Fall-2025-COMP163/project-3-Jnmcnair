"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
import math
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    
    BASE_STATS = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }
    if character_class not in BASE_STATS:
        raise InvalidCharacterClassError(character_class)
    stats = BASE_STATS[character_class]
    character_data = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }
    return character_data

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    
    try:
        os.makedirs(save_directory, exist_ok=True)
    except OSError as e:
        # Catch OSError which covers many file system issues including PermissionError
        print(f"Error creating directory '{save_directory}': {e}")
        # Re-raise the error to let the caller handle it
        raise
    
    character_name = character.get("name", "unknown_character")
    filename = f"{character_name}_save.txt"
    full_path = os.path.join(save_directory, filename)
    
    save_lines = []
    KEY_ORDER = [
        "name", "class", "level", "health", "max_health", 
        "strength", "magic", "experience", "gold", 
        "inventory", "active_quests", "completed_quests"
    ]
    
    for key in KEY_ORDER:
        value = character.get(key)
        if isinstance(value, list):
            formatted_value = ",".join(map(str, value))
        else:
            # All other types (int, str) are converted to string
            formatted_value = str(value)
            
        save_lines.append(f"{key.upper()}: {formatted_value}")
        
    # 3. Write the data to the file
    try:
        with open(full_path, 'w') as f:
            f.write("\n".join(save_lines))
        
        return True
        
    except IOError as e:
        # Catch errors during file writing/closing
        print(f"Error writing file '{full_path}': {e}")
        # Re-raise the error
        raise
    

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    filename = f"{character_name}_save.txt"
    full_path = os.path.join(save_directory, filename)
    
    if not os.path.exists(full_path):
        raise CharacterNotFoundError(character_name, full_path)
        
    character_data = {}
    
    try:
        with open(full_path, 'r') as f:
            lines = f.readlines()
            
    except IOError as e:
        raise SaveFileCorruptedError(full_path, original_error=e)
        
    LIST_KEYS = ["inventory", "active_quests", "completed_quests"]
    INT_KEYS = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]

    # 3. Parse and Validate data format -> InvalidSaveDataError
    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ":" not in line:
                raise InvalidSaveDataError(full_path, key_error="Malformed line (missing colon)")

            key_str, value_str = line.split(":", 1)
            key = key_str.strip().lower() # Normalize key to lowercase
            value = value_str.strip()
            
            if key in LIST_KEYS:
                # Parse lists from comma-separated string
                # Handles empty lists (i.e., "INVENTORY: ") -> []
                character_data[key] = [item.strip() for item in value.split(',') if item.strip()]
                
            elif key in INT_KEYS:
                # Convert numeric values back to integers
                character_data[key] = int(value)
                
            else:
                # Default: name and class are strings
                character_data[key] = value
                
    except (ValueError, IndexError) as e:
        # Catch errors from int() conversion or list parsing
        raise InvalidSaveDataError(full_path, key_error=f"Type conversion or parsing error: {e}")

    # Final check for required keys 
    REQUIRED_KEYS = ["name", "class", "health", "gold"] # Check a subset of critical keys
    for req_key in REQUIRED_KEYS:
        if req_key not in character_data:
            raise InvalidSaveDataError(full_path, key_error=f"Missing required key: {req_key}")

    return character_data
    

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    character_names = []
    SUFFIX = "_save.txt"
    
    # Return empty list if directory doesn't exist
    if not os.path.isdir(save_directory):
        return []
        
    try:
        # Get list of all files in the directory
        filenames = os.listdir(save_directory)
        
        # Filter files and extract character names
        for filename in filenames:
            # Check if the file ends with the required suffix
            if filename.endswith(SUFFIX):
                # Extract the character name by removing the suffix
                name = filename[:-len(SUFFIX)]
                character_names.append(name)
                
    except OSError as e:
        print(f"Error listing directory contents: {e}")
        return [] # Return empty list on error
        
    return character_names
def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = f"{character_name}_save.txt"
    full_path = os.path.join(save_directory, filename)
    
    if not os.path.exists(full_path):
        raise CharacterNotFoundError(character_name, full_path)
        
    try:
        os.remove(full_path)
        # print(f"Successfully deleted save file for '{character_name}' at: {full_path}")
        return True
        
    except OSError as e:
        # Catch potential file system errors (e.g., permissions) that prevent deletion
        print(f"Error deleting file '{full_path}': {e}")
        raise
# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
   # 1. Check if character is dead first
    if character["health"] <= 0:
        raise CharacterDeadError(character["name"])
        
    # 2. Add experience
    character["experience"] += xp_amount
    
    print(f"{character['name']} gained {xp_amount} XP. Total XP: {character['experience']}")
    
    # Check for level up (can level up multiple times)
    while True:
        current_level = character["level"]
        
        # Level up formula: level_up_xp = current_level * 100
        xp_needed_for_next_level = current_level * 100
        
        if character["experience"] >= xp_needed_for_next_level:
            
            # Update stats on level up
            character["level"] += 1
            character["max_health"] += 10
            character["strength"] += 2
            character["magic"] += 2
            
            # Restore health to max_health
            character["health"] = character["max_health"]
            
            print(f"🎉 {character['name']} leveled up! Now Level {character['level']}!")
            print(f"   New Stats: Max Health={character['max_health']}, Str={character['strength']}, Mag={character['magic']}")
            
        else:
            # XP is less than needed for the next level, stop leveling up
            break

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    current_gold = character["gold"]
    new_gold_total = current_gold + amount
    
    # 1. Check that result won't be negative
    if new_gold_total < 0:
        if amount < 0:
            raise ValueError(
                f"Cannot spend buy item. {character['name']} only has {current_gold} gold, "

            )
        else:
            # Should not happen if amount is positive, but catch for safety
            raise ValueError("Gold total cannot be negative.")
            
    # 2. Update character's gold
    character["gold"] = new_gold_total
    
    # Return the new total
    return new_gold_total

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    if amount < 0:
        # A negative healing amount should typically be handled by a 'take_damage' function,
        # but we can treat it as 0 heal here.
        return 0

    current_health = character["health"]
    max_health = character["max_health"]
    
    # Calculate how much healing is actually needed to reach max_health
    needed_heal = max_health - current_health
    
    # Calculate the actual amount of health gained
    actual_heal = min(amount, needed_heal)
    
    # Update character health
    character["health"] += actual_heal
    
    print(f"Healed {character['name']} for {actual_heal}. New health: {character['health']}/{max_health}")
    
    return actual_heal

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    if character["health"] <= 0:
        return True
    return False

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    if not is_character_dead(character):
        print(f"{character['name']} is already alive.")
        return False
        
    max_health = character["max_health"]
    # Calculate 50% of max health, rounding up to prevent 0 health on small max_health values
    revive_health = math.ceil(max_health / 2)
    
    # Restore health to half of max_health
    character["health"] = revive_health
    
    print(f"✨ {character['name']} has been revived! Health restored to {revive_health}.")
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    EXPECTED_FIELDS = {
        "name": str, 
        "class": str, 
        "level": int, 
        "health": int, 
        "max_health": int, 
        "strength": int, 
        "magic": int, 
        "experience": int, 
        "gold": int, 
        "inventory": list,
        "active_quests": list, 
        "completed_quests": list
    }
    
    # 1. Check all required keys exist
    for key in EXPECTED_FIELDS:
        if key not in character:
            raise InvalidSaveDataError(key_error=key)
            
    # 2. Check for correct data types
    for key, expected_type in EXPECTED_FIELDS.items():
        value = character[key]
        
        # Use isinstance check for type validation
        if not isinstance(value, expected_type):
            # Special case: allow float/bool values that could be mistakenly loaded as numbers
            # or strings that look like numbers, but report the type mismatch.
            if key in ["name", "class"] and not value:
                 raise InvalidSaveDataError(type_error=f"{key} (cannot be empty)")
            
            # Allow int/float interchangeability for numbers loaded from string files, but
            # only if the *primary* type check fails. 
            if expected_type is int and not isinstance(value, (int, float)):
                 raise InvalidSaveDataError(type_error=f"{key} (expected int, got {type(value).__name__})")
            
            if expected_type is list and not isinstance(value, list):
                 raise InvalidSaveDataError(type_error=f"{key} (expected list, got {type(value).__name__})")
            
            if expected_type is str and not isinstance(value, str):
                 raise InvalidSaveDataError(type_error=f"{key} (expected str, got {type(value).__name__})")
            
            # Simplified strict type check for all cases
            if not isinstance(value, expected_type):
                 raise InvalidSaveDataError(type_error=f"{key} (expected {expected_type.__name__}, got {type(value).__name__})")

    # If the loop completes without raising an exception, the data is valid.
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")



