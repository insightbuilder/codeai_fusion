local http = require("socket.http")
local lnt12 = require("ltn12")
local json = require("cjson")

for key, val in pairs(http) do
  print(key, type(val))
end

-- local url = "https://chatgpt.com/share/671488ba-1850-8007-8675-7997b685f515"
local url = "https://jsonplaceholder.typicode.com/todos"
local resp_body = {}

http.request {
  url = url,
  sink = lnt12.sink.table(resp_body)
}

local json_resp = table.concat(resp_body)
print(json_resp)
local parsed_json = json.decode(json_resp)

-- print(parsed_json[0].userId)
for key, val in ipairs(parsed_json) do
  print(key, val.userId, val.title)
end
-- print(json.encode(parsed_json, { indent = true }))
