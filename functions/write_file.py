import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The specified file path to write content. Relative to the current working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the specified file path.",
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, file_path))
    
        is_dir = os.path.isdir(target_path)
        if is_dir == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        common_path = os.path.commonpath([absolute_path, target_path]) == absolute_path
        if common_path != True:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        os.makedirs(file_path, exist_ok=True)
        with open(target_path, 'w') as f:
            f.write(content)

    except Exception as e:
        return f'Error: {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'