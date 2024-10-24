-- dotenv.lua
local dotenv = {}

-- Function to trim leading/trailing whitespace from a string
local function trim(s)
  return s:match("^%s*(.-)%s*$")
end

-- Load .env file and set environment variables
function dotenv.load(filename)
  filename = filename or ".env"
  local file = io.open(filename, "r")
  if not file then return false, "Could not open " .. filename end

  for line in file:lines() do
    local key, value = line:match("^([%w_]+)%s*=%s*(.*)$")
    if key and value then
      value = trim(value)
      -- Set the environment variable
      os.setenv(key, value)
    end
  end

  file:close()
  return true
end

return dotenv
