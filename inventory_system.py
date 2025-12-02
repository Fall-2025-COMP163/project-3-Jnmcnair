"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    if 'inventory' not in character:
        character['inventory'] = []

    inventory = character['inventory']
    
    # 1. Check if inventory is full
    if len(inventory) >= MAX_INVENTORY_SIZE:
        # Raise InventoryFullError
        raise InventoryFullError() 
        
    # 2. Add item_id to character['inventory'] list
    inventory.append(item_id)
    
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    if 'inventory' not in character:
        # If the list doesn't exist, the item certainly isn't there
        raise ItemNotFoundError(item_id)

    inventory = character['inventory']
    
    # 1. Check if item exists and remove it
    try:
        # The list.remove() method removes the first occurrence of the value
        inventory.remove(item_id)
        return True
    except ValueError:
        # list.remove() raises a ValueError if the item is not found
        # Raise ItemNotFoundError
        raise ItemNotFoundError(item_id)

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    if 'inventory' not in character:
        return False
        
    # Use the 'in' operator to quickly check for presence
    return item_id in character['inventory']

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    if 'inventory' not in character:
        return 0
        
    # Use list.count() method
    return character['inventory'].count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    if 'inventory' not in character:
        current_size = 0
    else:
        current_size = len(character['inventory'])
        
    # Calculate remaining space, ensuring the result is not negative
    remaining_space = MAX_INVENTORY_SIZE - current_size
    
    return max(0, remaining_space)

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    if 'inventory' not in character:
        # If no inventory exists, return an empty list of removed items
        return []
        
    # Save a copy of the current inventory before clearing
    removed_items = character['inventory'].copy()
    
    # Clear character's inventory list (easiest way is usually slice assignment)
    character['inventory'] = []
    
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    # 1. Check if character has the item
    # 1. Check if character has the item
    if not has_item(character, item_id):
        raise ItemNotFoundError(item_id)
        
    item_name = item_data.get('name', item_id)
    item_type = item_data.get('type')
    
    # 2. Check if item type is 'consumable'
    if item_type != 'consumable':
        raise InvalidItemTypeError(f"Item '{item_name}' is a '{item_type}' and cannot be used in this manner.")
        
    # 3. Parse effect data
    effect = item_data.get('effect')
    if not effect or 'stat' not in effect or 'value' not in effect:
        raise InvalidItemTypeError(f"Item '{item_name}' has an invalid or missing effect definition.")

    stat_name = effect['stat']
    stat_value = effect['value']
    
    effect_message = ""

    # 4. Directly apply the effect based on the stat_name
    
    if stat_name == "health":
        current_hp = character.get('health', 0)
        max_hp = character.get('max_health', current_hp)
        
        # Calculate new health, capped by max_health
        new_hp = min(current_hp + stat_value, max_hp)
        
        # Calculate the actual amount gained
        actual_gain = new_hp - current_hp
        
        character['health'] = new_hp
        
        if actual_gain > 0:
            effect_message = f"Healed for {actual_gain} HP."
        elif actual_gain < 0:
            effect_message = f"Lost {abs(actual_gain)} HP."
        else:
            effect_message = "Health remains unchanged (already maxed or item had no effect)."
            
    # Handle other stats (e.g., strength, defense) as permanent buffs/debuffs
    elif stat_name in character:
        character[stat_name] = character.get(stat_name, 0) + stat_value
        effect_message = f"{stat_name} changed by {stat_value}."
    
    else:
        effect_message = f"Effect on unsupported stat '{stat_name}' was skipped."


    # 5. Remove item from inventory
    remove_item_from_inventory(character, item_id)
    
    # Final message assembly
    return f"✨ Used {item_name}. {effect_message}"

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    # Validation checks
    if not has_item(character, item_id):
        raise ItemNotFoundError(item_id)
        
    item_name = item_data.get('name', item_id)
    item_type = item_data.get('type')
    
    if item_type != 'weapon':
        raise InvalidItemTypeError(f"Item '{item_name}' is a '{item_type}'. Only 'weapon' can be equipped here.")

    effect = item_data.get('effect')
    if not effect or 'stat' not in effect or 'value' not in effect:
        raise InvalidItemTypeError(f"Weapon '{item_name}' has an invalid effect definition.")

    new_stat = effect['stat']
    new_value = effect['value']

    unequip_message = ""
    

    # Apply New Weapon Effect (INLINED LOGIC)
    applied_new_bonus = False
    if new_stat in character and isinstance(character[new_stat], (int, float)):
        character[new_stat] += new_value
        applied_new_bonus = True
    
    if not applied_new_bonus:
        raise InvalidItemTypeError(f"Weapon '{item_name}' has an effect on an unsupported stat: {new_stat}.")

    # Finalize
    character['equipped_weapon'] = item_id
    remove_item_from_inventory(character, item_id)
    
    #  Final message assembly
    return (
        f"⚔️ {unequip_message}Equipped {item_name}! "
        f"({new_stat.capitalize()}: +{new_value}). "
        f"Current {new_stat.capitalize()}: {character.get(new_stat, 'N/A')}"
    )
