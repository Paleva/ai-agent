from google.genai import types
import google.genai as genai
from config.available_functions import available_functions
from config.system_prompt import SYSTEM_PROMPT
from call_function import call_function

def generate_content(client: genai.Client, messages, debug=False):
    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )
    
    if debug:
        print("Prompt tokens:", res.usage_metadata.prompt_token_count)
        print("Response tokens:", res.usage_metadata.candidates_token_count)
        
    function_response_list = []
    if not res.function_calls:
        return res
    
    # for function_call in res.function_calls:
    #     function_response = call_function(function_call, verbose=debug)
        
    #     if not function_response.parts[0].function_response.response:
    #         raise Exception('Function response is empty. Please check the function implementation.')
        
    #     if debug:
    #         print(f"-> {function_response.parts[0].function_response.response}")

    #     function_response_list.append(function_response.parts[0].function_response.response)
    
    # if not function_response_list:
    #     raise Exception('No function response found. Exiting')
    
    return res
        