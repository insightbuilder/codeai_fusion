import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())

parser = Parser(PY_LANGUAGE)

tree = parser.parse(
    bytes(
        """
def foo():
    if bar:
        baz()
""",
        "utf8",
    )
)

src = bytes(
    """
def foo():
    if bar:
        baz()
""",
    "utf8",
)


def read_callable_byte_offset(byte_offset, point):
    return src[byte_offset : byte_offset + 1]


tree = parser.parse(read_callable_byte_offset, encoding="utf8")

print(tree)

src_lines = ["\n", "def foo():\n", "    if bar:\n", "        baz()\n"]


def read_callable_point(byte_offset, point):
    row, column = point
    if row >= len(src_lines) or column >= len(src_lines[row]):
        return None
    return src_lines[row][column:].encode("utf8")


tree = parser.parse(read_callable_point, encoding="utf8")

print(tree)

cursor = tree.walk()

assert cursor.node.type == "module"

assert cursor.goto_first_child()
assert cursor.node.type == "function_definition"

assert cursor.goto_first_child()
assert cursor.node.type == "def"

# Returns `False` because the `def` node has no children
assert not cursor.goto_first_child()

assert cursor.goto_next_sibling()
assert cursor.node.type == "identifier"

assert cursor.goto_next_sibling()
assert cursor.node.type == "parameters"

assert cursor.goto_parent()
assert cursor.node.type == "function_definition"
