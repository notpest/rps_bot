from typing import Dict
from game_engine import GameEngine

# Global singleton for the active session (Simplification for CLI Runner)
active_engine = GameEngine()

def submit_move(user_move: str) -> Dict[str, str]:
    """
    Submits the user's move to the game engine to resolve the round.
    
    Args:
        user_move: The move attempted by the user (e.g., 'rock', 'paper', 'bomb').
        
    Returns:
        A dictionary containing the results of the round, current score, and game status.
    """
    return active_engine.process_turn(user_move)

# Tool registry list for the Agent
game_tools = [submit_move]