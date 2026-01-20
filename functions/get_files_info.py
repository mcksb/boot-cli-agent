import os

def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, directory))
        
        is_directory = os.path.isdir(target_path)
        if is_directory != True:
            return f'Error: "{directory}" is not a directory'

        common_path = os.path.commonpath([absolute_path, target_path]) == absolute_path
        if common_path != True:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        directory_contents = os.listdir(target_path)
        file_info = ''
        for file in directory_contents:
            file_path = os.path.join(target_path, file)
            file_name = file
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            file_info = file_info + f'- {file}: file_size={file_size}, is_dir={is_dir}\n'
    
    except Exception as e:
        return f'Error: {e}'
    
    return file_info