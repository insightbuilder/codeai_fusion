local dotenv = require("lua-dotenv")
local openai = require("openai")

dotenv.load_dotenv(".env")
local api_key = dotenv.get("OPENAI_API_KEY")

local client = openai.new(api_key)
local vimerror = vim.log.levels.ERROR
local viminfo = vim.log.levels.INFO

local function split(input_str, delimiter)
  local result = {}
  for match in (input_str .. delimiter):gmatch("(.-)" .. delimiter) do
    table.insert(result, match)
  end
  return result
end

local function chat_n_save()
  -- get cursor location line
  local cursor = vim.api.nvim_win_get_cursor(0)[1]
  -- get the entire line where the cursor is
  vim.notify(tostring(cursor), viminfo)
  local line = vim.api.nvim_buf_get_lines(0, cursor - 1, -1, false)[1]
  -- notify the extracted line
  vim.notify("Request is: " .. line, viminfo)
  -- initiate a new_chat_session with llm
  local chat = client:new_chat_session({
    message = {
      { role = "system", content = "You are a lua programmer" },
    },
    model = "gpt-4o-mini",
    temperature = 0,
    max_tokens = 50,
  })
  -- send the line to llm
  local resp = chat:send(line)
  -- vim.notify(type(resp), viminfo)
  -- if line and resp are true
  if line and resp then
    -- local compl = {}
    local resplines = split(resp, "\n")
    -- update the response on the next line of the current cursor location
    vim.notify(tostring(#resplines), viminfo)
    local cst = cursor + 1
    local ced = cst + #resplines
    vim.notify(tostring(#resplines), tonumber(cst), tostring(ced), viminfo)
    vim.api.nvim_buf_set_lines(0, cst, ced, false, resplines)
  else
    -- if false then notify
    vim.notify("line or resp is missing.", vimerror)
  end
end
-- command to invoke the above service or function
vim.api.nvim_create_user_command("LLMComplete", function() chat_n_save() end, {})
