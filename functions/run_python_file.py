import os
import subprocess

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, file_path))

        common_path = os.path.commonpath([absolute_path, target_path]) == absolute_path
        if not common_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        is_file = os.path.isfile(target_path)
        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args is not None:
            command.extend(args)

        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        
        output_string = ''
        
        if process.returncode != 0:
            output_string += f'Process exited with code {process.returncode}'
        
        if process.stdout is None and process.stderr is None:
            output_string += f'No output produced'

        output_string += f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}'

    except Exception as e:
        return f'Error: executing Python file: {e}'

    return output_string