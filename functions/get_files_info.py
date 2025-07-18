import os
from google.genai import types


def get_files_info(working_dir, directory=None):

    absolute_working_dir = os.path.abspath(working_dir)
    absolute_directory = os.path.abspath(os.path.join(absolute_working_dir, directory or '.'))

    if not absolute_directory.startswith(absolute_working_dir):
        return f"Error: Directory {absolute_directory} is not within the working directory {absolute_working_dir}."
    
    if not os.path.isdir(absolute_directory):
        return f"Error: Directory {absolute_directory} does not exist."

    dir = os.listdir(absolute_directory)
    dir_contents = ""

    for item in dir:
        file_path = os.path.join(absolute_directory, item)
        file_size = os.path.getsize(file_path)
        file_name = item
        is_dir = os.path.isdir(file_path)
        dir_contents += f'- {file_name}: file_size={file_size} bytes, is_dir={is_dir}\n'
    return dir_contents


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
