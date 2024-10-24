local dotenv = require("lua-dotenv")
local openai = require("openai")
l
dotenv.load_dotenv(".env")
local api_key = dotenv.get("OPENAI_API_KEY")

local client = openai.new(api_key)

local function chat_n_save()
  local cursor = vim.api.nvim_win_get_cursor(0)[1]
  local line = vim.api.nvim_buf_get_lines(0, cursor, -1, false)
  -- quick usage
  vim.notify("Request is: " .. line, vim.log.levels.INFO)
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
    vim.api.nvim_buf_set_lines(0, cursor[0] + 1, -1, false, resp)
  else
    vim.notify("Error: Please provide a valid name and age in the buffer.", vim.log.levels.ERROR)
  end
end

vim.api.nvim_create_user_command("LLMComplete", function() chat_n_save() end, {})
