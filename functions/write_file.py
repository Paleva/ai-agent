import os

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
