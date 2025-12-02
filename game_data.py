"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    quests = {}
    
    # 1. Handle FileNotFoundError -> MissingDataFileError
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        raise MissingDataFileError(filename)
    except Exception as e:
        # Catch other unexpected read errors
        raise CorruptedDataError(filename) from e

    # Define the exact keys expected and their required data types
    EXPECTED_KEYS = {
        "QUEST_ID": str, 
        "TITLE": str, 
        "DESCRIPTION": str, 
        "REWARD_XP": int, 
        "REWARD_GOLD": int, 
        "REQUIRED_LEVEL": int, 
        "PREREQUISITE": str
    }
    
    # Split the content into individual quest blocks (separated by blank lines)
    quest_blocks = [block.strip() for block in content.split('\n\n') if block.strip()]
    
    if not quest_blocks and content.strip():
         # Case where the file is not empty but doesn't conform to block separation
         raise InvalidDataFormatError(filename, "File must contain quest blocks separated by blank lines.")

    # 2. Process each quest block
    for i, block in enumerate(quest_blocks):
        current_quest = {}
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        # Check for minimum number of lines
        if len(lines) != len(EXPECTED_KEYS):
            raise InvalidDataFormatError(
                filename, 
                "Quest block {} is missing fields. Expected {} fields, found {}.".format(i+1, len(EXPECTED_KEYS), len(lines))
            )

        try:
            # Parse key-value pairs
            for line in lines:
                if ':' not in line:
                    raise InvalidDataFormatError(filename, "Line in Quest block {} must contain a 'KEY: VALUE' structure.".format(i+1))
                
                parts = [part.strip() for part in line.split(':', 1)]
                key = parts[0]
                value = parts[1]
                
                if key not in EXPECTED_KEYS:
                     raise InvalidDataFormatError(filename, "Quest block {} contains unexpected key: {}.".format(i+1, key))
                
                # Type conversion and validation
                expected_type = EXPECTED_KEYS[key]
                if expected_type is int:
                    current_quest[key] = int(value)
                else:
                    current_quest[key] = value
                    
        except ValueError:
            # Raised if int(value) fails (corrupted data)
            raise CorruptedDataError(filename)
        except InvalidDataFormatError as e:
            # Re-raise format errors caught inside the loop
            raise e
        except Exception as e:
            # Catch any other unexpected parsing issues
            raise CorruptedDataError(filename) from e
        
        # Final validation and storage
        quest_id = current_quest.get("QUEST_ID")
        if not quest_id:
             raise InvalidDataFormatError(filename, "Quest block {} missing QUEST_ID.".format(i+1))
             
        if quest_id in quests:
             raise InvalidDataFormatError(filename, "Duplicate QUEST_ID found: {}.".format(quest_id))
             
        # Normalize data structure for final output
        quests[quest_id] = {
            "title": current_quest["TITLE"],
            "description": current_quest["DESCRIPTION"],
            "reward_xp": current_quest["REWARD_XP"],
            "reward_gold": current_quest["REWARD_GOLD"],
            "required_level": current_quest["REQUIRED_LEVEL"],
            # Ensure PREREQUISITE is stored as None if "NONE" is explicitly set
            "prerequisite": current_quest["PREREQUISITE"] if current_quest["PREREQUISITE"].upper() != "NONE" else None,
        }

    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    items = {}
    
    # 1. Handle FileNotFoundError -> MissingDataFileError
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        raise MissingDataFileError(filename)
    except Exception as e:
        # Catch other unexpected read errors
        raise CorruptedDataError(filename) from e

    # Define the exact keys expected and their required data processing
    # Key: (Output_Key_Name, Expected_Type, Required_Split_Count_for_EFFECT)
    EXPECTED_KEYS = {
        "ITEM_ID": ("item_id", str, 0),
        "NAME": ("name", str, 0),
        "TYPE": ("type", str, 0),
        "EFFECT": ("effect", str, 2), # Requires special handling (stat:value split)
        "COST": ("cost", int, 0),
        "DESCRIPTION": ("description", str, 0)
    }
    
    VALID_TYPES = {"weapon", "armor", "consumable"}
    
    # Split the content into individual item blocks (separated by blank lines)
    item_blocks = [block.strip() for block in content.split('\n\n') if block.strip()]
    
    if not item_blocks and content.strip():
         raise InvalidDataFormatError(filename, "File must contain item blocks separated by blank lines.")

    # 2. Process each item block
    for i, block in enumerate(item_blocks):
        current_item = {}
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        # Check for minimum number of lines
        if len(lines) != len(EXPECTED_KEYS):
            raise InvalidDataFormatError(
                filename, 
                "Item block {} is missing fields. Expected {} fields, found {}.".format(i+1, len(EXPECTED_KEYS), len(lines))
            )

        try:
            # Parse key-value pairs
            for line in lines:
                if ':' not in line:
                    raise InvalidDataFormatError(filename, "Line in Item block {} must contain a 'KEY: VALUE' structure.".format(i+1))
                
                parts = [part.strip() for part in line.split(':', 1)]
                key = parts[0]
                value = parts[1]
                
                if key not in EXPECTED_KEYS:
                     raise InvalidDataFormatError(filename, "Item block {} contains unexpected key: {}.".format(i+1, key))
                
                output_key, expected_type, split_count = EXPECTED_KEYS[key]
                
                # Type conversion and validation
                if expected_type is int:
                    current_item[output_key] = int(value)
                else:
                    current_item[output_key] = value
                    
        except ValueError:
            # Raised if int(value) fails (corrupted data)
            raise CorruptedDataError(filename)
        except InvalidDataFormatError as e:
            # Re-raise format errors caught inside the loop
            raise e
        except Exception as e:
            # Catch any other unexpected parsing issues
            raise CorruptedDataError(filename) from e
        
        # 3. Final structural and semantic validation
        item_id = current_item.get("item_id")
        
        if not item_id:
             raise InvalidDataFormatError(filename, "Item block {} missing ITEM_ID.".format(i+1))
             
        if item_id in items:
             raise InvalidDataFormatError(filename, "Duplicate ITEM_ID found: {}.".format(item_id))
        
        # Validate TYPE
        item_type = current_item.get("type")
        if item_type not in VALID_TYPES:
             raise InvalidDataFormatError(filename, "Item {} has invalid TYPE: {}. Must be one of {}.".format(item_id, item_type, list(VALID_TYPES)))

        # Validate EFFECT format (stat:value)
        effect_str = current_item.get("effect", "")
        effect_parts = [p.strip() for p in effect_str.split(':', 1)]
        
        if len(effect_parts) != 2:
            raise InvalidDataFormatError(filename, "Item {} has invalid EFFECT format. Expected 'stat:value', got '{}'.".format(item_id, effect_str))
        
        stat_name = effect_parts[0]
        stat_value = effect_parts[1]
        
        try:
            # Convert effect value to integer
            value = int(stat_value)
        except ValueError:
            raise CorruptedDataError(filename, "Item {} effect value '{}' is not a valid integer.".format(item_id, stat_value))
            
        # Store the parsed data
        items[item_id] = {
            "id": current_item["item_id"],
            "name": current_item["name"],
            "type": current_item["type"],
            "effect": {
                "stat": stat_name,
                "value": value
            },
            "cost": current_item["cost"],
            "description": current_item["description"],
        }

    return items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    REQUIRED_FIELDS = {
        "id": str,
        "title": str,
        "description": str,
        "reward_xp": int,
        "reward_gold": int,
        "required_level": int,
        "prerequisite": (str, type(None)) # Prerequisite can be a string or None
    }
    
    quest_id = quest_dict.get('id', 'UNKNOWN_ID') # Get ID for use in error message

    # 2. Check for missing keys
    for key, expected_type in REQUIRED_FIELDS.items():
        if key not in quest_dict:
            raise InvalidDataFormatError(
                f"Quest ID '{quest_id}' is missing the required field: '{key}'."
            )
            
    # 3. Check data types and value integrity
    for key, expected_type in REQUIRED_FIELDS.items():
        value = quest_dict[key]
        
        # Check numeric types (int)
        if expected_type is int:
            if not isinstance(value, int) or value < 0:
                raise InvalidDataFormatError(
                    f"Quest ID '{quest_id}' field '{key}' must be a non-negative integer, but found: {value} ({type(value).__name__})."
                )
        
        # Check prerequisite type (str or None)
        elif key == "prerequisite":
            # expected_type is (str, type(None))
            if not isinstance(value, str) and value is not None:
                raise InvalidDataFormatError(
                    f"Quest ID '{quest_id}' field '{key}' must be a string or None, but found: {value} ({type(value).__name__})."
                )
        
        # Check string types (id, title, description)
        elif expected_type is str:
            if not isinstance(value, str):
                 raise InvalidDataFormatError(
                    f"Quest ID '{quest_id}' field '{key}' must be a string, but found: {type(value).__name__}."
                )

    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    REQUIRED_FIELDS = {
        "id": str,
        "name": str,
        "type": str,
        "effect": dict,  # Expects a dict like {'stat': str, 'value': int}
        "cost": int,
        "description": str
    }
    
    VALID_TYPES = {"weapon", "armor", "consumable"}
    
    item_id = item_dict.get('id', 'UNKNOWN_ID') # Get ID for use in error message

    # 1. Check for missing keys and basic type validation
    for key, expected_type in REQUIRED_FIELDS.items():
        if key not in item_dict:
            raise InvalidDataFormatError(
                f"Item ID '{item_id}' is missing the required field: '{key}'."
            )
        
        value = item_dict[key]
        
        # Check basic type matching (excluding the special 'effect' dict)
        if key != "effect" and not isinstance(value, expected_type):
            raise InvalidDataFormatError(
                f"Item ID '{item_id}' field '{key}' must be of type {expected_type.__name__}, but found: {type(value).__name__}."
            )

    # 2. Validate 'type' field
    item_type = item_dict["type"]
    if item_type not in VALID_TYPES:
        raise InvalidDataFormatError(
            f"Item ID '{item_id}' has an invalid type: '{item_type}'. Must be one of: {', '.join(VALID_TYPES)}."
        )

    # 3. Validate 'cost' field (must be a non-negative integer)
    item_cost = item_dict["cost"]
    if not isinstance(item_cost, int) or item_cost < 0:
        raise InvalidDataFormatError(
            f"Item ID '{item_id}' cost must be a non-negative integer, but found: {item_cost}."
        )

    # 4. Validate 'effect' field structure and types
    item_effect = item_dict["effect"]
    
    if not isinstance(item_effect, dict):
         raise InvalidDataFormatError(
            f"Item ID '{item_id}' effect must be a dictionary, but found: {type(item_effect).__name__}."
        )

    if "stat" not in item_effect or "value" not in item_effect:
        raise InvalidDataFormatError(
            f"Item ID '{item_id}' effect dictionary is missing 'stat' or 'value' keys."
        )
    
    effect_stat = item_effect["stat"]
    effect_value = item_effect["value"]
    
    if not isinstance(effect_stat, str) or not effect_stat.strip():
        raise InvalidDataFormatError(
            f"Item ID '{item_id}' effect 'stat' must be a non-empty string."
        )
        
    if not isinstance(effect_value, int):
        # NOTE: Allow value to be negative or positive
        raise InvalidDataFormatError(
            f"Item ID '{item_id}' effect 'value' must be an integer, but found: {type(effect_value).__name__}."
        )
        
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    DATA_DIR = "data"
    
    # 1. Create data/ directory if it doesn't exist
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            print(f"Directory '{DATA_DIR}' created.")
    except PermissionError:
        print(f"Error: **Permission denied** when creating directory '{DATA_DIR}'. Check file permissions.")
        return
    except OSError as e:
        # Catch other unexpected OS errors
        print(f"An unexpected OS error occurred while creating directory '{DATA_DIR}': {e}")
        return
            
    # Define default content for files
    DEFAULT_QUESTS_CONTENT = """
QUEST_ID: tutorial_start
TITLE: A Fresh Start
DESCRIPTION: Speak to the village elder to begin your adventure.
REWARD_XP: 10
REWARD_GOLD: 5
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

QUEST_ID: first_hunt
TITLE: The Goblin Problem
DESCRIPTION: Defeat 1 Goblin near the forest entrance.
REWARD_XP: 50
REWARD_GOLD: 20
REQUIRED_LEVEL: 2
PREREQUISITE: tutorial_start
"""

    DEFAULT_ITEMS_CONTENT = """
ITEM_ID: wood_sword
NAME: Wooden Sword
TYPE: weapon
EFFECT: strength:2
COST: 50
DESCRIPTION: A simple, sturdy sword for beginners.

ITEM_ID: leather_armor
NAME: Leather Vest
TYPE: armor
EFFECT: defense:3
COST: 75
DESCRIPTION: Light and flexible protective gear.

ITEM_ID: basic_potion
NAME: Health Potion
TYPE: consumable
EFFECT: health:20
COST: 25
DESCRIPTION: Restores a small amount of health instantly.
"""

    files_to_create = {
        os.path.join(DATA_DIR, "quests.txt"): DEFAULT_QUESTS_CONTENT,
        os.path.join(DATA_DIR, "items.txt"): DEFAULT_ITEMS_CONTENT
    }

    # 2. Create default files if they don't exist
    for filename, content in files_to_create.items():
        if not os.path.exists(filename):
            try:
                with open(filename, 'w') as f:
                    # Write the content, stripping leading/trailing whitespace
                    f.write(content.strip())
                print(f"Default file '{filename}' created.")
            except IOError as e:
                # Catch general file writing errors (including permissions)
                print(f"Error: Could not write to file '{filename}'. Check permissions. Details: {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    REQUIRED_KEYS = {
        "QUEST_ID": str, 
        "TITLE": str, 
        "DESCRIPTION": str, 
        "REWARD_XP": int, 
        "REWARD_GOLD": int, 
        "REQUIRED_LEVEL": int, 
        "PREREQUISITE": str
    }
    
    quest_data = {}
    
    if len(lines) != len(REQUIRED_KEYS):
        raise InvalidDataFormatError(
            f"Quest block expected {len(REQUIRED_KEYS)} lines, found {len(lines)}."
        )

    for line in lines:
        try:
            # Split each line on the first ": " to get key-value pairs
            key, value_str = [p.strip() for p in line.split(':', 1)]
        except ValueError:
            raise InvalidDataFormatError(f"Line must contain 'KEY: VALUE' structure: '{line}'")

        if key not in REQUIRED_KEYS:
            raise InvalidDataFormatError(f"Unexpected key found: '{key}'")
        
        expected_type = REQUIRED_KEYS[key]
        
        try:
            # Convert numeric strings to integers
            if expected_type is int:
                value = int(value_str)
            else:
                value = value_str
        except ValueError:
            raise InvalidDataFormatError(f"Value for '{key}' must be an integer: '{value_str}'")

        quest_data[key] = value

    # Final normalization of keys and prerequisite handling
    final_data = {
        "id": quest_data["QUEST_ID"],
        "title": quest_data["TITLE"],
        "description": quest_data["DESCRIPTION"],
        "reward_xp": quest_data["REWARD_XP"],
        "reward_gold": quest_data["REWARD_GOLD"],
        "required_level": quest_data["REQUIRED_LEVEL"],
        # Prerequisite is None if the string is "NONE"
        "prerequisite": quest_data["PREREQUISITE"] if quest_data["PREREQUISITE"].upper() != "NONE" else None,
    }
    
    return final_data

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    REQUIRED_KEYS = {
        "ITEM_ID": str, 
        "NAME": str, 
        "TYPE": str, 
        "EFFECT": str, # Will be parsed into a dict later
        "COST": int, 
        "DESCRIPTION": str
    }
    VALID_TYPES = {"weapon", "armor", "consumable"}
    
    item_data = {}
    
    if len(lines) != len(REQUIRED_KEYS):
        raise InvalidDataFormatError(
            f"Item block expected {len(REQUIRED_KEYS)} lines, found {len(lines)}."
        )

    for line in lines:
        try:
            # Split each line on the first ": "
            key, value_str = [p.strip() for p in line.split(':', 1)]
        except ValueError:
            raise InvalidDataFormatError(f"Line must contain 'KEY: VALUE' structure: '{line}'")

        if key not in REQUIRED_KEYS:
            raise InvalidDataFormatError(f"Unexpected key found: '{key}'")
        
        expected_type = REQUIRED_KEYS[key]
        
        try:
            # Convert COST to integer
            if key == "COST":
                value = int(value_str)
            else:
                value = value_str
        except ValueError:
            raise InvalidDataFormatError(f"Value for '{key}' must be an integer: '{value_str}'")

        item_data[key] = value
        
    # Validation and Final Normalization
    
    # 1. Validate TYPE
    item_type = item_data.get("TYPE", "")
    if item_type not in VALID_TYPES:
        raise InvalidDataFormatError(f"Invalid item TYPE: '{item_type}'. Must be one of {list(VALID_TYPES)}.")

    # 2. Parse EFFECT (e.g., "strength:5" -> {'stat': 'strength', 'value': 5})
    effect_str = item_data.get("EFFECT", "")
    effect_parts = [p.strip() for p in effect_str.split(':', 1)]
    
    if len(effect_parts) != 2:
        raise InvalidDataFormatError(f"EFFECT format invalid. Expected 'stat:value', got '{effect_str}'.")
    
    stat_name = effect_parts[0]
    
    try:
        stat_value = int(effect_parts[1])
    except ValueError:
        raise InvalidDataFormatError(f"EFFECT value must be an integer: '{effect_parts[1]}'")
        
    # Final data structure
    final_data = {
        "id": item_data["ITEM_ID"],
        "name": item_data["NAME"],
        "type": item_data["TYPE"],
        "effect": {
            "stat": stat_name,
            "value": stat_value
        },
        "cost": item_data["COST"],
        "description": item_data["DESCRIPTION"],
    }
    
    return final_data

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

