import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

model = "gemini-2.5-flash"
prompt = args.user_prompt

def main():
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    res = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    if not res.usage_metadata:
        raise RuntimeError("API request failed: Usage metadata is None")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
    
    if not res.function_calls:
        print("Response:")
        print(res.text)
        return

    function_results = []
    for function in res.function_calls:
        call_function_result = call_function(function, args.verbose)
        
        if not call_function_result.parts:
            raise Exception("call_function_results.parts is empty")
        
        if not call_function_result.parts[0].function_response:
            raise Exception("parts[0].function_response is None")
        
        if not call_function_result.parts[0].function_response.response:
            raise Exception("parts[0.function_response.response is None]")
        
        function_results.append(call_function_result.parts[0])
        
        if args.verbose:
            print(f"-> {call_function_result.parts[0].function_response.response}")
    
if __name__ == "__main__":
    main()
