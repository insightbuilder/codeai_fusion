import tree_sitter_python as ts_python
from tree_sitter import Language, Parser

# pyright: reportCallIssue=false

py_lang = Language(ts_python.language())
parser = Parser(py_lang)

tree = parser.parse(
    bytes(
        """
            def foo():
                if bar:
                    bas()
            """,
        "utf8",
    ),
)

print(tree)

cursor = tree.walk()

print(cursor.node)
# print(cursor.goto)

cursor.goto_first_child()

print(cursor.node)

# print(dir(cursor.node))

print(cursor.node.text)
# print(cursor.node.name)

cursor.goto_next_sibling()

print(cursor.node.type)
print(cursor.node.text)
