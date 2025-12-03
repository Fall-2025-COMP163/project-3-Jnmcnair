[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wnCpjX4n)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21913790&assignment_repo_type=AssignmentRepo)
# COMP 163: Project 3 - Quest Chronicles

**AI Usage: Free Use (with explanation requirement)**

## Overview

Build a complete modular RPG adventure game demonstrating mastery of **exceptions and modules**.

## Getting Started

### Step 1: Accept Assignment
1. Click the assignment link provided in Blackboard
2. Accept the assignment - this creates your personal repository
3. Clone your repository to your local machine:
```bash
git clone [your-personal-repo-url]
cd [repository-name]
```

### Step 2: Understand the Project Structure

Your repository contains:

```
quest_chronicles/
├── main.py                     # Game launcher (COMPLETE THIS)
├── character_manager.py        # Character creation/management (COMPLETE THIS)
├── inventory_system.py         # Item and equipment management (COMPLETE THIS)
├── quest_handler.py            # Quest system (COMPLETE THIS)
├── combat_system.py            # Battle mechanics (COMPLETE THIS)
├── game_data.py                # Data loading and validation (COMPLETE THIS)
├── custom_exceptions.py        # Exception definitions (PROVIDED)
├── data/
│   ├── quests.txt             # Quest definitions (PROVIDED)
│   ├── items.txt              # Item database (PROVIDED)
│   └── save_games/            # Player save files (created automatically)
├── tests/
│   ├── test_module_structure.py       # Module organization tests
│   ├── test_exception_handling.py     # Exception handling tests
│   └── test_game_integration.py       # Integration tests
└── README.md                   # This file
```

### Step 3: Development Workflow

```bash
# Work on one module at a time
# Test your code frequently

# Commit and push to see test results
git add .
git commit -m "Implement character_manager module"
git push origin main

# Check GitHub for test results (green checkmarks = passed!, red xs = at least 1 failed test case. Click the checkmark or x and then "Details" to see what test cases passed/failed)
```

## Core Requirements (60 Points)

### Critical Constraint
You may **only** use concepts covered through the **Exceptions and Modules** chapters. 

### 🎨 Creativity and Customization

This project encourages creativity! Here's what you can customize:

**✅ FULLY CUSTOMIZABLE:**
- **Character stats** - Adjust health, strength, magic for balance
- **Enemy stats** - Make enemies easier or harder
- **Special abilities** - Design unique abilities for each class
- **Additional enemies** - Add your own enemy types beyond the required three
- **Game mechanics** - Add status effects, combos, critical hits, etc.
- **Quest rewards** - Adjust XP and gold amounts
- **Item effects** - Create unique items with creative effects

**⚠️ REQUIRED (for testing):**
- **4 Character classes:** Warrior, Mage, Rogue, Cleric (names must match exactly)
- **3 Enemy types:** "goblin", "orc", "dragon" (must exist, stats flexible)
- **All module functions** - Must have the specified function signatures
- **Exception handling** - Must raise appropriate exceptions

**💡 CREATIVITY TIPS:**
1. Start with required features working
2. Add creative elements incrementally
3. Test after each addition
4. Be ready to explain your design choices in the interview
5. Bonus interview points for thoughtful, balanced customization!

**Example Creative Additions:**
- Vampire enemy that heals when attacking
- Warrior "Last Stand" ability that activates when health is low
- Poison status effect that deals damage over time
- Critical hit system based on character stats
- Rare "legendary" weapons with special effects

### Module 1: custom_exceptions.py (PROVIDED - 0 points to implement)

**This module is provided complete.** It defines all custom exceptions you'll use throughout the project.

### Module 2: game_data.py (10 points)

### Module 3: character_manager.py (15 points)

### Module 4: inventory_system.py (10 points)

### Module 5: quest_handler.py (10 points)

### Module 6: combat_system.py (10 points)

### Module 7: main.py (5 points)

## Automated Testing & Validation (60 Points)

## Interview Component (40 Points)

**Creativity Bonus** (up to 5 extra points on interview):
- Added 2+ custom enemy types beyond required three
- Designed unique and balanced special abilities
- Implemented creative game mechanics (status effects, advanced combat, etc.)
- Thoughtful stat balancing with clear reasoning

**Note:** Creativity is encouraged, but functionality comes first! A working game with required features scores higher than a broken game with lots of extras.

### Update README.md

Document your project with:

1. **Module Architecture:** Explain your module organization
The game_data module acts as the Data Layer, managing file loading, parsing, and strict validation of all game assets (quests and items). The character_manager (implied) oversees the Game State, handling character creation and attribute updates. Finally, the quest_handler module contains the Game Logic, enforcing rules for accepting, progressing, and rewarding quests by coordinating data from the other modules. This structure enhances readability, maintainability, and testing by preventing logic from being tightly coupled.

3. **Exception Strategy:** Describe when/why you raise specific exceptions
Throughout each module I chose the most critical and/or relevant exceptions for the instance to make sure that the game proceeded without any hiccups. I did this to make sure there were no critical failures throughout. Within the game_data.py module, exceptions like MissingDataFileError and InvalidDataFormatError signal critical issues related to file access and malformed data structure (e.g., a string found where an integer is expected), preventing the game from loading corrupt information. In the quest_handler.py module, exceptions like InsufficientLevelError and QuestRequirementsNotMetError enforce core game rules, immediately stopping the player's attempt to accept a quest if prerequisites like level or prerequisite quest completion aren't satisfied.
5. **Design Choices:** Justify major decisions
The project's design is justified by key decisions focused on usability and integrity. A major choice is data normalization, specifically converting raw file strings like 'health:20' into structured Python dictionaries {'stat': 'health', 'value': 20} during the load phase, which greatly simplifies game logic and prevents runtime errors. Another crucial decision is using custom exceptions (e.g., InsufficientLevelError, InvalidDataFormatError) , which allows the code to signal specific failures clearly and enables graceful error handling in the main game loop. Finally, adhering to Separation of Concerns by placing quest acceptance rules in the quest_handler.py (logic) and leaving file structure checks to game_data.py (data) ensures that each module has a single, testable responsibility.
7. **AI Usage:** Detail what AI assistance you used
8. Gemini AI used throughout all files to identify and fix bugs as well as
explain how the code fails the test cases.
Ai was mostly used to fix issues in game_data and quest_hgandler modules.

9. **How to Play:** Instructions for running the game
First, ensure you have Python 3.x installed and that all necessary module files (game_data.py, quest_handler.py, etc.) are present in your project directory. Second, confirm that the data directory contains the required game content files (like quests.txt and items.txt); the game may automatically create these defaults if they are missing. Finally, to launch the application, open your terminal, navigate to the project's root folder, and execute the main game file (typically main.py) using the command: python main.py. This initiates the game's sequence, starting with data loading, character creation, and entering the main text-based game loop.
### What to Submit:

1. **GitHub Repository:** Your completed multi-module project
2. **Interview:** Complete 10-minute explanation session
3. **README:** Updated documentation

## Protected Files Warning

⚠️ **IMPORTANT: Test Integrity**

Test files are provided for your learning but are protected. Modifying test files constitutes academic dishonesty and will result in:

- Automatic zero on the project
- Academic integrity investigation

You can view tests to understand requirements, but any modifications will be automatically detected.
