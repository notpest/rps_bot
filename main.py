import os
import sys
from agent import LlmAgent

def main():
    # Load API Key (Ensure GOOGLE_API_KEY is set in your environment)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        sys.exit(1)

    # Initialize Agent
    print("Initializing Referee Agent...")
    agent = LlmAgent(api_key=api_key)

    # Introduction
    print("\n--- Rock-Paper-Scissors ---")
    intro = agent.send_message("Start the game. Explain the rules briefly and ask for the first move.")
    print(f"Referee: {intro}\n")

    # Game Loop
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit']:
                print("Game aborted.")
                break

            # Delegate to Agent
            response = agent.send_message(user_input)
            print(f"Referee: {response}\n")

            from tools import active_engine
            if active_engine.game_over:
                print("--- GAME OVER ---")
                break

        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()