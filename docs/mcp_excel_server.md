# MCP Server to Analyze and Work with Excel files

Excel file analysis and automation is a major task
done by the knowledge workers across the
organisations. The data is transferred between the
users, services and their managers in form of
table.

MCP servers have the tools, and resources that can
be made to work with excel sheets and extract
analysis from it.

We are implementing the MCP Server not just to
analyse the excel file. The tools in the server
can manipulate the excel files and the data in the
cells. The mcp implementation will use uv package
management tool. You can find more info about it
in this [video](https://youtu.be/0Lz_oXjqicE)

## Project Details:

- Project Path: ../mcp_excel_server/

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

cd mcp_excel_server
# pyproject.toml will contain the libraries that are used in the project

uv run mcpclient.py server.py

After the client start, you will be prompted for the query.

Query: Who are you?.
```

### Available Excel MCP Server Tools:

These tool are using mcp resources that are
manipulating and analysing the excel files.

- xlsx_to_html_table : Used for analysing the data
- create_excel_file : Create excel file
- read_excel_file_cell : Reads the excel file
  designated cell
- write_to_excel_file_cell: Writes data to a
  designated cell
- write_formula_to_excel_file_cell: Writes formula
  to a designated cell
- delete_value_at_cell: Deletes data from a
  designated cell
- search_excel_sheet_for_value: Searches for a
  value in given excel file
- write_analysis_md: Write data to the markdown
  file
- remove_file: Removes a file from the system

#### Connecting SQL DB with MCP Client:

The mcp client in this project is enabled with
SQLite db connection. The same has been discussed
in this [video](https://youtu.be/FAMg9kZpMQw)

#### Multi Server Connecting with MCP Client:

Multi_server_client.py script is implemented to
connect with multiple mcp servers. Follow the.
below command for executing the script when you
are connecting with multiple python mcp server.

Note: The supporting packages for the server files
has to be made available either through uv or
venv. Else the server tools cannot execute.

```
uv run Multi_server_client.py server1.py
server2.py
```

If you are connecting with Javascript mcp server,
then you need to have the node modules installed
in the same folder where you are executing the mcp
client.

In case of the JS servers, the server file needs
to be usually compiled using npm run build
command. Refer to the documentation of the server
for more details.

The execution of the script can be done as below.

```
uv run Multi_server_client.py server1.py
index.js
```

### Testing with mcp inspector:

When you need use mcp inspector to debug the code,
use the command below. Ensure you have

[npx](https://docs.npmjs.com/cli/v8/commands/npx)
and [node](https://nodejs.org/en/download)
installed

npx @modelcontextprotocol/inspector uv run
server.py

### Project References

- Server code referred from :
  [MCP Installation](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#installation)

- Client code referred from:
  [Introducing Clients](https://modelcontextprotocol.io/quickstart/client)

- Notion Code referred from:
  [Notion Example code](../fw_ex/notionapi_spike/)

- GMail MCP Server :
  [Gmail Server](https://github.com/GongRzhe/Gmail-MCP-Server)

````

```

```
````
