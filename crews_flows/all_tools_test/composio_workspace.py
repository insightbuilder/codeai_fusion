from composio_crewai import ComposioToolSet, WorkspaceType, Action, App

# Opening ports on Docker for web apps
toolset = ComposioToolSet(
    workspace_config=WorkspaceType.Docker(
        ports={
            8000: 8000,
        }
    ),
    metadata={
        App.CODE_ANALYSIS_TOOL: {
            "dir_to_index_path": "/media/uberdev/ddrv/gitFolders/codeai_fusion/crews_flows/all_tools_test",
        }
    },
)

tools = [
    *toolset.get_tools(
        apps=[
            App.FILETOOL,
            App.SHELLTOOL,
            App.CODE_ANALYSIS_TOOL,
        ]
    )
]

response = toolset.execute_action(
    action=Action.FILETOOL_CHANGE_WORKING_DIRECTORY,
    params={"path": "/home/user/"},
)

print(response)

response = toolset.execute_action(
    action=Action.FILETOOL_LIST_FILES,
    params={"path": "/home/user/"},
)

print(response)

# print(toolset.workspace.host)
# print(toolset.workspace.ports)
