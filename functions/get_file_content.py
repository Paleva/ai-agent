import os
from google.genai import types

def get_file_content(working_dir, file_path=None):

    absolute_working_dir = os.path.abspath(working_dir)
    absolute_directory = os.path.abspath(os.path.join(absolute_working_dir, file_path or '.'))
    
    if not absolute_directory.startswith(absolute_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(absolute_directory):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(absolute_directory, 'r') as file:
        MAX_SIZE = 10000
        char = 0
        try:
            content = file.read()
            if content:
                char = len(content)
                if char <= MAX_SIZE:
                    return content
                else:
                    # If the file is too large, return an error message
                    content = content[:MAX_SIZE] + f'[...File "{file_path}" truncated at 10000 characters...]'
                    print(content)
            return content
        except Exception as e:
            return f'Error reading file: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file within the working directory, returning up to 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory. If not provided, defaults to None",
            ),
        },
    ),
)