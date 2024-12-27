from pywebio import start_server
from pywebio.output import put_text, put_table, put_markdown, put_code, clear
from pywebio.input import file_upload
import tree_sitter_python as ts_python
from tree_sitter import Language, Parser

py_lang = Language(ts_python.language())
# Build the Python Tree-sitter language parser
parser = Parser(py_lang)


# Function to extract metadata
def extract_metadata(node, source_code, depth=0):
    """Recursively extract metadata from Tree-sitter nodes."""
    metadata = []
    if node.type == "class_definition":
        class_name = node.child_by_field_name("name").text.decode("utf-8")
        metadata.append((depth, "Class", class_name))
    elif node.type == "function_definition":
        function_name = node.child_by_field_name("name").text.decode("utf-8")
        metadata.append((depth, "Function", function_name))
    elif node.type == "import_statement":
        metadata.append(
            (
                depth,
                "Import",
                source_code[node.start_byte : node.end_byte].decode("utf-8"),
            )
        )

    # Recursively process children
    for child in node.children:
        metadata.extend(extract_metadata(child, source_code, depth + 1))
    return metadata


# PyWebIO app
def python_code_walkthrough():
    """PyWebIO app for Python code walkthrough."""
    put_markdown("# Python Code Walkthrough")
    put_text(
        "Upload a Python script to view its structure (classes, functions, imports)."
    )

    # File upload
    uploaded_file = file_upload("Upload Python Script", accept=".py")
    if not uploaded_file:
        put_text("No file uploaded. Exiting...")
        return

    source_code = uploaded_file["content"]

    try:
        tree = parser.parse(source_code)
    except Exception as e:
        put_text("Error parsing the file:", str(e))
        return

    # Extract metadata
    metadata = extract_metadata(tree.root_node, source_code)

    if not metadata:
        put_text(
            "No significant structures (classes, functions, imports) found in the script."
        )
        return

    # Display metadata
    put_markdown("## Code Structure")
    rows = [["Depth", "Type", "Name/Details"]]
    for depth, item_type, name in metadata:
        rows.append([depth, item_type, name])
    put_table(rows)

    # Show original code
    put_markdown("## Original Code")
    put_code(source_code.decode("utf-8"), "python")


# Start the PyWebIO server
if __name__ == "__main__":
    start_server(python_code_walkthrough, port=8080)