def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    # Validation checks
    if not has_item(character, item_id):
        raise ItemNotFoundError(item_id)
        
    item_name = item_data.get('name', item_id)
    item_type = item_data.get('type')
    
    if item_type != 'armor':
        raise InvalidItemTypeError(f"Item '{item_name}' is a '{item_type}'. Only 'armor' can be equipped here.")

    effect = item_data.get('effect')
    if not effect or 'stat' not in effect or 'value' not in effect:
        raise InvalidItemTypeError(f"Armor '{item_name}' has an invalid effect definition.")

    new_stat = effect['stat']
    new_value = effect['value']

    unequip_message = ""
    
    #  Handle Unequipping Current Armor (if any)
   

    #  Apply New Armor Effect (Inline Logic)
    applied_new_bonus = False
    if new_stat in character and isinstance(character[new_stat], (int, float)):
        character[new_stat] += new_value
        applied_new_bonus = True
        
        
    if not applied_new_bonus:
        # If the stat is unknown or not numeric, raise an error
        raise InvalidItemTypeError(f"Armor '{item_name}' has an effect on an unsupported stat: {new_stat}.")

    #  Finalize
    character['equipped_armor'] = item_id
    remove_item_from_inventory(character, item_id)
    
    #  Final message assembly
    current_stat_value = character.get(new_stat, 'N/A')
    
    return (
        f"🛡️ {unequip_message}Equipped {item_name}! "
        f"({new_stat.capitalize()}: +{new_value}). "
        f"Current {new_stat.capitalize()}: {current_stat_value}"
    )
def unequip_weapon(character, item_data_dict):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    old_weapon_id = character.pop('equipped_weapon', None)
    
    if old_weapon_id is None:
        return None # Nothing to unequip
        
    # 2. Look up the old weapon's effect data
    if old_weapon_id in item_data_dict:
        old_item_data = item_data_dict[old_weapon_id]
        old_effect = old_item_data.get('effect', {})
        old_stat = old_effect.get('stat', 'strength') # Default to common weapon stat
        old_value = old_effect.get('value', 0)
        
        # 3. Add weapon back to inventory (MUST happen before removing stats, 
        # as this can raise InventoryFullError)
        try:
            add_item_to_inventory(character, old_weapon_id)
        except InventoryFullError:
            # If inventory is full, return the weapon ID to the character object
            # and re-raise the error.
            character['equipped_weapon'] = old_weapon_id 
            raise InventoryFullError(f"Cannot unequip {old_weapon_id}: Inventory is full.")

        # 4. Remove stat bonuses (Inline Logic)
        if old_stat in character and isinstance(character[old_stat], (int, float)):
            character[old_stat] -= old_value
            
        return old_weapon_id

