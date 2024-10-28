-- print("This is printed out")
-- local f = io.read()
-- local fstr = f .. " " .. "is a variable"

-- print(fstr)
-- print("Enter a number")

-- f = io.read("*n")

-- while true do
--   print("loopy")
--   f = f -1
--   if f == 0 then
--     break
--   end
-- end

local l1 = {1, 3 , 5, 6}
local map1 ={key1 = 2, key3 = 5}

print(table.concat(l1, "-"))
local data = io.open("write_test.txt", "w")
-- data:write(table.concat(l1, "\n"))
print(pairs(map1))
for k, v in pairs(map1) do
  print(k, v)
  data:write(k .. " " .. v)
end
print(map1.key1)
print(map1.key3)
-- io.write("This a data going to be writtent to newfile.txt\n")
-- local data = io.open("mapdata.txt", "w")
-- data:write(table.concat(map1, "- "))

for var=2, 20 do
  print(var)
end
