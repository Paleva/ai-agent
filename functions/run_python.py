import os
import subprocess
from google.genai import types

def run_python_file(working_dir, file_path, args=None):
    absolute_working_dir = os.path.abspath(working_dir)
    absolute_directory = os.path.abspath(os.path.join(absolute_working_dir, file_path or '.'))
    print(f"Absolute working directory: {absolute_working_dir}")
    print(f"Absolute directory: {absolute_directory}")
    if not absolute_directory.startswith(absolute_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(absolute_directory):
        return f'Error: File "{file_path}" not found.'

    if not absolute_directory.endswith('.py'):
        return f'Error: File "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ["python3", absolute_directory], 
            capture_output=True,
            text=True,
            cwd=absolute_working_dir, 
            timeout=30
        )
        
        output = []

        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout.strip()}")
        
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr.strip()}")
        
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        return "\n".join(output) if output else "No output from the script."
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python script.",
                ),
                description="Optional arguments to pass to the Python script."
            ),
        },
    )
)