import os
from config import MAX_FILE_CHARS
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content of a file up to the character limit(default is 10000), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get content from, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)

        #Validate Existence of File
        if not os.path.exists(working_directory):
            return f"Error: The path '{working_directory}' is not a directory."
        if not os.path.exists(full_path):
            return f"Error: The file '{full_path}' does not exist."
        if not os.path.isfile(full_path):
            return f"Error: The path '{full_path}' is not a file."

        #Ensure file is within working_directory
        if os.path.commonpath([working_directory, full_path]) != working_directory:
            return f"Error: '{full_path}' is outside of '{working_directory}'."

        #Read File Content
        with open(full_path, 'r') as file:
            content = file.read()
            if len(content) > MAX_FILE_CHARS:
                content = content[:MAX_FILE_CHARS] + f"\n[File '{file_path}' truncated at {MAX_FILE_CHARS} characters]"

        return content
    except Exception as e:
        return f"Error: {e}"