def unequip_armor(character, GAME_ITEM_DATA):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    old_armor_id = character.pop('equipped_armor', None)
    
    if old_armor_id is None:
        return None # Nothing to unequip
        
    # 2. Look up the old armor's effect data using the GLOBAL constant
    if old_armor_id in GAME_ITEM_DATA:
        old_item_data = GAME_ITEM_DATA[old_armor_id]
        old_effect = old_item_data.get('effect', {})
        old_stat = old_effect.get('stat', 'max_health') # Default to common armor stat
        old_value = old_effect.get('value', 0)
        
        # 3. Add armor back to inventory (Must happen before removing stats, 
        # as this can raise InventoryFullError)
        try:
            # Assuming add_item_to_inventory is accessible
            add_item_to_inventory(character, old_armor_id)
        except InventoryFullError:
            # If inventory is full, return the armor ID to the character object
            # and re-raise the error.
            character['equipped_armor'] = old_armor_id 
            raise InventoryFullError(f"Cannot unequip {old_armor_id}: Inventory is full.")

        # 4. Remove stat bonuses (Inline Logic)
        if old_stat in character and isinstance(character[old_stat], (int, float)):
            # Remove the bonus
            character[old_stat] -= old_value
            
            # Special Case: If max_health was reduced, check and clamp current health.
            if old_stat == 'max_health':
                current_health = character.get('health', 0)
                new_max_health = character[old_stat]
                
                # Health cannot exceed the new maximum
                if current_health > new_max_health:
                    character['health'] = new_max_health
            
        return old_armor_id
    
    # Case where the ID was equipped but the data is missing
    return None

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    item_cost = item_data.get('cost', 0)
    current_gold = character.get('gold', 0)
    
    # 1. Check if character has enough gold
    if current_gold < item_cost:
        raise InsufficientResourcesError("Gold", item_cost, current_gold)
    
    # 2. Check if inventory has space
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Cannot purchase item: Inventory is full.")
        
    # 3. Subtract gold from character
    character['gold'] = current_gold - item_cost
    
    # 4. Add item to inventory
    # This call includes a final check for space and handles the addition
    add_item_to_inventory(character, item_id)
    
    item_name = item_data.get('name', item_id)
    
    # Optional: Return a descriptive message
    print(f"💰 Purchased {item_name} for {item_cost} gold. Remaining gold: {character['gold']}")
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    # 1. Check if character has the item and remove it from inventory
    # remove_item_from_inventory handles the ItemNotFoundError if the item isn't present.
    remove_item_from_inventory(character, item_id)
    
    item_cost = item_data.get('cost', 0)
    
    # 2. Calculate sell price (cost // 2 for integer division)
    # The cost is typically the purchase price; selling is half that.
    sell_price = item_cost // 2
    
    # 3. Add gold to character
    current_gold = character.get('gold', 0)
    character['gold'] = current_gold + sell_price
    
    item_name = item_data.get('name', item_id)
    
    # Optional: Print a descriptive message
    print(f"💰 Sold {item_name} for {sell_price} gold. Character now has {character['gold']} gold.")
    
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    # Split the string into stat and value, limiting the split to 1
    parts = [p.strip() for p in effect_string.split(':', 1)]
    
    # Validation: Check if we got exactly two parts
    if len(parts) != 2:
        raise InvalidItemTypeError(f"Effect format invalid: '{effect_string}'. Expected 'stat:value'.")
        
    stat_name = parts[0]
    
    # Attempt to convert the value to an integer
    try:
        value = int(parts[1])
    except ValueError:
        raise InvalidItemTypeError(f"Effect value is not a valid integer: '{parts[1]}'.")
        
    return stat_name, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    # 1. Handle health separately (requires max_health check)
    if stat_name == "health":
        # Get current health and max health, defaulting to safe values
        current_hp = character.get('health', 0)
        max_hp = character.get('max_health', current_hp) # If max_health isn't set, use current HP as max
        
        new_hp = current_hp + value
        
        # Apply the new health, ensuring it does not exceed max_health
        character['health'] = min(new_hp, max_hp)
        
        # Also ensure health doesn't drop below zero
        character['health'] = max(0, character['health'])
        
    # 2. Handle other stats
    elif stat_name in character:
        # Check if the stat is an integer/float before modifying
        if isinstance(character[stat_name], (int, float)):
            character[stat_name] += value
        else:
            print(f"Warning: Stat '{stat_name}' is not numeric and was not modified.")
            
    # 3. Handle stats that might be new (e.g., permanent buff from consumable)
    # This assumes we want to add the stat if it doesn't exist
    elif isinstance(value, int) or isinstance(value, float):
        character[stat_name] = value

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    inventory_list = character.get('inventory', [])
    
    if not inventory_list:
        return "Inventory is empty."
        
    # 1. Count items (items can appear multiple times)
    item_counts = {}
    for item_id in inventory_list:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1
        
    # Determine the max capacity (assumed from MAX_INVENTORY_SIZE, but safely using current length for display)
    max_slots = character.get('max_inventory_size', 20) # Use 20 as default if not defined in character
        
    output = ["## 🎒 Inventory Status"]
    output.append(f"Total items: {len(inventory_list)} / {max_slots}")
    output.append("---")
    
    # 2. Display unique items, sorted by name or ID
    for item_id, count in sorted(item_counts.items()):
        # Get data, falling back to safe defaults for unknown items
        item_info = item_data_dict.get(item_id, {'name': 'UNKNOWN ITEM', 'type': 'N/A'})
        
        name = item_info['name']
        item_type = item_info['type'].capitalize()
        
        output.append(f"* **{name}** ({item_type}) x{count}")
        
    return "\n".join(output)

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

