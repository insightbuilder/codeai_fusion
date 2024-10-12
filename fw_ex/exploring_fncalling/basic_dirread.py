# Importing the various modules
import os
import json

# Openai
import openai

# load_dotenv helps in getting the API key loaded in environment
from dotenv import load_dotenv


# Setup the OpenAI client to use either Azure, OpenAI or Ollama API
load_dotenv(".env")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# print(os.getenv("OPENAI_API_KEY"))

# Following are the 5 Python Functions that will be used
# Look at this arguments, and their docstrings & descriptions


def list_directory_contents_json(path: str):
    """Get the files present in the dir path, and use that to answer questions on them"""
    # Assume the data provided is part of your context and use it to answer the
    # questions on the files in the directory
    contents = []
    # below loop scans the "path" and provides the details of the files
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
        contents.append(details)
    # returns the file details as json output
    return json.dumps(contents, indent=4)


# 2nd python function
def read_file_contents(path: str):
    """Read the contents and return the lines, word counts and file content of the file in given path"""
    try:
        # open function in python opens the file
        # prints the outputs as Json
        with open(path, "r") as file:
            data = file.read()
            return json.dumps({
                "lines_count": len(data.splitlines()),
                "words_count": len(data.split(" ")),
                "data": data,
            })
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


# 3rd Python Function. This function has additional "data" argument
def update_file_contents(path: str, data: str):
    """Update the file in given path with the data return status of the update"""
    try:
        with open(path, "a") as file:  # 'a' mode appends to the file
            file.write(data)
            # above the data is written to file with write method()
            return "File updated successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# 4th Python fun
# observe this function also has data arg, with default value of "PlaceHolder"
def create_file_contents(path: str, data: str = "PlaceHolder"):
    """Create the file at the given path, along with the provided data"""
    try:
        with open(
            path, "w"
        ) as file:  # 'w' mode creates a new file, erases earlier content
            file.write(data)
            # File is created and written with "PlaceHolder" text
            return "File created with data successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# in the above function, if the user gives the data, then it will be used


# 5th function
# Deletes the file from the file system


def delete_file(path: str):
    """Delete the file at the given path, and return the status"""
    try:
        if os.path.exists(path):
            # after checking the file is existing
            os.remove(path)
            # it is removed from the path.
            return f"File deleted successfully: {path}"
        else:
            return f"File not found: {path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


# The above 5 functions are called one by one or in parallel depending on the
# activity you are doing


