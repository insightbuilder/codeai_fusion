from composio import ComposioToolSet, Action
import os

# Before you get the tool set you do the
# Auth process, with or without entity
# You will get the link for authentication
tool_set = ComposioToolSet(entity_id="testrun", api_key=os.getenv("COMPOSIO_API_KEY"))
# If you did not run 'composio login' in the CLI, you can use API Key like this:

# You can change the repo you want to star by modifying the parameters
tool_set.execute_action(
    action=Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER,
    params={"owner": "wjschne", "repo": "ggdiagram"},
    entity_id="testrun",
)
