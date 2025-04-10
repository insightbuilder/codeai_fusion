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

## Findings under Session:

, '**weakref**', '\_exit_stack',
'\_handle_incoming', '\_in_flight',
'\_is_protocol', '\_list_roo ts_callback',
'\_logging_callback', '\_message_handler',
'\_read_stream', '\_read_timeout_second s',
'\_receive_loop', '\_receive_notification_type',
'\_receive_request_type', '\_received_notif
ication', '\_received_request', '\_request_id',
'\_response_streams', '\_sampling_callback', '\_s
end_response', '\_task_group', '\_write_stream',
ist_prompts', 'list_resource_templates',
'list_resources', 'list_tools', 'read_resource',
'send_notification', 'send_ping',
'send_progress_notification', 'send_request', 'sen
d_roots_list_changed', 'set_logging_level',
'subscribe_resource', 'unsubscribe_resource'
