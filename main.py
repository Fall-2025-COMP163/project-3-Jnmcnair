"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    while True:
        # 1. Show options
        print("\n=== Main Menu ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        print("-------------------")
        
        # 2. Get user input
        choice_input = input("Enter your choice (1-3): ").strip()
        
        # 3. Validate input
        try:
            choice = int(choice_input)
            
            # Check if the choice is within the valid range
            if 1 <= choice <= 3:
                # 4. Return choice
                return choice
            else:
                print("⚠️ Invalid choice. Please enter a number between 1 and 3.")
                
        except ValueError:
            # Handle cases where the input is not a number
            print("⚠️ Invalid input. Please enter a numerical choice.")

# Example of how to use the function:
if __name__ == "__main__":
    player_choice = main_menu()
    print(f"\nPlayer selected option: {player_choice}")
    
    if player_choice == 1:
        print("Starting a New Game...")
    elif player_choice == 2:
        print("Loading a Saved Game...")
    elif player_choice == 3:
        print("Exiting the game. Goodbye!")

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    # 1. Get character name from user
    name = input("Enter your character's name: ").strip()
    if not name:
        print("Character creation cancelled. Name cannot be empty.")
        return

    while True:
        # 2. Get character class from user
        class_prompt = f"Choose your class ({', '.join(character_manager.VALID_CLASSES)}): "
        class_choice = input(class_prompt).strip()
        
        # 3. Try to create character
        try:
            new_char = character_manager.create_character(name, class_choice)
            
            # Character creation successful
            current_character = new_char
            print(f"\n✅ Character '{name}' ({class_choice.capitalize()}) created successfully!")
            
            # Optional: Save character (placeholder)
            # character_manager.save_character(current_character) 
            
            # 4. Start game loop
            game_loop()
            break
            
        # 4. Handle InvalidCharacterClassError
        except InvalidCharacterClassError as e:
            print(f"❌ Error: {e}. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred during character creation: {e}")
            break

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    # 1. Get list of saved characters
    try:
        saved_games = character_manager.list_saved_characters()
    except Exception as e:
        print(f"❌ Error retrieving saved games: {e}")
        return

    if not saved_games:
        print("ℹ️ No saved games found. Please start a New Game.")
        return

    while True:
        # 2. Display them to user
        print("\n=== Saved Characters ===")
        for i, name in enumerate(saved_games, 1):
            print(f"{i}. {name}")
        print("------------------------")
        
        # 3. Get user choice
        choice_input = input("Enter the number of the game to load (or 'C' to Cancel): ").strip()
        
        if choice_input.lower() == 'c':
            print("Loading cancelled.")
            return

        try:
            choice_index = int(choice_input) - 1
            
            if 0 <= choice_index < len(saved_games):
                selected_save_name = saved_games[choice_index]
                
                # 4. Try to load character
                print(f"Attempting to load '{selected_save_name}'...")
                
                try:
                    loaded_char = character_manager.load_character(selected_save_name)
                    
                    # Successfully loaded
                    current_character = loaded_char
                    print(f"✅ Game loaded successfully! Welcome back, {current_character['name']}.")
                    
                    # 5. Start game loop
                    game_loop()
                    return # Exit the load_game function
                
                # 6. Handle CharacterNotFoundError and SaveFileCorruptedError
                except CharacterNotFoundError as e:
                    print(f"❌ Load Error: {e}. The save file appears to be missing.")
                    # Continue the loop to allow user to try again
                
                except SaveFileCorruptedError as e:
                    print(f"❌ Load Error: {e}. This save file is unusable and has been skipped.")
                    # Optionally remove the corrupted file from the list/disk here
                    saved_games.remove(selected_save_name)
                    if not saved_games:
                         print("No more valid saved games left.")
                         return

            else:
                print("⚠️ Invalid number selected. Please try again.")

        except ValueError:
            print("⚠️ Invalid input. Please enter a number or 'C' to cancel.")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    # Safety check: Ensure a character is loaded
    if not current_character or not current_character.get('name'):
        print("❌ Error: Cannot start game loop. No character is loaded.")
        game_running = False
        return

    game_running = True
    print("\n==================================")
    print(f"Adventure Begins, {current_character['name']}!")
    print("==================================")
    
    
    while game_running:
        print("\n--- Current Status ---")
        print(view_character_stats(current_character))
        print("----------------------")

        # Display game menu
        print("\n=== Game Menu ===")
        print("1. Explore (Adventure/Combat)")
        print("2. Visit Town (Shop/Heal)")
        print("3. Check Inventory")
        print("4. Save Game")
        print("5. Quit Game")
        print("-----------------")

        # Get player choice
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '5':
            print("👋 Are you sure you want to quit? (Y/N)")
            if input().strip().lower() == 'y':
                save_game(current_character)
                print("Exiting the adventure. Goodbye!")
                game_running = False
            continue # Skip saving if canceled

        elif choice == '4':
            # Execute Save action directly
            save_game(current_character)

        elif choice in ('1', '2', '3'):
            result = (current_character, choice)
            print(f"➡️ Action Result: {result}")
            
            # Save game after *each* significant action
            save_game(current_character)
            
        else:
            print(f"⚠️ Invalid choice '{choice}'. Please enter a number between 1 and 5.")

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    while True:
        # Display game menu options
        print("\n=== Game Menu ===")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")
        print("-------------------")
        
        # Get user input
        choice_input = input("Enter your choice (1-6): ").strip()
        
        # Validate input
        try:
            choice = int(choice_input)
            
            # Check if the choice is within the valid range
            if 1 <= choice <= 6:
                return choice
            else:
                print("⚠️ Invalid choice. Please enter a number between 1 and 6.")
                
        except ValueError:
            # Handle cases where the input is not a number
            print("⚠️ Invalid input. Please enter a numerical choice.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    if not current_character:
        print("❌ No character loaded.")
        return

    char = current_character
    
    # Use character_manager functions
    level, xp, xp_to_next = character_manager.get_level_and_xp(char)
    quest_summary = quest_handler.get_progress_summary(char)
    
    # Get equipped item names
    weapon_id = char.get('equipped_weapon')
    armor_id = char.get('equipped_armor')
    
    # Assuming GAME_ITEM_DATA is a global dictionary
    weapon_name = GAME_ITEM_DATA.get(weapon_id, {}).get('name', 'None') if weapon_id else 'None'
    armor_name = GAME_ITEM_DATA.get(armor_id, {}).get('name', 'None') if armor_id else 'None'
    
    print("\n==============================")
    print(f"       {char['name'].upper()} - STATS")
    print("==============================")
    print(f"**Class:** {char['class'].capitalize()}")
    print(f"**Level:** {level} (XP: {xp}/{xp + xp_to_next})")
    print(f"**Gold:** {char.get('gold', 0)}")
    print("------------------------------")
    print(f"**Health:** {char.get('health', 0)} / {char.get('max_health', 0)}")
    print(f"**Strength:** {char.get('strength', 0)}")
    print(f"**Magic:** {char.get('magic', 0)}")
    print("------------------------------")
    print(f"**Equipped Weapon:** {weapon_name}")
    print(f"**Equipped Armor:** {armor_name}")
    print("------------------------------")
    print(f"**Quest Progress:** {quest_summary}")
    print("==============================")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    if not current_character:
        print("❌ No character loaded.")
        return

    char = current_character
    
    while True:
        # Show current inventory (assuming display_inventory is defined elsewhere)
        display_inventory(char, GAME_ITEM_DATA)
        
        print("\n--- Inventory Actions ---")
        print("U. Use Item | E. Equip/Unequip | S. Sell Item | D. Drop Item | B. Back")
        action = input("Choose an action: ").strip().lower()

        if action == 'b':
            return

        if action in ('u', 'e', 's', 'd'):
            # For simplicity, we ask for the item ID (not the name)
            item_id = input("Enter the ID of the item: ").strip()
            item_data = GAME_ITEM_DATA.get(item_id)

            if not item_data:
                print(f"❌ Item ID '{item_id}' not found in game data.")
                continue
                
            try:
                if action == 'u':
                    if item_data['type'] != 'consumable':
                        print("❌ Only consumable items can be 'Used'.")
                    else:
                        print(f"✅ {inventory_system.use_item(char, item_id, item_data)}")
                        
                elif action == 'e':
                    if item_data['type'] == 'weapon':
                        # The equip_weapon function should handle unequipping the old one
                        print(f"✅ {inventory_system.equip_weapon(char, item_id, item_data)}")
                    elif item_data['type'] == 'armor':
                        # Same for armor
                        print(f"✅ Armor equipped (Functionality TBD)") 
                    else:
                        print(f"❌ Cannot equip item of type '{item_data['type']}'.")
                        
                elif action == 's':
                    gold_received = inventory_system.sell_item(char, item_id, item_data)
                    print(f"✅ Sold {item_data['name']} for {gold_received} gold.")
                    
                elif action == 'd':
                    inventory_system.remove_item_from_inventory(char, item_id)
                    print(f"🗑️ Dropped {item_data['name']}.")
                    
            except (ItemNotFoundError, InvalidItemTypeError, InventoryFullError) as e:
                print(f"❌ Inventory Error: {e}")
                
        else:
            print("⚠️ Invalid action.")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    if not current_character:
        print("❌ No character loaded.")
        return
    
    char = current_character
    
    while True:
        print("\n=== 📜 Quest Menu ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (Testing/Admin)")
        print("7. Back")
        print("--------------------")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '7':
            return
            
        try:
            if choice == '1':
                print("\n**ACTIVE QUESTS:**")
                active_quests = quest_handler.view_active_quests(char)
                if active_quests:
                    for q in active_quests: print(f"- {q}")
                else:
                    print("No active quests.")
            
            elif choice == '2':
                print("\n**AVAILABLE QUESTS:**")
                available_quests = quest_handler.view_available_quests(char)
                if available_quests:
                    # Assumes available_quests returns a dictionary/list suitable for printing ID and description
                    for qid, desc in available_quests.items(): print(f"[{qid}] {desc}")
                else:
                    print("No quests currently available.")

            elif choice == '3':
                print("\n**COMPLETED QUESTS:**")
                completed_quests = quest_handler.view_completed_quests(char)
                if completed_quests:
                    for q in completed_quests: print(f"✅ {q}")
                else:
                    print("No quests completed yet.")
            
            elif choice == '4':
                q_id = input("Enter the ID of the Quest to ACCEPT: ").strip()
                result = quest_handler.accept_quest(char, q_id)
                print(f"✅ {result}")

            elif choice == '5':
                q_id = input("Enter the ID of the Quest to ABANDON: ").strip()
                result = quest_handler.abandon_quest(char, q_id)
                print(f"🗑️ {result}")

            elif choice == '6':
                q_id = input("Enter the ID of the Quest to FORCE COMPLETE (Admin): ").strip()
                result = quest_handler.complete_quest(char, q_id)
                print(f"🔥 {result}")
                
            else:
                print("⚠️ Invalid choice.")
                
        except (QuestNotFoundError, QuestRequirementsNotMetError) as e:
            # Catch specific, anticipated quest-related exceptions
            print(f"❌ Quest Error: {e}")
        except Exception as e:
            # Catch any unexpected errors (e.g., I/O issues, internal logic errors)
            print(f"🚨 An unexpected error occurred: {e}")

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    if not current_character:
        print("❌ No character loaded.")
        return
    
    char = current_character
    
    print("\n🔍 Exploring the wilderness...")
    
    try:
        # 1. Generate random enemy based on character level
        level, _, _ = character_manager.get_level_and_xp(char)
        enemy_data = enemy_data(level)
        
        print(f"Encountered a **{enemy_data['name']}** (Lvl {enemy_data['level']})!")
        
        # 2. Start combat
        results = combat_system.SimpleBattle(char, enemy_data)
        
        # 3. Handle combat results
        if results['result'] == 'win':
            char['xp'] = char.get('xp', 0) + results['xp']
            char['gold'] = char.get('gold', 0) + results['gold']
            
            print("🎉 **VICTORY!**")
            print(f"Gained {results['xp']} XP and {results['gold']} Gold.")
            
            # Handle loot
            if results.get('loot'):
                for item in results['loot']:
                    try:
                        equip_item(char, item)
                        print(f"💰 Found loot: {item} (Added to inventory).")
                    except InventoryFullError:
                        print(f"⚠️ Could not pick up {item}: Inventory is full.")
        
        elif results['result'] == 'loss':
            damage = results.get('damage_taken', 0)
            print("💀 **DEFEAT!**")
            print(f"You narrowly escaped, but took {damage} damage.")
            print(f"Current Health: {char.get('health')}")
            
            # Handle death/critical loss
            if char['health'] <= 0:
                print("YOU DIED. Game Over.")
                # Logic for game over/respawn
                
    except Exception as e:
        print(f"❌ Exploration Error: {e}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    if not current_character:
        print("❌ No character loaded.")
        return

    char = current_character
    
    while True:
        current_gold = char.get('gold', 0)
        
        print("\n=== 🛍️ The Village Shop ===")
        print(f"Current Gold: {current_gold}")
        print("----------------------------")
        
        # Show available items for purchase
        print("**Items for Sale:**")
        print("ID   | Name | Type | Cost (Sell)")
        print("-----|------|------|------------")
        for i, item_id in enumerate(SHOP_ITEMS, 1):
            item_data = GAME_ITEM_DATA.get(item_id, {})
            name = item_data.get('name', item_id)
            cost = item_data.get('cost', 0)
            sell_price = cost // 2
            item_type = item_data.get('type', 'N/A').capitalize()
            print(f"{i:<4} | {name:<10} | {item_type:<5} | {cost} ({sell_price})")
        
        print("----------------------------")
        print("B. Buy Item | S. Sell Item | X. Back to Menu")
        choice = input("Enter your choice: ").strip().lower()

        if choice == 'x':
            return

        try:
            if choice == 'b':
                item_choice = input("Enter the number of the item to buy: ").strip()
                item_index = int(item_choice) - 1
                
                if 0 <= item_index < len(SHOP_ITEMS):
                    item_id = SHOP_ITEMS[item_index]
                    item_data = GAME_ITEM_DATA[item_id]
                    
                    inventory_system.purchase_item(char, item_id, item_data)
                    print(f"✅ Purchased {item_data['name']} for {item_data['cost']} gold.")
                else:
                    print("⚠️ Invalid item number.")
                    
            elif choice == 's':
                item_id = input("Enter the ID of the item to sell (e.g., wood_sword): ").strip()
                
                if item_id not in GAME_ITEM_DATA:
                    print(f"❌ Unknown item ID: {item_id}.")
                    continue
                    
                item_data = GAME_ITEM_DATA[item_id]
                sell_amount = inventory_system.sell_item(char, item_id, item_data)
                print(f"✅ Sold {item_data['name']} for {sell_amount} gold.")
                
            else:
                print("⚠️ Invalid choice.")
                
        except ValueError:
            print("⚠️ Invalid input. Please enter a number or a valid menu option.")
        except (InsufficientResourcesError, InventoryFullError, ItemNotFoundError) as e:
            print(f"❌ Transaction Error: {e}")
        except Exception as e:
            print(f"🚨 An unexpected error occurred: {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    if not current_character:
        print("⚠️ Cannot save: No character data is currently loaded.")
        return

    char_name = current_character.get('name', 'Unnamed Character')
    print(f"Attempting to save game for **{char_name}**...")
    
    try:
        # 1. Use character_manager.save_character()
        character_manager.save_character(current_character)
        
        print(f"✅ Game saved successfully for **{char_name}**.")
        
    # 2. Handle any file I/O exceptions (Using the custom SaveError and general OSError)
    except ( OSError, IOError) as e:
        print(f"❌ Save Failed for {char_name}: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    data_loaded = False
    
    # First, attempt to create default files if they don't exist.
    try:
        # Try to load quest data
        all_quests = game_data.load_quests()
        
        # Try to load item data
        all_items = game_data.load_items()
        
        data_loaded = True
        print("✅ Game data (Quests & Items) loaded successfully.")

    except MissingDataFileError as e:
        print(f"⚠️ Missing data file: {e}. Attempting to create defaults...")
        
        # If files missing, create defaults
        try:
            default_quests, default_items = game_data.create_default_data_files()
            all_quests = default_quests
            all_items = default_items
            data_loaded = True
            print("✅ Default data loaded.")
            
        except Exception as e:
            print(f"❌ FATAL ERROR: Could not create default files. Game cannot run. Details: {e}")
            return # Exit the function, as data loading failed entirely
            
    except InvalidDataFormatError as e:
        print(f"❌ Data Format Error in file: {e}. Please correct the file format.")
        return # Exit, as corrupted files cannot be automatically fixed safely

    except Exception as e:
        print(f"❌ An unexpected error occurred during data loading: {e}")
        return

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    char_name = current_character.get('name', 'The Hero')
    
    print("\n\n" + "💀" * 20)
    print(f"      **{char_name.upper()} HAS FALLEN!**")
    print("💀" * 20)
    
    # 1. Display death message and offer options
    cost = character_manager.REVIVE_COST * current_character.get('level', 1)
    
    while True:
        print(f"\nYour quest ends here, unless you can pay the price to return.")
        print(f"Current Gold: {current_character.get('gold', 0)}")
        print(f"Revive Cost: {cost} gold.")
        
        print("\nOptions:")
        print(f"1. Revive (Pay {cost} Gold)")
        print("2. Quit Game (Character will be lost/unplayable)")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == '1':
            # Try to revive
            try:
                gold_paid = character_manager.revive_character(current_character)
                print(f"✨ You paid {gold_paid} gold and were instantly revived!")
                print(f"Health restored to {current_character['health']}.")
                return # Exit death handling
                
            except InsufficientResourcesError as e:
                print(f"❌ Revival Failed: {e}")
                
            except Exception as e:
                print(f"❌ An unexpected error occurred during revival: {e}")
                
        elif choice == '2':
            # Quit game
            print("\nYour spirit fades... The adventure is over.")
            game_running = False
            return
            
        else:
            print("⚠️ Invalid choice. Please enter 1 or 2.")

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

