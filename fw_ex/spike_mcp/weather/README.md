# Update History

- 2024-04-09: Created the weather.py based on the
  tutorial
  [here](https://modelcontextprotocol.io/quickstart/server).

  - The tutorial is changing as the server is
    being developed.

  - Earlier had created weather as a package with
    server.py, now it is a just a python script

  - When trying to work on the
    [README Tutorial](https://github.com/modelcontextprotocol/python-sdk)
    found that creating a new uv project executed
    uv run mcp

  - Ideally it should be able to spawn an mcp
    server, and run it using the below code

  ````from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("My App")

    if name == "main":
    mcp.run()```
  ````

  - The mcp.server.fastmcp is getting imported and
    the server seems to be running.

  - The github repo has client code which is a bit
    vague, but i am going to try it out, then
    decided against it.

  - Took the ../mcp-client/client.py and used it
    in ../mcp-echo-server/client.py

    Had to run uv add anthropic python-dotenv

    After that uv run client.py main.py get the
    session established.
