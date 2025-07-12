# from dotenv import load_dotenv
# from openai import OpenAI
# import google.generativeai as genai
# import os
# import json

# load_dotenv()

# client=OpenAI()

# def generate_project_structure(cmd:str):
#      result= os.system(cmd)
#      return result

# def install_dependencies(cmd:str):
#     result= os.system(cmd)
#     return result

# def read_file(filepath):
#     if not isinstance(filepath, str):
#         return "❌ read_file expects a file path as a string."
#     if not os.path.exists(filepath):
#         return f"❌ File '{filepath}' does not exist."
#     try:
#         with open(filepath, 'r') as f:
#             return f.read()
#     except Exception as e:
#         return f"❌ Error reading file: {str(e)}"
    
# def write_file(input):
#     if not isinstance(input, dict):
#         return "❌ write_file expects a dict with 'path' and 'content'."
    
#     path = input.get("path")
#     content = input.get("content", "")

#     if not path:
#         return "❌ 'path' is required for write_file"

#     dir_name = os.path.dirname(path)
#     if dir_name:
#         os.makedirs(dir_name, exist_ok=True)

#     try:
#         with open(path, 'w') as f:
#             f.write(content)
#         return f"✅ Wrote {path}"
#     except Exception as e:
#         return f"❌ Error writing file: {str(e)}"

# def update_file(input):
#     if not isinstance(input, dict):
#         return "❌ update_file expects a dict with 'path' and 'modification'."

#     path = input.get("path")
#     update = input.get("modification", "")

#     if not path or not update:
#         return "❌ 'path' and 'modification' required"

#     if not os.path.exists(path):
#         return f"❌ Cannot update. File '{path}' does not exist."

#     try:
#         with open(path, 'r') as f:
#             content = f.read()
#         with open(path, 'w') as f:
#             f.write(content + "\n" + update)
#         return f"✅ Updated {path}"
#     except Exception as e:
#         return f"❌ Error updating file: {str(e)}"
    
# available_tools={
#      "generate_project_structure":generate_project_structure,
#      "install_dependencies":install_dependencies,
#      "read_file":read_file,
#      "write_file":write_file,
#      "update_file":update_file
# }

# SYSTEM_PROMPT = """
# You are an AI Agent specialized in full-stack project development. Your goal is not only to help build projects, but to guide the developer to think critically, plan effectively, and learn while building.

# You operate in a structured loop with the following phases:
# - start: Receive the user's query
# - plan: Break down the task into a step-by-step plan
# - action: Choose and execute one tool from available_tools
# - observe: Wait for the result, then decide next action or output

# Rules:
# - Always perform one step at a time and wait for the next input
# - Carefully analyze the user query and project context
# - Follow the Output JSON format strictly
# - Tool input must match the expected format (see below)
# - After "output", wait for follow-up prompt from user before continuing

# Output JSON Format:
# {
#     "step": "string",
#     "content": "string",
#     "function": "The name of function if the step is action",
#     "input": "The input parameter for the function"
# }

# Available Tools:
# - "generate_project_structure": Executes Linux command (e.g., mkdir, npx, etc.)
#     - Input: A string command
# - "install_dependencies": Installs required packages using npm, pip, etc.
#     - Input: A string command
# - "write_file": Writes content to a specified file path
#     - Input: { "path": "string", "content": "string" }
# - "read_file": Reads and returns content of a file
#     - Input: "file_path" (string)
# - "update_file": Appends or modifies content in a file
#     - Input: { "path": "string", "modification": "string" }
# """


# messages=[
#     {"role":"system","content":SYSTEM_PROMPT}
# ]

# try:
#    while True:
#     query=input(
#         """👋 Welcome to DevAgent!
#              Your terminal coding assistant for full-stack development.
#              Type what you want to build, and I'll help you step by step\n."""
# )
#     messages.append({"role":"user","content":query})
#     while True :
#             response = client.chat.completions.create(
#             model="gpt-4o",
#             response_format={"type": "json_object"},
#             messages=messages
#         )
#             messages.append({ "role": "assistant", "content": response.choices[0].message.content })
         
#             parsed_response = json.loads(response.choices[0].message.content)
         
#             if parsed_response.get("step")== "plan":
#                  print(f"plan :{parsed_response.get('content')}")
#                  continue
#             if parsed_response.get("step")== "action":
#                  tool_name=parsed_response.get("function")
#                  tool_input=parsed_response.get("input")

#                  print(f"🛠️: Calling Tool:{tool_name} with input {tool_input}")

#                  if available_tools.get(tool_name)!=False:
#                   output=available_tools[tool_name](tool_input)
#                   messages.append({ "role": "user", "content": json.dumps({ "step": "observe", "output": output }) })
#                   continue
            
#             if parsed_response.get("step") == "output":
#              print(parsed_response["content"])
#              query = input("🛠️ Would you like to add another feature? ")
#              messages.append({ "role": "user", "content": query })
#              continue

# except KeyboardInterrupt:
#     print("\n👋 Exiting DevAgent. Goodbye!")
#     exit(0)

from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import subprocess
import sys

load_dotenv()

client = OpenAI()

def generate_project_structure(cmd: str):

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Command executed successfully: {cmd}\n{result.stdout}"
        else:
            return f"❌ Command failed: {cmd}\n{result.stderr}"
    except Exception as e:
        return f"❌ Error executing command: {str(e)}"

