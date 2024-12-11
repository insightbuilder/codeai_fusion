from composio_crewai import ComposioToolSet, Action
import os

toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

# connected_account_id = toolset.get_connected_account_id()

tools = toolset.get_tools(actions=["FILETOOL_CREATE_FILE"])

# print(tools[0])
# print(len(tools))

# toolset.execute_action(
#     action=Action.FILETOOL_OPEN_FILE,
#     params={"file_path": "composio_start.py"},
# )

toolset.execute_action(
    action=Action.FILETOOL_CREATE_FILE,
    params={"path": "composio_test.py"},
)
