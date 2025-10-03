import os
import json

from dotenv import load_dotenv
import sys
from config import system_prompt
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("Using API key:", api_key)

from google import genai
from google.genai import types
from functions.function_caller import available_functions, call_function





if api_key is None:
    raise ValueError("No GEMINI_API_KEY set in environment")

client = genai.Client(api_key=api_key)

def extract_response_text(response):
    if response is None:
        return "Error: No response (possibly rate limited)."
    
    if not hasattr(response, "candidates"):
        return "Error: Invalid response object (rate limit or other error)."
    texts = []
    for cand in response.candidates:
        if not cand.content:
            continue
        for part in cand.content.parts:
            if hasattr(part, "text") and part.text:
                texts.append(part.text)
            elif hasattr(part, "function_response") and part.function_response:
                texts.append(json.dumps(part.function_response, indent=2))
    return "\n".join(texts) if texts else None

def call_gemini(messagehistory, verbose):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messagehistory,
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt
            )
        )
        limiter = 0

        while limiter < 20:
            function_called = False

            for part in response.candidates[0].content.parts:
                if part.function_call:
                    function_called = True
                    fn_call = part.function_call

                    fn_result = call_function(fn_call, verbose=verbose)
                    if not fn_result:
                        return f"Error calling function {fn_call.name}"

                    if not isinstance(fn_result, dict):
                        fn_result = {"result": str(fn_result)}

                    tool_response = types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=fn_call.name,
                                response=fn_result
                            )
                        ]
                    )

                    messagehistory.append(tool_response)

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=messagehistory,
                        config=types.GenerateContentConfig(
                            tools=[available_functions], 
                            system_instruction=system_prompt
                        )
                    )

                    limiter += 1
            if not function_called:
                break

        return response  #Always return a response

    except Exception as e:
        if verbose:
            print("Error occured when calling gemini:", e)
        return None

def main():
    messagehistory = []

    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in {"quit", "exit"}:
            break

        # add user input to history
        user_message = types.Content(role="user", parts=[types.Part(text=prompt)])
        messagehistory.append(user_message)

        # call Gemini with full history
        response = call_gemini(messagehistory, verbose=True)

        # extract text
        response_text = extract_response_text(response)
        print("Gemini:", response_text)

        # add Gemini response to history
        if response.candidates and response.candidates[0].content:
            messagehistory.append(response.candidates[0].content)

if __name__ == "__main__":
    main()
