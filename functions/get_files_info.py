import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.join(working_directory, directory)
        full_path = os.path.abspath(full_path)

        #Validate Existence of Directory
        if not os.path.exists(working_directory):
            return f"Error: The path '{directory}' is not a directory."
        if not os.path.exists(full_path):
            return f"Error: The directory '{full_path}'does not exist."
        if not os.path.isdir(full_path):
            return f"Error: The path '{full_path}' is not a directory."
        

        #ensure directory is within working_directory
        if os.path.commonpath([working_directory, full_path]) != working_directory:
            return f"Error: '{full_path}' is outside of '{working_directory}'."

        #Gets File Info
        files_info = []
        file_names = os.listdir(full_path)
        for file_name in file_names:
            file_path = os.path.join(full_path, file_name)
            file_info = {
                "name": file_name,
                "size": os.path.getsize(file_path) if os.path.isfile(file_path) else None,
                "is_dir": os.path.isdir(file_path),
            }
            files_info.append(file_info)
        report = []
        for i in range(len(files_info)):
            report.append(f"{files_info[i]['name']}: file_size={files_info[i]['size']}, is_dir={files_info[i]['is_dir']}")
        
        return "\n".join(report)
    except Exception as e:
        return f"Error: {e}"