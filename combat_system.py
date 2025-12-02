"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""
import random
import character_manager
from character_manager import is_character_dead
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    BASE_STATS = {
        "goblin": {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100},
    }
    
    # Ensure the input is lowercase for case-insensitive matching
    enemy_type = enemy_type.lower()
    
    # 1. Validate enemy_type
    if enemy_type not in BASE_STATS:
        raise InvalidTargetError(enemy_type, list(BASE_STATS.keys()))
        
    # Get base stats for the selected enemy
    stats = BASE_STATS[enemy_type]
    
    # 2. Implement enemy creation (health and max_health are the same initially)
    enemy_data = {
        "name": enemy_type.capitalize(), # Capitalize for display name
        "type": enemy_type,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "xp_reward": stats["xp_reward"],
        "gold_reward": stats["gold_reward"],
    }
    
    return enemy_data

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 0:
        raise ValueError("Character level must be 1 or greater.")
        
    enemy_type = ""
    
    # Implement level-appropriate enemy selection
    if character_level <= 2:
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else: # Level 6 and above
        enemy_type = "dragon"

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character
        self.enemy = enemy
        
        # Set combat_active flag
        self.combat_active = False
        
        # Initialize turn counter
        self.turn = 0
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        # Check character isn't dead
        if is_character_dead(self.character):
            raise CharacterDeadError(self.character["name"])
            
        self.combat_active = True
        print(f"\n--- Battle Started: {self.character['name']} vs. {self.enemy['name']} ---")
        
        while self.combat_active:
            self.turn += 1
            print(f"\nTurn {self.turn}")
            
            # 1. Character's Turn
            if not is_character_dead(self.character):
                self._calculate_damage(self.character, self.enemy)
                
            # Check if Enemy died after character's attack
            if is_character_dead(self.enemy):
                self.combat_active = False
                print(f"** {self.enemy['name']} defeated! **")
                break
                
            # 2. Enemy's Turn
            if not is_character_dead(self.enemy):
                self._calculate_damage(self.enemy, self.character)
                
            # Check if Character died after enemy's attack
            if is_character_dead(self.character):
                self.combat_active = False
                print(f"** {self.character['name']} was defeated... **")
                break
                
            print(f"  {self.character['name']} Health: {self.character['health']}/{self.character['max_health']}")
            print(f"  {self.enemy['name']} Health: {self.enemy['health']}/{self.enemy['max_health']}")

        # 3. Determine Winner and Results
        winner = 'player' if is_character_dead(self.enemy) else 'enemy'
        xp_gained = self.enemy.get("xp_reward", 0) if winner == 'player' else 0
        gold_gained = self.enemy.get("gold_reward", 0) if winner == 'player' else 0

        # Award XP and gold if player wins (This would normally call the gain_experience and add_gold functions)
        if winner == 'player':
            print(f"Rewards: +{xp_gained} XP, +{gold_gained} Gold.")
        
        return {
            'winner': winner, 
            'xp_gained': xp_gained, 
            'gold_gained': gold_gained
        }
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        # 1. Check combat is active
        if not self.combat_active:
            raise CombatNotActiveError()
            
        player_name = self.character["name"]
        
        while True:
            # 2. Display options
            print(f"\n{player_name}'s Turn (Health: {self.character['health']}/{self.character['max_health']})")
            print("1. Basic Attack (STR: {})".format(self.character['strength']))
            print("2. Special Ability (Placeholder)")
            print("3. Try to Run")
            
            # 3. Get player choice
            choice = input("Enter action number (1-3): ").strip()
            
            # 4. Execute chosen action
            if choice == '1':
                # Basic Attack
                damage = self._calculate_damage(self.character, self.enemy)
                print(f"{player_name} attacks the {self.enemy['name']} for {damage} damage.")
                
                if self.enemy["health"] <= 0:
                    return 'win'
                return 'continue'
                
            elif choice == '2':
                # Special Ability (Placeholder)
                print(f"{player_name} uses a placeholder special ability. (No effect yet.)")
                return 'continue' # For now, acts as a skip
                
            elif choice == '3':
                # Try to Run
                if self._run_attempt():
                    print(f"{player_name} successfully flees the battle!")
                    return 'flee'
                else:
                    print(f"{player_name} failed to escape!")
                    return 'continue'
                    
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        # Check combat is active
        if not self.combat_active:
            raise CombatNotActiveError()
            
        enemy_name = self.enemy["name"]
        
        # Enemy always attacks
        damage = self._calculate_damage(self.enemy, self.character)
        
        print(f"  {enemy_name} attacks {self.character['name']} for {damage} damage.")
        
        # Check if Character died after enemy's attack
        if self.character["health"] <= 0:
            print(f"** {self.character['name']} was defeated by the {enemy_name}! **")
            return 'dead'
        
        return 'continue'
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        # Calculate defense value (integer division)
        defense = defender.get('strength', 0) // 4
        
        # Calculate raw damage
        raw_damage = attacker.get('strength', 0) - defense
        
        # Apply minimum damage rule
        final_damage = max(1, raw_damage)
        
        return final_damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        damage = max(0, damage)
        
        # Reduce health
        target["health"] -= damage
        
        # Prevent negative health
        if target["health"] < 0:
            target["health"] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if is_character_dead(self.enemy):
            return 'player'
        elif is_character_dead(self.character):
            return 'enemy'
        else:
            return None # Battle is ongoing
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        if random.random() < 0.5: 
            self.combat_active = False
            return True
        else:
            return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================
