# Capture The Flag (Python / Pygame)

## Overview

Capture The Flag is a small platformer game built with **Python and Pygame**. The objective of the game is to capture the flag and return it to your base while avoiding enemies and obstacles.

The player must navigate platforms, avoid bullets, and survive long enough to bring the flag back safely.

## Features

* Platform-based movement with jumping and gravity
* Enemy AI that chases the player
* Turret guns that shoot bullets
* Increasing difficulty as the score increases
* Score, timer, and life system
* Level selection at the start screen


## OOP Structure

The game uses several classes to organize game logic:

- **Player** – Handles player movement, jumping, and flag interaction.
- **Enemy** – AI enemy that chases the player and becomes stronger as the score increases.
- **Platform** – Represents platforms that the player and enemy can stand on.
- **Bullet / EnemyBullet** – Projectiles fired by turrets or enemies.
- **Gun** – Stationary turrets that shoot bullets at intervals.
- **Flag** – The object the player must capture and return to base.
- **Game** – Controls the main game loop, updates, rendering, and game state.


## Game Objective

1. Move across the platforms to reach the flag.
2. Pick up the flag.
3. Return it to your base on the left side of the map.
4. Each successful capture increases the score and enemy difficulty.

## Controls

| Key                      | Action                  |
| ------------------------ | ----------------------- |
| **A / Left Arrow**       | Move left               |
| **D / Right Arrow**      | Move right              |
| **W / Up Arrow / Space** | Jump                    |
| **Enter**                | Start the game          |
| **R**                    | Restart after game over |
| **Q**                    | Quit the game           |

## Requirements

Make sure Python and Pygame are installed.

Install Pygame with:

```bash
pip install pygame
```

## Running the Game

Run the game using:

```bash
python main.py
```

## Project Structure

```
main.py       - Main game file
README.md     - Project description
```

## Technologies Used

* Python
* Pygame


## AI Assistance

Some AI tools were used during development to help debug code, improve structure, and generate documentation. All code was reviewed and understood before being included in the project.