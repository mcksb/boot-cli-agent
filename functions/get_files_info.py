import os

def get_files_info(working_directory, directory="."):
    
    is_valid_directory = os.path.isdir(directory)
    if is_valid_directory == False:
        raise Exception(f'Error: "{directory}" is not a directory')

    absolute_path = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(absolute_path, directory))
    
    # Will be True or False
    valid_target_dir = os.path.commonpath([absolute_path, target_directory]) == absolute_path
    
    if valid_target_dir == False:
        raise Exception(f'Error: Cannot list {directory} as it is outside the permitted working directory')

    return