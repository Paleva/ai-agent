from google.genai import types
from config.available_functions import available_functions
from config.system_prompt import SYSTEM_PROMPT
from call_function import call_function

def generate_content(client, message, debug=False):
    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=message,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )

    function_response_list = []
    if not res.function_calls:
        print(res.text)
        return
    
    for function_call in res.function_calls:
        function_response = call_function(function_call, verbose=True)
        
        if not function_response.parts[0].function_response.response:
            raise Exception('Function response is empty. Please check the function implementation.')
        
        if debug:
            print(f"-> {function_response.parts[0].function_response.response}")

        function_response_list.append(function_response.parts[0].function_response.response)
        
    if debug:
        print("Prompt tokens:", res.usage_metadata.prompt_token_count)
        print("Response tokens:", res.usage_metadata.candidates_token_count)