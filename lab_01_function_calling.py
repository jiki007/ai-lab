import os
import random
from google import genai
from google.genai import types
from dotenv import load_dotenv
import platform

# 1. Load Credentials
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key not found in .env file")
    exit()
client = genai.Client(api_key=api_key)

# --- 🛠️ THE TOOLS ---
# Regular Python functions. The new SDK reads the type hints automatically!

def basic_calculator(a: int, b: int, operation: str) -> int:
    """
    Performs basic math. 
    Args:
        a: First number
        b: Second number
        operation: 'add', 'subtract', 'multiply', 'power'
    """
    print(f"\n[SYSTEM] ⚙️ TOOL ACTIVE: Calculator running {a} {operation} {b}...")
    if operation == 'add': return a + b
    elif operation == 'subtract': return a - b
    elif operation == 'multiply': return a * b
    elif operation == 'power': return a ** b
    return 0

def flip_coin() -> str:
    """
    Flips a coin to help decide. Returns 'Heads' or 'Tails'.
    """
    print("\n[SYSTEM] ⚙️ TOOL ACTIVE: Flipping a coin...")
    return random.choice(['Heads', 'Tails'])

def get_system_info() -> str:
    """
    Returning your current OS and Python version.
    """
    print("\n[SYSTEM ⚙️ TOOL ACTIVE: Identifying the OS and Python version....]")
    return f"OS: {platform.system()} {platform.release()}, Python: {platform.python_version()}"

# --- 🧠 THE BRAIN ---
print("--- 🟢 LEVEL 1 LAB: Function Calling (Modern SDK) ---")

# Create the chat session with tools attached
chat = client.chats.create(
    model='gemini-2.5-flash',
    config=types.GenerateContentConfig(
        tools=[basic_calculator, flip_coin, get_system_info], # Pass functions directly
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=False # This enables the AI to run the code itself
        )
    )
)

print("System Ready. Try: 'What is 5 to the power of 4?' or 'Flip a coin'")

while True:
    try:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        response = chat.send_message(user_input)
        
        print(f"AI: {response.text}")
        
    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"Error: {e}")