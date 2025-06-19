import os
import subprocess

def run_python_file(working_dir, file_path):
    absolute_working_dir = os.path.abspath(working_dir)
    absolute_directory = os.path.abspath(os.path.join(absolute_working_dir, file_path or '.'))

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