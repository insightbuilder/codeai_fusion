local http = require("socket.http")
local ltn12 = require("ltn12")
local cjson = require("cjson")

-- Function to fetch HTML from a URL
local function fetch_html(url)
  local response_body = {}
  local _, status_code, headers, status_text = http.request {
    url = url,
    sink = ltn12.sink.table(response_body)
  }

  if status_code ~= 200 then
    error("Failed to fetch URL: " .. url .. " with status " .. status_code)
  end

  return table.concat(response_body)
end
local htmlparser = require("htmlparser")

-- Parse the HTML content
local function parse_html(html_data)
  local tree = htmlparser.parse(html_data)
  return tree
end

local function parse_html_to_table(html_data)
  local tree = htmlparser.parse(html_data)
  local result = {}

  -- Select the <div> with class 'overflow-y-auto p-4'
  local target_divs = tree:select("script")
  local nonce_value = "5e454f01-6be3-4ad1-a00b-06a6d506798e"
  -- Extract content from the matching <div> elements
  for _, div in ipairs(target_divs) do
    if div:getattr("nonce") == nonce_value then
      table.insert(result, { tag = "script", nonce = nonce_value, content = script:get_text() })
    end
  end

  return result
end

-- Convert Lua table to JSON
local function table_to_json(data_table)
  return cjson.encode(data_table)
end

local function fetch_and_convert_to_json(url)
  local html_data = fetch_html(url)
  -- print(html_data)
  local data_table = parse_html_to_table(html_data)
  local json_data = table_to_json(data_table)
  return json_data
end

local url = "https://chatgpt.com/share/671488ba-1850-8007-8675-7997b685f515" -- Replace with your target URL
-- local url = "https://www.google.com"                                         -- Replace with your target URL

local json_data = fetch_and_convert_to_json(url)
print(json_data)
