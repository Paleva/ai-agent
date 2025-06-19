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


def call_function(function_call_part: types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name} with arguments {function_call_part.args}")

    print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    function_args = function_call_part.args
    print(function_args)
    if function_name == "get_file_content":
        function_result = get_file_content('./calculator', **function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result}
                )
            ]
        )
    elif function_name == "get_files_info":
        function_result = get_files_info('./calculator', **function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result}
                )
            ]
        )
    elif function_name == "run_python_file":
        function_result = run_python_file('./calculator',**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result}
                )
            ]
        )
    elif function_name == "write_file":
        function_result = write_file('./calculator',**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result}
                )
            ]
        )
    else:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_name},
            )
        ],
)


def generate_content(client, message, debug=False):
    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=message,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )

    
    if not res.function_calls:
        print(res.text)
        return
    
    for function_call in res.function_calls:
        function_response = call_function(function_call, verbose=True)
        
        if not function_response.parts[0].function_response.response:
            raise Exception('Function response is empty. Please check the function implementation.')
        
        print(f"-> {function_response.parts[0].function_response.response}")
        
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