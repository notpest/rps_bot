from google import genai
from google.genai import types
from tools import game_tools

class LlmAgent:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        
        self.system_prompt = """
        You are the Referee for a game of Rock, Paper, Scissors.
        
        ### GAME RULES
        1. Best of 3 rounds.
        2. 'Bomb' beats everything but can be used only ONCE per player.
        3. Invalid moves waste the round (User loses the round immediately).
        
        ### YOUR JOB
        1. Receive the user's move.
        2. CALL THE TOOL `submit_move`.
        3. Render the tool's output using the STRICT format below.

        ### MANDATORY OUTPUT FORMAT
        For every turn, your response must look exactly like this:

        **Round [round from tool]**
        * **Moves:** You: [user_move] | Me: [bot_move]
        * **Winner:** [round_winner]
        * **Reason:** [reason]
        
        **Current Score:** User [score_user] - Bot [score_bot]

        [If 'game_over' is "False":]
        ---------------------
        **Round [round + 1] Begins.** Enter your move:

        [If 'game_over' is "True":]
        ---------------------
        *** FINAL RESULT: [final_result] ***
        """
        
        self.conf = types.GenerateContentConfig(
            tools=game_tools,
            system_instruction=self.system_prompt,
            temperature=0.1, 
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
        )
        
        self.chat = self.client.chats.create(
            model='gemini-2.5-flash',
            config=self.conf
        )

    def send_message(self, message: str) -> str:
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"System Error: {str(e)}"