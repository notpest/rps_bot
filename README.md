# Rock-Paper-Scissors (RPS) Referee

A minimal, ADK-compliant AI Game Referee built with Python and the **Google Gen AI SDK**.

## 1. State Model
The game state is strictly deterministic and isolated from the LLM to prevent hallucinations. It is managed by a Python class, `GameEngine`, which tracks:
* **Global Counters:** `round_count` (0-3), `scores` ({user, bot}).
* **Bomb Logic:** `bomb_state` ({user, bot}) — A boolean flag ensuring the "Bomb" move is used only once per player.
* **Game Status:** `game_over` boolean.

**Key Rule Implementation:**
* **The "Waste" Rule:** Invalid inputs do not prompt a retry; they strictly increment the round counter and award a point to the Bot (Forfeit).
* **Bomb Persistence:** The engine refuses to accept a second "bomb" input from a player who has already used it, penalizing them with a wasted round.

## 2. Agent & Tool Design
The architecture follows the **Runner Pattern**, separating Intent (Agent) from Logic (Engine).

* **The Agent (Gemini 2.5 Flash):**
    * Acts **only** as the interface and narrator.
    * Possesses **no internal game logic**.
    * **System Prompt:** Enforces a strict Markdown template for responses (`**Round X**`, `**Winner:**`, etc.) to ensure consistent, parseable output.
    * **Configuration:** Temperature set to `0.1` to minimize creativity and maximize adherence to the data returned by the tool.

* **The Tool (`submit_move`):**
    * The single bridge between the Agent and the Engine.
    * Takes the raw user string.
    * Returns a structured dictionary (Winner, Reason, Score, Game Over Status).

## 3. Tradeoffs
* **Singleton State:** The current implementation uses a global instance of `GameEngine` in `tools.py`. This works perfectly for a local CLI `Runner`, but it is not thread-safe for a concurrent web server (multiple users would overwrite each other's game state).
* **CLI UX:** The game runs in a blocking `input()` loop. A production version would likely use an event-driven websocket or REST API.
* **Strictness vs. Helpfulness:** To strictly adhere to the "invalid input wastes round" rule, the bot is "mean." It does not clarify *why* a move is invalid before punishing the user, which is a harsh User Experience but fulfills the logic constraints.

## 4. Future Improvements
With more time, I would implement:
1.  **Session Management:** Replace the global singleton with a `SessionManager` class that creates unique `GameEngine` instances keyed by a `user_id`, enabling multi-user support.
2.  **Unit Testing:** Add `pytest` coverage specifically for edge cases (e.g., User plays Bomb, then plays Bomb again; User plays 'Spock').
3.  **Persistence:** Serialize the `GameEngine` state to a lightweight database (SQLite) so a game can be resumed if the script crashes.