import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python (.py) file within the specified working directory, with optional arguments, and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of string arguments to pass to the Python file during execution.",
            ),
        },
        required=["file_path"],
    ),
)
def run_python_file(working_directory, file_path, args=[]):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.join(working_directory, file_path)
        full_path = os.path.abspath(full_path)

        #Validation
        if not os.path.exists(working_directory):
            return f"Error: The path '{working_directory}' is not a directory."
        if not os.path.exists(full_path):
            return f"Error: The file '{full_path}' not found."
        if not os.path.isfile(full_path):
            return f"Error: The path '{full_path}' is not a file."
        if not full_path.endswith('.py'):
            return f"Error: The file '{full_path}' is not a Python (.py) file."

        #Ensure file is within working_directory
        if os.path.commonpath([working_directory, full_path]) != working_directory:
            return f"Error: Cannot execute '{full_path}' as it is outside the permitted working directory."

        #Execute Python File
        completed_process = subprocess.run(
            ["python3", full_path] + args, #executed command
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30  # Limit execution time to 30 seconds
        )
        return {
            "exit_code": completed_process.returncode,
            "stdout": completed_process.stdout.strip(),
            "stderr": completed_process.stderr.strip(),
        }
        return f"STDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Process timed out."
    except Exception as e:
        return f"Error: {e}"



       