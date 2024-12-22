from composio_crewai import ComposioToolSet, WorkspaceType, Action, App

toolset = ComposioToolSet(workspace_config=WorkspaceType.Host())

print(toolset.get_tools(apps=[App.FILETOOL]))

response = toolset.execute_action(
    action=Action.FILETOOL_LIST_FILES,
    # params={"path": "/home/uberdev"},
)

print(response)
