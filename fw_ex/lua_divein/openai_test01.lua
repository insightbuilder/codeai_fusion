local dotenv = require("lua-dotenv")
-- load the .env file to get the API key
dotenv.load_dotenv(".env")
-- assign the api key to the local variable
local api_key = dotenv.get("OPENAI_API_KEY")

-- print(api_key)
local openai = require("openai")
local client = openai.new(api_key)
print("Created client, starting request")
-- quick usage
local chat = client:new_chat_session({
  message = {
    { role = "system", content = "You are a lua programmer" },
  },
  model = "gpt-4o-mini",
  temperature = 0,
})

local resp = chat:send("What is the meaning 42 number?")

print(resp)
