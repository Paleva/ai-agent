import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config.available_functions import available_functions
from config.system_prompt import SYSTEM_PROMPT
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from generate_content import generate_content

def main():
    load_dotenv()
    API_KEY = os.environ.get("GEMINI_API_KEY")
    args = sys.argv[1:]
    DEBUG = None

    if len(sys.argv) == 1:
        print("Usage: python main.py <prompt>")
        sys.exit(1)

    if "--verbose" in args:
        DEBUG = True

    prompt = str(sys.argv[1])
    messages = [
        types.Content(role='user', parts=[types.Part(text=prompt)]),
    ]
    client = genai.Client(api_key=API_KEY)

    if DEBUG:
        print("User prompt:", prompt)

    generate_content(client, messages, debug=DEBUG)
    


if __name__ == "__main__":
    main()