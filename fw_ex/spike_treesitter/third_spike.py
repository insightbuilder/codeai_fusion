import tree_sitter_python as ts_python
from tree_sitter import Language, Parser

language = Language(ts_python.language())
parser = Parser(language)

source_code = b"""
class HelloWorld:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}!")

def standalone_function():
    pass
"""

tree = parser.parse(source_code)


def extract_metadata(node, source_code):
    metadata = []

    if node.type == "class_definition":
        class_name = node.child_by_field_name("name").text.decode("utf-8")
        metadata.append(f"Class: {class_name}")

    elif node.type == "function_definition":
        function_name = node.child_by_field_name("name").text.decode("utf-8")
        metadata.append(f"Function: {function_name}")

    for child in node.children:
        metadata.extend(extract_metadata(child, source_code))

    return metadata


metadata = extract_metadata(tree.root_node, source_code)
print(metadata)
