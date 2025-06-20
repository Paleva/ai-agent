from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

WORKING_DIR = './calculator'


def call_function(function_call_part: types.FunctionCall, verbose=False):
    if verbose:
        print(f" - Calling function: {function_call_part.name} with arguments {function_call_part.args}")

    functions = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call_part.name
    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown '{function_name}'"}
                )
            ]
        )
    function_args = dict(function_call_part.args)
    function_args['working_dir'] = WORKING_DIR
    function_result = functions[function_name](**function_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result}
            )
        ]
    )
