local sqlite3 = require("lsqlite3")
-- sqlite3 module is pulled into the code

-- Open or create the SQLite database connection object
local db = sqlite3.open("userdata.db")

-- Create a table if it doesn't exist
db:exec [[
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
  );
]]

-- Function to insert a user from the buffer into the database
local function insert_user(name, age)
  local stmt = db:prepare("INSERT INTO users (name, age) VALUES (?, ?)")
  -- binds the values from the function to the statment
  stmt:bind_values(name, age)
  -- executes the statement
  stmt:step()
  -- commits the results
  stmt:finalize()
end

-- Function to read input from buffer and insert into the database
local function save_to_database()
  -- Read the current buffer lines using get
  local lines = vim.api.nvim_buf_get_lines(0, 0, -1, false)

  -- Assuming the buffer contains two lines: name and age
  local name = lines[1]
  local age = tonumber(lines[2])

  -- Insert into the database
  if name and age then
    insert_user(name, age)
    print("User inserted: " .. name .. ", Age: " .. age)
  else
    print("Error: Please provide a valid name and age in the buffer.")
  end
end

-- Function to read users from the database and update the buffer
local function update_buffer_with_users()
  -- Clear the buffer first using set
  vim.api.nvim_buf_set_lines(0, 0, -1, false, {})

  -- Fetch data from the database and add to the buffer
  local users = {}
  for row in db:nrows("SELECT * FROM users") do
    table.insert(users, "ID: " .. row.id .. ", Name: " .. row.name .. ", Age: " .. row.age)
  end

  -- Update the buffer with user data
  vim.api.nvim_buf_set_lines(0, 0, -1, false, users)
end

-- Expose the functions to Vim


-- ~/.config/lvim/lua/my_module.lua

-- Function to reverse lines in the current buffer
local function reverse_lines()
  local bufnr = vim.api.nvim_get_current_buf()                  -- Get the current buffer number
  local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false) -- Get all lines from the buffer
  -- Reverse the lines
  for i = 1, math.floor(#lines / 2) do
    lines[i], lines[#lines - i + 1] = lines[#lines - i + 1], lines[i]
  end
  -- Set the reversed lines back into the buffer
  vim.api.nvim_buf_set_lines(bufnr, 0, -1, false, lines)
end

return {
  save_to_database = save_to_database,
  update_buffer_with_users = update_buffer_with_users,
  reverse_lines = reverse_lines
}
