import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

def generate_content(client, message, debug=False):
    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=message,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )

    print(res.text)
    for function_call in res.function_calls:
        print(f"Function call: {function_call.name} with arguments {function_call.args}")
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