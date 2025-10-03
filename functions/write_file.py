import os
from functions.get_files_info import get_files_info
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory. Replaces existing content if file exists. Creates the file if it does not exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
def write_file(working_directory, file_path, content):
    try:
        #Validation
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)
        working_directory = os.path.abspath(working_directory)

        if os.path.commonpath([working_directory, full_path]) != working_directory:
            return f"Error: Cannot write to '{full_path}' as it is outside the permitted working directory."
        if not os.path.exists(working_directory):
            return f"Error: The working directory '{working_directory}' does not exist."
        if not os.path.isdir(working_directory):
            return f"Error: The working directory '{working_directory}' is not a directory."
        
        if not os.path.exists(full_path):
            # Creates neccessary directories if they don't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write content to file, replaces existing content
        with open(full_path, 'w') as f:
            f.write(content)
        if get_files_info(working_directory, os.path.dirname(full_path)).startswith("Error"):
            return f"Error: Failed to write to {full_path}."
        return f"Successfully wrote to '{full_path}' ({len(content)} characters written)"
    except Exception as e:
        return f"Error: {e}"
