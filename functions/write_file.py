import os
from google.genai import types

def write_file(working_dir, file_path, content):

    absolute_working_dir = os.path.abspath(working_dir)
    absolute_directory = os.path.abspath(os.path.join(absolute_working_dir, file_path or '.'))

    if not absolute_directory.startswith(absolute_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(absolute_directory, 'w') as file:
            file.write(content)
        return f'Succesfully wrote to "{file_path}" {len(content)} characters written'
    except Exception as e:
        return f'Error: {str(e)}'
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)
