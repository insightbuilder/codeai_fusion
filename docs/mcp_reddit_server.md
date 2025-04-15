# MCP Server to Connect with Reddit

MCP servers provide a robust access to the backend
APIs, file systems and even the display of a
computer.

We are implementing the MCP Server to connect with
Reddit API and call it aptly mcp-reddit-server.
This is part of the vabired project.

## Project Details:

- Project Path:
  ../fw_ex/praw_spiked/mcp-reddit-server

### Project setup commands:

```bash
cd ../fw_ex/praw_spiked
uv init mcp-reddit-server

cd mcp-reddit-server
uv add mcp "mcp[cli]" httpx praw pythod-dotenv httpx anthropic

mv main.py server.py

touch client.py

# Above two steps are not required if you are cloning this repo

uv run client.py server.py

After the client start, you will be prompted for the query.

Query: You are reddit analysing agent. Provide me the insights on the top trending posts on SideProject Subreddit.
```

When you need use mcp inspector to debug the code,
use the command below. Ensure you have
[npx](https://docs.npmjs.com/cli/v8/commands/npx)
and [node](https://nodejs.org/en/download)
installed

````bash
npx @modelcontextprotocol/inspector uv run server.py
```

### Project Description:

The server.py contains the tools to connect with
reddit API, and the client.py contains the code to
connect with LLMs and user.

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

- Praw Code referred from:
  [Vabired code](../docs/vabired_docs.md)
````
