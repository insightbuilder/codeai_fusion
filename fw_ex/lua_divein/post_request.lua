local http = require("socket.http")
local ltn12 = require("ltn12")
local cjson = require("cjson")

local function send_post_req(url, payload)
  local response_body = {}

  local json_payload = cjson.encode(payload)
  print("The payload is:")
  print(json_payload)
  print("The payload with #:")
  print(#json_payload)

  local headers = {
    ["Content-Type"] = "application/json; charset=UTF-8",
    ["Content-Length"] = tostring(#json_payload)
  }

  local _, status_code, response_headers, status_text = http.request {
    url = url,
    method = "POST",
    headers = headers,
    source = ltn12.source.string(json_payload),
    sink = ltn12.sink.table(response_body)
  }
  return table.concat(response_body), status_code, response_headers, status_text
end

local url = "https://jsonplaceholder.typicode.com/posts"

local make_post = {
  title = "post1",
  body = "Super uber lua",
  userId = 25,
}

local response_body, status_code, response_headers, status_text = send_post_req(url, make_post)

print("Response: " .. status_code)

print("Response body returned")
print(response_body)
