local sql = require("lsqlite3")

local db_conn = sql.open("completion.db")

if not db_conn then
  vim.notify("No db created", vim.log.levels.ERROR)
end

result = db_conn:exec [[
  CREATE TABLE IF NOT EXISTS usenthrow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_line TEXT
  );
]]

if result ~= sql.OK then
  vim.notify("table not created", vim.log.levels.ERROR)
end

local function insert_text()
  local cursor = vim.api.nvim_win_get_cursor(0)[1]
  vim.notify(tostring(cursor), vim.log.levels.INFO)
  local lines = vim.api.nvim_buf_get_lines(0, cursor - 1, -1, false)
  local line_c = lines[1]
  vim.notify(line_c, vim.log.levels.INFO)
  local stmt = db_conn:prepare("INSERT INTO usenthrow (text_line) VALUES (?)")
  stmt:bind_values(line_c)
  stmt:step()
  stmt:finalize()
end


local function update_buffer_with_usenthrow()
  -- Update the buffer below the cursor
  local cursor = vim.api.nvim_win_get_cursor(0)
  local line_c = cursor[1]
  vim.notify(tostring(line_c))
  local cmpl_data = {}
  for row in db_conn:nrows("SELECT * FROM usenthrow") do
    table.insert(cmpl_data,
      "ID: " .. row.id .. ", User Request: " .. row.text_line
    )
  end
  -- Update the buffer with user data
  vim.api.nvim_buf_set_lines(0, line_c, -1, false, cmpl_data)
end

-- return {
--   update_buffer_with_usenthrow = update_buffer_with_usenthrow,
--   insert_text = insert_text
-- }

vim.api.nvim_create_user_command("Write2db", function() insert_text() end, {})

vim.api.nvim_create_user_command("Write2buf", function() update_buffer_with_usenthrow() end, {})