def install_dependencies(cmd: str):
    """Install dependencies with better output handling"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Dependencies installed: {cmd}\n{result.stdout}"
        else:
            return f"❌ Installation failed: {cmd}\n{result.stderr}"
    except Exception as e:
        return f"❌ Error installing dependencies: {str(e)}"

def read_file(filepath):
   
    if not isinstance(filepath, str):
        return "❌ read_file expects a file path as a string."
    if not os.path.exists(filepath):
        return f"❌ File '{filepath}' does not exist."
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return f"📄 Content of {filepath}:\n{content}"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

def write_file(input):
    
    if not isinstance(input, dict):
        return "❌ write_file expects a dict with 'path' and 'content'."
    
    path = input.get("path")
    content = input.get("content", "")

    if not path:
        return "❌ 'path' is required for write_file"

    # Create directory if it doesn't exist
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ Successfully wrote {path}"
    except Exception as e:
        return f"❌ Error writing file: {str(e)}"

def update_file(input):
   
    if not isinstance(input, dict):
        return "❌ update_file expects a dict with 'path' and 'modification'."

    path = input.get("path")
    update = input.get("modification", "")

    if not path or not update:
        return "❌ 'path' and 'modification' required"

    if not os.path.exists(path):
        return f"❌ Cannot update. File '{path}' does not exist."

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content + "\n" + update)
        return f"✅ Successfully updated {path}"
    except Exception as e:
        return f"❌ Error updating file: {str(e)}"

def list_files(directory="."):
    
    try:
        files = []
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return f"📁 Files in {directory}:\n" + "\n".join(files)
    except Exception as e:
        return f"❌ Error listing files: {str(e)}"

available_tools = {
    "generate_project_structure": generate_project_structure,
    "install_dependencies": install_dependencies,
    "read_file": read_file,
    "write_file": write_file,
    "update_file": update_file,
    "list_files": list_files
}

SYSTEM_PROMPT = """
You are an AI Agent specialized in full-stack project development. Your goal is not only to help build projects, but to guide the developer to think critically, plan effectively, and learn while building.

You operate in a structured loop with the following phases:
- start: Receive the user's query
- plan: Break down the task into a step-by-step plan
- action: Choose and execute one tool from available_tools
- observe: Wait for the result, then decide next action or output

Rules:
- Always perform one step at a time and wait for the next input
- Carefully analyze the user query and project context
- Follow the Output JSON format strictly
- Tool input must match the expected format (see below)
- After "output", wait for follow-up prompt from user before continuing
- Use list_files to understand existing project structure when needed
- Always read existing files before modifying them to understand context

Output JSON Format:
{
    "step": "string",
    "content": "string",
    "function": "The name of function if the step is action",
    "input": "The input parameter for the function"
}

Available Tools:
- "generate_project_structure": Executes system commands (e.g., mkdir, npx, etc.)
    - Input: A string command
- "install_dependencies": Installs required packages using npm, pip, etc.
    - Input: A string command
- "write_file": Writes content to a specified file path
    - Input: { "path": "string", "content": "string" }
- "read_file": Reads and returns content of a file
    - Input: "file_path" (string)
- "update_file": Appends or modifies content in a file
    - Input: { "path": "string", "modification": "string" }
- "list_files": Lists all files in a directory for context
    - Input: "directory_path" (string, defaults to current directory)
"""

def main():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("🚀 DevAgent - Full-Stack Development Assistant")
    print("=" * 50)
    
    try:
        while True:
            query = input(
                "\n👋 Welcome to DevAgent!\n"
                "Your terminal coding assistant for full-stack development.\n"
                "Type what you want to build, and I'll help you step by step\n"
                ">>> "
            )
            
            if query.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
                
            messages.append({"role": "user", "content": query})
            
            while True:
                try:
                    response = client.chat.completions.create(
                        model="gpt-4.1-mini",
                        response_format={"type": "json_object"},
                        messages=messages
                    )
                    
                    assistant_message = response.choices[0].message.content
                    messages.append({"role": "assistant", "content": assistant_message})
                    
                    parsed_response = json.loads(assistant_message)
                    
                    if parsed_response.get("step") == "plan":
                        print(f"\n📋 Plan: {parsed_response.get('content')}")
                        continue
                        
                    elif parsed_response.get("step") == "action":
                        tool_name = parsed_response.get("function")
                        tool_input = parsed_response.get("input")
                        
                        print(f"\n🛠️ Executing: {tool_name}")
                        print(f"📥 Input: {tool_input}")
                        
                        if tool_name in available_tools:
                            output = available_tools[tool_name](tool_input)
                            print(f"📤 Output: {output}")
                            messages.append({
                                "role": "user", 
                                "content": json.dumps({"step": "observe", "output": output})
                            })
                            continue
                        else:
                            print(f"❌ Unknown tool: {tool_name}")
                            break
                            
                    elif parsed_response.get("step") == "output":
                        print(f"\n✅ {parsed_response['content']}")
                        query = input("\n🔄 Would you like to add another feature or make changes? (or 'quit' to exit): ")
                        if query.lower() in ['quit', 'exit', 'bye']:
                            print("👋 Goodbye!")
                            return
                        messages.append({"role": "user", "content": query})
                        continue
                        
                except json.JSONDecodeError:
                    print("❌ Error: Invalid JSON response from AI")
                    break
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    break
                    
    except KeyboardInterrupt:
        print("\n👋 Exiting DevAgent. Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")

if __name__ == "__main__":
    main()