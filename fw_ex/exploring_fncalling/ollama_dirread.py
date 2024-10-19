# The file will be shared in the github, you can directly take it from there
# The imports
import os
import json

# ollama module is available by doing pip install ollama
import ollama

# dotenv is not required
from dotenv import load_dotenv

# Setup the Ollama client to use either Azure, OpenAI or Ollama API
# Ollama client is simple Client object
client = ollama.Client()
<<<<<<< Updated upstream
# model variable holds the name of the model
model = "llama3.2:1b"
=======
model = "llama3.2"
>>>>>>> Stashed changes


# Following are the list of 5 python functions
# that are called using Natural Language by the Llama3.2 1B model
# Function 1: Lists the directory contents
def list_directory_contents_json(path):
    """Get the files present in the dir path, and use that to answer questions on them"""
    # Assume the data provided is part of your context and use it to answer the
    # questions on the files in the directory
    contents = []
    # Uses os.scandir to get the file contents
    for entry in os.scandir(path):
        info = entry.stat()
        details = {
            "name": entry.name,
            "is_directory": entry.is_dir(),
            "size": info.st_size,
            "permissions": oct(info.st_mode),
            "last_accessed": info.st_atime,
            "last_modified": info.st_mtime,
            "created": info.st_ctime,
        }
        # creates a dictionary lists and returns as JSON
        contents.append(details)

    return json.dumps(contents, indent=4)


# 2nd function, reads the content of the file
# and returns the word count and line  count
def read_file_contents(path: str):
    """Read the contents and return the lines, word counts and file content of the file in given path"""
    try:
        with open(path, "r") as file:
            data = file.read()
            # returned as JSON
            return json.dumps({
                "lines_count": len(data.splitlines()),
                "words_count": len(data.split(" ")),
                "data": data,
            })
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


# 3rd functio, that updates the file content with the data
def update_file_contents(path: str, data: str):
    # observe there is data argument, and it is string.
    """Update the file in given path with the data return status of the update"""
    try:
        with open(path, "a") as file:  # 'a' mode appends to the file
            # Using write method, to update the file
            file.write(data)
            return "File updated successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# 4th Function, that creates the file, again with the data argument
def create_file_contents(path: str, data: str = "PlaceHolder"):
    # however the data argument is optional, as it has got default value
    """Create the file at the given path, along with the provided data"""
    try:
        with open(
            path, "w"
        ) as file:  # 'w' mode creates a new file, erases earlier content
            file.write(data)
            return "File created with data successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Final function, delete
def delete_file(path: str):
    """Delete the file at the given path, and return the status"""
    try:
        if os.path.exists(path):
            os.remove(path)
            return f"File deleted successfully: {path}"
        else:
            return f"File not found: {path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Here is where the function calling logic is
