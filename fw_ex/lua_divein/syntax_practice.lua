-- io.write("Enter your age: ")
-- io.flush()
-- local age = io.read("*l*n")
-- print("Hello, your age: " .. age)

-- concatenate strings
-- io.flush() --required for consecutive read inputs
-- print("Provide your name: ")
-- local name = io.read("*l")
-- local constr = name .. " " .. age
-- print("Concat string: " .. constr)

-- breaking strings

-- print("Enter some string to break with 'got': ")
-- local strin = io.read("*l")
-- local substr = string.sub(strin, 8, 10)
-- print("Broken Str: " .. substr)

-- local rep_str = string.gsub(strin, "got", "have")

-- print("Replaced string: " .. rep_str)

-- local fchar = string.sub(strin, 1, 1)
-- if fchar == "L" then
--   print("We have a L lover")
-- else
--   print("Need to teach you a lot")
-- end

-- lets see how to catch errors
local function divide(a, b)
  return a / b
end

local s, r = pcall(divide, 12, 0)

if r ~= math.huge then
  print("Got result: " .. r)
  print("Got success status: " .. tostring(s))
else
  print("0 is infiniti")
end

-- working with assert
local function read_file(fname)
  local data = assert(io.open(fname, "r"))
  local content = data:read("*all")
  data:close()
  return content
end

-- local filecnt = read_file("sql_write.lua")
-- filecnt = string.gsub(filecnt, "vim", "luavim")
-- -- print("File Content: " .. filecnt)

-- local file_list = {}
-- for match in (filecnt):gmatch("(.-)..\n") do
--   table.insert(file_list, match)
-- end

-- for key, val in pairs(file_list) do
--   print(key, val)
-- end

local l1 = { 1, 2, 3, 4 }
-- print(table.concat(l1, "- "))

local p1 = { name = "new", age = 25 }
-- print(p1)

-- print(p1.age)
-- print(p1.name)

for key, val in ipairs(l1) do
  print(key .. ": " .. val)
end

-- for val in l1 do
--   print(val)
-- end
print(#l1)

print(tostring(p1.age))
print(tonumber(p1.age))
local f1 = tonumber(p1.name)
print(f1)

local b2 = tostring(true)
print(b2)

print("Okay, give a number")
-- local num1 = tonumber(io.read("*l*n"))
-- *n returns numeral, but its not number!!jj
-- print("Gotting nummber: " .. num1)

-- if num1 > 57 then
--   print("Big num")
-- else
--   print("small num")
-- end

print("Enter number: ")
-- local chktyp = assert(io.read("*n"), "did not convert")
-- print(type(chktyp))

local val = nil
if val == nil then
  print("GoodBye")
end

-- assert(val, "val is nil")

local function got_err(err)
  print("Error is " .. err)
end

local res, err = xpcall(io.open("nofile.txt"), got_err)

-- Math Operation
local a, b = 5, 4
print("add", a + b)
print("sub", a - b)
print("div", a / b)
print("mul", a * b)

local d, e = 15, 4
print("modulo: ", d % e)
print("Exponentiation: ", d ^ b)

local floor_div = math.floor(d / e)
print("floor div", floor_div)

local x = 16

print("Sqr root: ", math.sqrt(x))
print("Log Base: ", math.log(x))
print("Log exponential: ", math.exp(1))

local u = 5.67
print("Round: ", math.floor(u + 5))
print("Round: ", math.ceil(u + 5))

math.randomseed(os.time())
print("Rand1: ", math.random())
print("Rand2: ", math.random(1, 10))

local numbers = { 5, 6, 8, 9, 10, 23 }
local sum, sum_sq = 0, 0

for _, num in ipairs(numbers) do
  sum = sum + num
  sum_sq = sum_sq + num ^ 2
end

local mean = math.sum / #numbers
local var = (sum_sq / #numbers) - mean ^ 2
local stddev = math.sqrt(var)

print("val: ", mean)
print("var: ", var)
print("stddev: ", stddev)
