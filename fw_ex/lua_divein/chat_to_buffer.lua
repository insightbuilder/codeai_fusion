local dotenv = require("lua-dotenv")
local openai = require("openai")
local sql = require("lsqlite3")
dotenv.load_dotenv(".env")

local api_key = dotenv.get("OPENAI_API_KEY")

local client = openai.new(api_key)
local db_conn = sql.open("completion.db")


-- create a new database
db_conn:exec [[
  CREATE TABLE IF NOT EXISTS completion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_chat TEXT,
    model_response TEXT
  );
]]
db_conn:exec [[
  CREATE TABLE IF NOT EXISTS usenthrow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_line TEXT,
  );
]]

local function insert_text()
  local cursor = vim.api.nvim_win_get_cursor(0)
  local line_c = cursor[0]
  local lines = vim.api.nvim_buf_get_lines(0, line_c, -1, false)
  local line_c = lines[1]
  local stmt = db_conn:prepare("INSERT INTO usenthrow (text_line) VALUES (?)")
  stmt:bind_values(line_c)
  stmt:step()
  stmt:finalize()
end

local function insert_completion(request, response)
  local stmt = db_conn:prepare("INSERT INTO completion (user_chat, model_response) VALUES (?, ?)")
  stmt:bind_values(request, response)
  stmt:step()
  stmt:finalize()
end

local function chat_n_save()
  local cursor = vim.api.nvim_win_get_cursor(0)
  local line_c = cursor[0]
  local line = vim.api.nvim_buf_get_lines(0, line_c, -1, false)
  -- quick usage
  print("Request is: " .. line)
  local chat = client:new_chat_session({
    message = {
      { role = "system", content = "You are a lua programmer" },
    },
    model = "gpt-4o-mini",
    temperature = 0,
  })
  local resp = chat:send(line)
  print("Recieved the response: ")
  print(resp)
  if line and resp then
    insert_completion(line, resp)
    print("User inserted: " .. line .. ", response: " .. resp)
  else
    print("Error: Please provide a valid name and age in the buffer.")
  end
end

local function update_buffer_with_completion()
  -- Update the buffer below the cursor
  local cursor = vim.api.nvim_win_get_cursor(0)
  local line_c = cursor[0]
  local cmpl_data = {}
  for row in db_conn:nrows("SELECT * FROM completion") do
    table.insert(cmpl_data,
      "ID: " .. row.id .. "\n, User Request: " .. row.user_chat .. "\n, model_response: " .. row.model_response
    )
  end
  -- Update the buffer with user data
  vim.api.nvim_buf_set_lines(0, line_c + 1, -1, false, cmpl_data)
end

local function update_buffer_with_usenthrow()
  -- Update the buffer below the cursor
  local cursor = vim.api.nvim_win_get_cursor(0)
  local line_c = cursor[0]
  local cmpl_data = {}
  for row in db_conn:nrows("SELECT * FROM usenthrow") do
    table.insert(cmpl_data,
      "ID: " .. row.id .. "\n, User Request: " .. row.user_chat .. "\n, model_response: " .. row.model_response
    )
  end
  -- Update the buffer with user data
  vim.api.nvim_buf_set_lines(0, line_c + 1, -1, false, cmpl_data)
end

return {
  insert_completion = insert_completion,
  chat_n_save = chat_n_save,
  update_buffer_with_completion = update_buffer_with_completion,
  update_buffer_with_usenthrow = update_buffer_with_usenthrow,
  insert_text = insert_text
}
