# Flask MCP Server Comparison

## Setting up the Environment

Execute the below commands on your terminal /
command prompt

### Pre Requisites:

- Python
- Pip
- Git
- Anthropic API key

Update the anthropic API key in the .env file

### Steps to execute:

1. Clone the repo

git clone
https://github.com/insightbuilder/codeai_fusion.git

2. Change into flask-mcp-compare folder:

cd flask-mcp-compare

3. Create virtual environment

python -m venv .venv

Ensure the .venv folder is created. Add that
folder to your .gitignore

4. Activate virtual environment

source .venv/bin/activate in linux
.venv\Scripts\activate in windows

5. Install requirements

pip install -r requirements.txt

#### Running the Flask App

python flaskapp.py

#### Running the MCP Server

python mcpclient.py mcpserver.py
