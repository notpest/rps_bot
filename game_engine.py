import random
from typing import Dict

class GameEngine:
    VALID_MOVES = ["rock", "paper", "scissors", "bomb"]
    
    def __init__(self):
        self.round_count: int = 0
        self.max_rounds: int = 3
        self.scores: Dict[str, int] = {"user": 0, "bot": 0}
        self.bomb_state: Dict[str, bool] = {"user": False, "bot": False}
        self.game_over: bool = False

    def _get_bot_move(self) -> str:
        options = ["rock", "paper", "scissors"]
        # Bot uses bomb intelligently (10% chance) only if allowed
        if not self.bomb_state["bot"]:
            if random.random() < 0.1: 
                options.append("bomb")
        
        move = random.choice(options)
        if move == "bomb": self.bomb_state["bot"] = True
        return move

    def _resolve_round(self, user_move: str, bot_move: str) -> str:
        if user_move == bot_move: return "DRAW"
        
        # Bomb Mechanics
        if user_move == "bomb": return "USER"
        if bot_move == "bomb": return "BOT"
            
        wins_against = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        if wins_against.get(user_move) == bot_move:
            return "USER"
        return "BOT"

    def process_turn(self, user_input: str) -> Dict[str, str]:
        if self.game_over:
            return {"status": "error", "message": "Game Over."}

        raw_input = user_input.lower().strip()
        bot_move = self._get_bot_move()
        round_winner = ""
        narrative_reason = ""

        # 1. Invalid Input (Waste Rule)
        if raw_input not in self.VALID_MOVES:
            self.round_count += 1
            self.scores["bot"] += 1
            round_winner = "BOT (Forfeit)"
            narrative_reason = f"Invalid move '{raw_input}' wastes the round."
            # Bot move is irrelevant in a waste, but we record it was ready
            bot_move = "(N/A)"

        # 2. Illegal Bomb (Waste Rule)
        elif raw_input == "bomb" and self.bomb_state["user"]:
            self.round_count += 1
            self.scores["bot"] += 1
            round_winner = "BOT (Penalty)"
            narrative_reason = "User tried to use Bomb twice."
            bot_move = "(N/A)"

        # 3. Valid Play
        else:
            if raw_input == "bomb": self.bomb_state["user"] = True
            
            self.round_count += 1
            # Resolve
            result = self._resolve_round(raw_input, bot_move)
            round_winner = result
            
            if result == "USER":
                self.scores["user"] += 1
                narrative_reason = f"{raw_input.title()} beats {bot_move.title()}"
            elif result == "BOT":
                self.scores["bot"] += 1
                narrative_reason = f"{bot_move.title()} beats {raw_input.title()}"
            else:
                narrative_reason = "Moves were identical"

        # 4. End Game Check
        final_result = ""
        if self.round_count >= self.max_rounds:
            self.game_over = True
            if self.scores["user"] > self.scores["bot"]:
                final_result = "USER WINS"
            elif self.scores["bot"] > self.scores["user"]:
                final_result = "BOT WINS"
            else:
                final_result = "DRAW"

        return {
            "round": str(self.round_count),
            "user_move": raw_input,
            "bot_move": bot_move,
            "round_winner": round_winner,
            "reason": narrative_reason,
            "score_user": str(self.scores["user"]),
            "score_bot": str(self.scores["bot"]),
            "game_over": str(self.game_over),
            "final_result": final_result
        }