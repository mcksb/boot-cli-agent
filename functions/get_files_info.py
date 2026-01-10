import os

def get_files_info(working_directory, directory="."):
    wd_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(wd_path, directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([wd_path, target_dir]) == wd_path
    if valid_target_dir == False:
        raise Exception(f'Error: Cannot list {directory} as it is outside the permitted working directory') 