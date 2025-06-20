import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from generate_content import generate_content
from call_function import call_function

def main():
    load_dotenv()
    API_KEY = os.environ.get("GEMINI_API_KEY")
    args = sys.argv[1:]
    DEBUG = None

    if len(sys.argv) == 1:
        print("Usage: python main.py <prompt> [--verbose]")
        print("Example: python3 main.py 'What is the capital of France?' --verbose")
        print("Example: python3 main.py 'Run tests.py'")
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
    
    response = None
    for i in range(20):
        function = False
        response = generate_content(client, messages, debug=DEBUG)
        for candidate in response.candidates:
            messages.append(candidate.content)
            for part in candidate.content.parts:
                if part.function_call:
                    function = True
                    function_response = call_function(part.function_call, verbose=DEBUG)
                    messages.append(function_response)
                    if DEBUG:
                        print("Function response:", function_response)
        if not function:
            break

        
    print("FINAL:", response.text)

    


if __name__ == "__main__":
    main()