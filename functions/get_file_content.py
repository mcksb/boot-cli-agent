from config import *
import os

def get_file_content(working_directory, file_path):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, file_path))
    
        is_file = os.path.isfile(target_path)
        if not is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        common_path = os.path.commonpath([absolute_path, target_path]) == absolute_path
        if not common_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        with open(target_path, 'r') as f:
            file_content = f.read(MAX_CHARS)
        
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    except Exception as e:
        return f'Error: {e}'
    
    return file_content