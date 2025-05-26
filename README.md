# Stimulation Clicker

Stimulation Clicker is an engaging incremental clicker game built with Python and Pygame. Click your way to higher energy levels, unlock powerful upgrades, and discover exciting new game mechanics!

## 🎮 Features

*   **Core Clicking:** Click the main button to generate energy.
*   **Manual Click Upgrades:** Purchase upgrades to increase the energy gained per click (e.g., +1, +5, +10, up to +50).
*   **Auto-Clicker:** Unlock an auto-clicker that passively generates energy for you.
    *   Upgrade its power (energy per auto-click).
    *   Upgrade its speed (how frequently it auto-clicks).
*   **Bouncing Ball:** Unlock a bouncing ball that generates energy every time it hits the screen edges.
    *   Upgrade the amount of energy gained per bounce.
*   **Critical Clicks:** Unlock the ability for your manual clicks to become critical hits!
    *   Upgrade the chance of a critical hit occurring.
    *   Upgrade the multiplier for critical hit energy.
*   **Supernova:** Unleash a powerful Supernova for a massive temporary boost to your click energy!
    *   Manage its duration and cooldown.
    *   Upgrade to reduce the Supernova's cooldown period.
*   **Rhythm Bonus:** Sync your clicks with the 60 BPM background music!
    *   Achieve a streak of rhythmic clicks (at least 5) to earn bonus energy.
    *   The bonus scales with your streak length and base click power.
    *   Visual feedback shows your current rhythm streak.
*   **Visual & Audio Feedback:**
    *   Dynamic particle system that changes during Supernova.
    *   Satisfying sound effects for clicks, upgrades, unlocks, ball bounces, and Supernova activation.
    *   Visual "pressed" effect on the main click button.
    *   Background music to set the mood.
*   **Stats Tracking:**
    *   See your current Energy.
    *   Track your total Clicks.
    *   Monitor your Energy Per Second (EPS).

## 🕹️ How to Play

1.  **Click:** Click the central "Click me!" button to generate energy.
2.  **Upgrade:** Use your accumulated energy to purchase upgrades from the columns below the main button.
    *   **Column 0 (Left):** Manual click power upgrades.
    *   **Column 1:** Unlock new features like the Auto-Clicker, Bouncing Ball, and Critical Hits.
    *   **Column 2:** Upgrade existing features (Auto-Clicker power/speed, Ball bounce power, Critical Hit chance/multiplier, Supernova cooldown).
    *   **Column 3 (Right):** Activate the Supernova when it's ready.
3.  **Discover:** As your energy grows, new upgrades and features will become available.
4.  **Listen:** Try to click in time with the background music (60 BPM, or 1 click per second) to activate the Rhythm Bonus for extra energy!

## 📋 Requirements

*   Python 3.x
*   Pygame library

## 🚀 How to Run

1.  **Ensure Python is installed.** If not, download and install it from [python.org](https://www.python.org/).
2.  **Install Pygame:**
    Open your terminal or command prompt and run:
    ```bash
    pip install pygame
    ```
3.  **Download the Game Files:**
    Clone this repository or download the game files (`Stimulation Clicker redone.py` and the `Audio` folder).
4.  **Run the Game:**
    Navigate to the directory where you saved the files in your terminal and run:
    ```bash
    python "Stimulation Clicker redone.py"
    ```
    (If you rename the main Python file, use that name instead.)

## ✨ Future Ideas

*   More upgrade types
*   Prestige system
*   Visual themes
*   Achievements
*   Offline progress
*   Add more rhythmical elements
*   Upgrading rhythm tempo
*   Unlock more background music to keep track of the rhythm
*   Integrate the python code in a react app with pyodide through react-py


---

Enjoy the stimulation!