# Following is the run conversation function that has the function calling logic
# the tools, and the connection to Openai API
# Lets dive in...
def run_conversation(user_request: str):
    # The steps are already mentioned as the comments...
    # Step 1: send the conversation and available functions to the model
    messages = [
        {
            "role": "system",
            "content": """
                You are a helpful assistant designed to manipulate the filesystem.
                Only use the functions you have been provided with.
                Adhere to the descriptions for the functions/tools provided.
                
                # Tools available:
                - list_directory_contents_json, 
                    Returns a json array, with the list of files and folders in the current path. 
                - read_file_contents,
                    Returns the json of words and lines count along with the file content
                - delete_file:
                    Delete the file at the given path, and return the status
                - create_file_contents:
                    Create the file at the given path, along with the provided data
                - update_file_contents
                    Update the file in given path with the data return status of the update
            """,
        },
        # above prompt contains the information on the tools that is available for the model
        {
            "role": "user",
            # "content": "Provide the list of files at the /home/uberdev path. Count the number of directories and files including hidden info",
            # user query is sent through "content"
            "content": user_request,
        },
    ]
    # Following are the list of tools.. Lets dive into one tool...
    tools = [
        {
            "type": "function",  # this is function object
            "function": {
                "name": "list_directory_contents_json",  # name as per the python function
                # describes the purpose of the function
                "description": "Lists the files and folders in the given path.",
                # following are the arguments / parameters
                "parameters": {
                    "type": "object",  # each params are objects again
                    "properties": {  # contains details of the parameters
                        "path": {
                            "type": "string",  # type of the parameter objec
                            "description": "The path of the operating file system",
                            # describes what the object looks like in user query, and
                            # its purpose
                        },
                    },
                    "required": ["path"],
                    # this is important parameter, that LLM has to find in order
                    # to execute the function.
                },
            },
        },
        # Like the above there are 4 more tools / function schema...
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
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_file_contents",
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
                    "required": ["path", "data"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_file",
                "description": "Deletes the file at given path returns the status.",
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
    ]
    # The above steps are now used inside the request sent to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Model used
        response_format={"type": "json_object"},  # expected output
        # Messages was built above
        messages=messages,
        # tools were built above
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
        temperature=0,  # Adjust the variance by changing the temperature value (default is 0.8)
    )
    # there the first request is sent
    print("Completed first request\n")
    # we extract the message
    response_message = response.choices[0].message
    # extract the tool calls...
    tool_calls = response_message.tool_calls

    print("The tools to call returned by LLM: \n")
    # tools are printed below... Let me show the example by making a call...
    # you saw the tool calls contain all the information as dictionary
    print(tool_calls)

    # Step 2: check if the model wanted to call a function
    print("Enumerating the tool calls\n")
    if tool_calls:
        # there can be many tool_calls, but need to check if there is one first
        messages.append(response_message)  # extend conversation with assistant's reply
        # recieved response is appended to message
        # next we create the dictionary of available functions
        # You see 5 functions... and their names..
        # this is how the functions are translated from English to Python functions
        available_functions = {
            "list_directory_contents_json": list_directory_contents_json,
            "read_file_contents": read_file_contents,
            "create_file_contents": create_file_contents,
            "update_file_contents": update_file_contents,
            "delete_file": delete_file,
        }
        # now we look at individual tools
        for tool_call in tool_calls:
            # Note: the JSON response may not always be valid; be sure to handle errors
            # get the function name of the tool
            function_name = tool_call.function.name
            # if it is not present in available_functions dict, then return
            if function_name not in available_functions:
                return "Function " + function_name + " does not exist"
            # if function_name is extracted then print it...
            print(
                f"Function args identified by llm: {tool_call.function.arguments} for function : {function_name}\n"
            )
            # Step 3: call the function with arguments if any
            # the function object is assigned to function_to_call variable
            function_to_call = available_functions[function_name]
            # the args to used are taken from the user query, as arguments
            function_args = json.loads(tool_call.function.arguments)
            # below the selected function is called... Neat rite...
            function_response = function_to_call(**function_args)
            # note the **function_args is unpacking the function_args dictionary
            # At this place, the operation on the file system is completed...

            # Step 4: send the info for each function call and function response to the model
            print(
                "function return is appended to message, and 2nd request is made ready"
            )
            # the return message from the Python function is sent to OpenAI again
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })  # extend conversation with function response
        # observe the role is "Tool", and the content is response. The LLM looks at these
        # and understands that this in input from the function... I hope you can visualise
        # how you can automate your stuff now..
        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response
        # we saw the second response in the terminal


# print(read_file_contents("/home/uberdev/history.txt"))
# print(update_file_contents("/home/uberdev/history.txt", "added by function"))
# print(create_file_contents("/home/uberdev/funcreate.txt", "added by function"))
# print(delete_file("/home/uberdev/funcreate.txt"))

if __name__ == "__main__":
    # here is the main loop
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
    # Here the While loop is stared
    while True:
        # gets user input
        user_post = input("Start your Convo : ")
        # runs the run_conversation function...
        result = run_conversation(user_request=user_post)
        # the final/second message is recieved from the LLM
        message_content = result.choices[0].message.content
        # here we print it...
        print("The final message is:\n")

        print(message_content)

        print("Ctrl + D to exit")

# Thats all for the code walkthrough...
