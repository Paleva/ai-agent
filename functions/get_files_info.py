import os


def get_files_info(working_dir, directory=None):

    absolute_working_dir = os.path.abspath(working_dir)
    absolute_directory = os.path.join(absolute_working_dir, directory)

    print(f"Working Directory: {absolute_working_dir}")
    print(f"Directory: {absolute_directory}")

    if not absolute_directory.startswith(absolute_working_dir):
        return f"Directory {absolute_directory} is not within the working directory {absolute_working_dir}."
    
    if not os.path.exists(absolute_directory):
        return f"Directory {absolute_directory} does not exist."

    dir = os.listdir(absolute_directory)
    return dir

print(get_files_info("calculator", "pkg"))