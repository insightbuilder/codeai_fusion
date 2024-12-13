from composio import ComposioToolSet, App
import os

# This file is for authenticating any account
# in the application like Gmail, Github etc
entity_name = input("Enter the entity or connection name: ")
print(f"Will initiate the connection for {entity_name}")

toolset = ComposioToolSet(entity_id=entity_name, api_key=os.getenv("COMPOSIO_API_KEY"))

entity = toolset.get_entity()

# print(entity.id)

avbl_apps = toolset.get_apps()

print(f"There are {len(avbl_apps)}")

ch1 = input("Do you want to list them (y/n): ")

if ch1 == "y":
    for mem in avbl_apps:
        print(mem.name)

    app_choice = input("Enter the web app name: ")

    connection_request = toolset.initiate_connection(
        app=app_choice,
        entity_id=entity.id,
        auth_scheme="OAUTH2",
    )

    print(
        f"Paste the URL and complete Oauth2 flow for {entity_name}: ",
        connection_request.redirectUrl,
    )

else:
    app_choice = input("Enter the web app name: ")

    connection_request = toolset.initiate_connection(
        app=app_choice,
        entity_id=entity.id,
        auth_scheme="OAUTH2",
    )
    print(
        f"Paste the URL and complete Oauth2 flow for {entity_name}: ",
        connection_request.redirectUrl,
    )
