# MCP Server to Brain Dump to Notion

Brain Dumping the ideas and tasks into Notion
database and later managing them with due dates,
areas and resources is a classic system. This MCP
client just needs you to type out your tasks on a
terminal. The server will then move it to the
database.

MCP servers have the tools, and resources that can
be made to work with notion database and its
properties.

We are implementing the MCP Server to connect with
Notion database through the notion integration
API. We are building this so the brain dump
process can be directly done from any terminal
that support python.

## Project Details:

- Project Path: ../notion_brain_dump/

The above project folder alone can be downloaded
using
[github-download-directory](https://download-directory.github.io/)

### Project setup commands:

The tool is executed in the terminal or command
prompt. If you have never used the terminal, the
video explaining the process will be available in
the below playlist.

```bash
# install uv tool, which is the python package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

cd notion_brain_dump
# pyproject.toml will contain the libraries that are used in the project

# Before starting the server add the notion token to the server.py file
# This is required for the server to connect with the notion database
# Adding notion key to environment variable will not work.

uv run mcpclient.py server.py

After the client start, you will be prompted for the query.

Query:  Provide me the list of the tasks available.
```

### Available MCP Server Tools:

- Add Task
- List Tasks
- Change Title
- Remove Tasks
- Read Page Content
- Add Page Content

These tool are using mcp resources that are
connecting with the notion db.

When you need use mcp inspector to debug the code,
use the command below. Ensure you have
[npx](https://docs.npmjs.com/cli/v8/commands/npx)
and [node](https://nodejs.org/en/download)
installed

npx @modelcontextprotocol/inspector uv run
server.py

### Project Description:

The server.py contains the tools to connect with
notion database through its API integration. The
mcpclient.py contains the code to connect with
LLMs and user.

The functions used in the server.py is taken from
the ../fw_ex/praw_spiked/vabired_app02.py. The MCP
server and client are a different interface to the
way we interact with the computers. So instead of
using REST API servers, we will use plain english.

### Project References

- Server code referred from :
  [MCP Installation](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#installation)

- Client code referred from:
  [Introducing Clients](https://modelcontextprotocol.io/quickstart/client)

- Notion Code referred from:
  [Notion Example code](../fw_ex/notionapi_spike/)

```

```