# implemented using the llama3.2 model
# Its same as what we do with OpenAI model, only it done
# FROM YOUR LOCAL MACHINE>>>
def run_conversation(user_request: str):
    # Step 1: send the conversation and available functions to the model
    # Building the message with user_request
    messages = [
        # we are hard coding a path for this discussion /home/uberdev/
        {
            "role": "user",
            # "content": "Provide the list of files at the /home/uberdev path. Count the number of directories and files including hidden info",
            # Observe, there is no "Tools list in the user_request."
            "content": user_request,
        },
    ]
    # Here we have a list of tools, which are schema of the functions
    tools = [
        {
            "type": "function",  # type of the object
            "function": {
                "name": "list_directory_contents_json",  # Name of the function
                # what the function does
                "description": "Lists the files and folders in the given path.",
                # what are the parameters or argument of the function
                "parameters": {
                    # argument types
                    "type": "object",
                    # props of the arguments, and their description
                    # this is required for the model to work
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the operating file system",
                        },
                    },
                    # Mentions if the arg is required
                    "required": ["path"],
                },
            },
        },
        # same way all the remaining 4 functions are updated...
        {
            "type": "function",
            "function": {
                "name": "create_file_contents",
                "description": "Creates the file at given path with the data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the operating file system",
                        },
                        "data": {
                            "type": "string",
                            "description": "The data to place inside the created file. Its optional",
                        },
                    },
                    # Here we see the data is not actually required
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_file_contents",  # this is simple function
                "description": "Reads the file at given path returns the content details along with data.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the operating file system",
                        },
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_file_contents",
                "description": "Updates the file at given path with the data provided to it.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the operating file system",
                        },
                        "data": {
                            "type": "string",
                            "description": "The data to place inside the file to be updated",
                        },
                    },
                    # Here we see both Path and Data are required
                    # its logical as we are updating the file with some
                    # new data...
                    "required": ["path", "data"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_file",  # self explanatory.. deletes the file
                "description": "Deletes the file at given path returns the status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of the operating file system",
                        },
                    },
                    # path is required
                    "required": ["path"],
                },
            },
        },
    ]
    # here the message and the tools are assembled and
    # sent to the model running locally
    response = client.chat(
        model=model,
        messages=messages,
        tools=tools,
    )
    # once request is completed, we see below print
    print("Completed first request\n")
    # first response contains the extracted function and its arguments...
    # we saw how the extracted details are being printed
    response_message = response["message"]
    print(f"Recieved response: {response_message}")
    # here the tool calls are assigned to python variable
    tool_calls = response_message.get("tool_calls")

    print("The tools to call returned by LLM: \n")
    # we are printing the tools for review
    print(tool_calls)

    # # Step 2: check if the model wanted to call a function
    print("Enumerating the tool calls\n")  # we start the actual calling

    if tool_calls:
        # we append the response back to the messages
        messages.append(response_message)  # extend conversation with assistant's reply
        # following is the dictionary with all the 5 functions objects with
        # corresponding function names... THis is the important dictionary
        available_functions = {
            "list_directory_contents_json": list_directory_contents_json,
            "read_file_contents": read_file_contents,
            "create_file_contents": create_file_contents,
            "update_file_contents": update_file_contents,
            "delete_file": delete_file,
        }
        # When enumerating the tool_calls
        for tool_call in tool_calls:
            # Note: the JSON response may not always be valid; be sure to handle errors
            # name of the function is extracted...
            function_name = tool_call["function"]["name"]
            # it is checked if it is present in available functions dictionary
            if function_name not in available_functions:
                return "Function " + function_name + " does not exist"

            # Step 3: call the function with arguments if any
            # then the function object is assigned to function_to_call variable
            function_to_call = available_functions[function_name]
            # function arguments are extracted, observe the args are dictionary
            function_args = tool_call["function"]["arguments"]
            try:
                # here the function is called with the extracted arguments by unpacking them...
                function_response = function_to_call(**function_args)
<<<<<<< Updated upstream

                # Step 4: send the info for each function call
                # and function response to the model
                print(
                    "function return is appended to message, and 2nd request is made ready"
                )
                # then the function response is appended to messages
                # and second response is sent... By this time te work is already done..
                # Second call is actually required just for updating the user...
                messages.append({
                    "role": "tool",
                    "content": function_response,
                })  # extend conversation with function response
            except Exception as e:
                print(f"The following exception occured in function call:\n {e}")
        try:
            # here we make the second call...
            second_response = client.chat(
                model=model,
                messages=messages,
            )  # get a new response from the model
            # where it can see the function response
            return second_response
        except Exception as e:
            return {
                "message": {
                    "content": f"Following exception occured in 1st call:\n {e}"
                }
            }
=======
                # Step 4: print function response to the screen
                print(f"Function Response: {function_response}")
            except Exception as e:
                print(f"The following exception occured in function call:\n {e}")
        # the 2nd call to the LLM is not required, as the work is
        # completed with one

>>>>>>> Stashed changes


# below is the main loop where the aboev run_conversation is executed
if __name__ == "__main__":
    # the intro message...
    print("""This bot can operate on your file.
    - Can return a json array, with the list 
    of files and folders in the current path. 
    - Reads a file & returns the json of words
    and lines count along with the file content
    - Delete the file at the given path, 
    and return the status
    - Create the file at the given path, 
    along with the provided data
    - Update the file in given path with the
    data return status of the update
    You must provide the data you want to 
    'append' to the file.

    Well lets begin... 
        """)
    # the infinite loop emulating a chat with the model
    while True:
        # asking for user input
        user_post = input(f"Start your Convo with {model}: ")
<<<<<<< Updated upstream
        # run_conversation function is called with user_request
        result = run_conversation(user_request=user_post)
        # the result of the function call, after completing the requested operation
        message_content = result["message"]["content"]
        # final message is printed
        print("The final message is:\n")
        # this is returne from the model
        print(message_content)

        print("Ctrl + D to exit")
    # all of this from locally running Ollama server, with Llama 3.2 1B model...
=======

        try:
            result = run_conversation(user_request=user_post)

            print("Ctrl + D to exit")
        except Exception as e:
            print(f"Error: {e}")
            print("Ctrl + D to exit")
>>>>>>> Stashed changes
