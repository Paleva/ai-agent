import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv


def generate_content(client, message, debug=False):
    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=message
    )
    print(res.text)
    if debug:
        print("Prompt tokens:", res.usage_metadata.prompt_token_count)
        print("Response tokens:", res.usage_metadata.candidates_token_count)

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