def _apply_damage(target, damage):
    """Reduces health, prevents negative health."""
    # Ensure damage is non-negative
    damage = max(0, damage)
    
    target["health"] -= damage
    
    # Prevent negative health
    if target["health"] < 0:
        target["health"] = 0

def _heal_target(target, amount):
    """Heals target, returns actual amount healed."""
    max_health = target["max_health"]
    needed_heal = max_health - target["health"]
    actual_heal = min(amount, needed_heal)
    target["health"] += actual_heal
    return actual_heal

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    character_class = character.get("class")
    
    if character_class == "Warrior":
        return warrior_power_strike(character, enemy)
    
    elif character_class == "Mage":
        return mage_fireball(character, enemy)
        
    elif character_class == "Rogue":
        return rogue_critical_strike(character, enemy)
        
    elif character_class == "Cleric":
        # Cleric ability only needs the character
        return cleric_heal(character)
        
    else:
        return f"⚠️ {character_class} does not have a defined special ability."

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    base_damage = character.get('strength', 0)
    damage = base_damage * 2
    
    _apply_damage(enemy, damage)
    
    return f"⚔️ {character['name']} uses Power Strike, dealing {damage} physical damage to {enemy['name']}!"

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    base_damage = character.get('magic', 0)
    damage = base_damage * 2
    
    _apply_damage(enemy, damage)
    
    return f"🔥 {character['name']} summons a Fireball, dealing {damage} magical damage to {enemy['name']}!"

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    base_damage = character.get('strength', 0)
    
    if random.random() < 0.5:
        damage = base_damage * 3
        _apply_damage(enemy, damage)
        return f"🔪 {character['name']} lands a **CRITICAL STRIKE** for {damage} damage on {enemy['name']}!"
    else:
        damage = 0
        _apply_damage(enemy, damage) # Must apply 0 damage to keep flow consistent
        return f"💨 {character['name']} tries a Critical Strike but misses the sweet spot."

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    heal_amount = 30
    actual_heal = _heal_target(character, heal_amount)
    
    if actual_heal > 0:
        return f"✨ {character['name']} **heals themselves** for {actual_heal} health. Current HP: {character['health']}/{character['max_health']}."
    else:
        return f"🛡️ {character['name']} attempts to heal but is already at maximum health."

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    # 1. Check if the character is alive
    if character.get('health', 0) <= 0:
        print(f"🛑 {character.get('name', 'Character')} cannot fight: Health is too low.")
        return False
        
    # 2. Check if the character is currently in a battle
    # NOTE: This requires the 'character' dictionary to have a flag (e.g., 'is_in_battle').
    # Assuming such a flag exists for a complete implementation:
    if character.get('is_in_battle', False) == True:
        print(f"🛑 {character.get('name', 'Character')} cannot fight: Already in combat.")
        return False
        
    return True

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    xp = enemy.get('xp_reward', 0)
    gold = enemy.get('gold_reward', 0)
    
    return {
        'xp': xp,
        'gold': gold
    }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    print("\n" + "="*40)
    print(f"| {character.get('name', 'Player'):<18} | {enemy.get('name', 'Enemy'):<18} |")
    print("-" * 40)
    print(f"| HP: {character.get('health'):<14} | HP: {enemy.get('health'):<14} |")
    print("="*40)

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

