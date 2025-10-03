from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
from google import genai
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def call_function(function_call, verbose=False):
    working_directory = "./calculator"  # Set your working directory here
    args = function_call.args
    try:
        if verbose:
            print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(f" - Calling function: {function_call.name}")
        if function_call.name == "get_files_info":
            directory = args.get("directory", ".") if args else "."
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name="get_files_info",
                        response={"result": get_files_info(working_directory, directory)},
                    )
                ],
            )
        elif function_call.name == "get_file_content":
            file_path = args.get("file_path") if args else None
            if not file_path:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name="get_file_content",
                            response={"error": "Error: 'file_path' argument is required."},
                        )
                    ],
                )
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name="get_file_content",
                        response={"result": get_file_content(working_directory, file_path)},
                    )
                ],
            )
        elif function_call.name == "write_file":
            file_path = args.get("file_path") if args else None
            content = args.get("content") if args else None
            if not file_path or content is None:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name="write_file",
                            response={"error": "Error: 'file_path' and 'content' arguments are required."},
                        )
                    ],
                )
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name="write_file",
                        response={"result": write_file(working_directory, file_path, content)},
                    )
                ],
            )
        elif function_call.name == "run_python_file":
            file_path = args.get("file_path") if args else None
            file_args = args.get("args", []) if args else []
            if not file_path:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name="run_python_file",
                            response={"error": "Error: 'file_path' argument is required."},
                        )
                    ],
                )

            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name="run_python_file",
                        response={"result": run_python_file(working_directory, file_path, file_args)},
                    )
                ],
            )
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call.name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Exception during {function_call.name}: {e}"},
                )
            ],
        )

            

