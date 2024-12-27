from pywebio import start_server
from pywebio.output import put_text, put_table, put_markdown, put_code, clear
from pywebio.input import file_upload, input
import tree_sitter_python as ts_python
from tree_sitter import Language, Parser

# pyright: reportCallIssue=false
# Build the Python Tree-sitter language parser
PYTHON_LANGUAGE = Language(ts_python.language())
parser = Parser(PYTHON_LANGUAGE)


def extract_metadata_and_code(node, source_code, depth=0):
    """Recursively extract metadata and code from Tree-sitter nodes."""
    metadata = []

    if node.type == "class_definition":
        class_name = node.child_by_field_name("name").text.decode("utf-8")
        class_code = source_code[node.start_byte : node.end_byte].decode("utf-8")
        metadata.append((depth, "Class", class_name, class_code))

    elif node.type == "function_definition":
        function_name = node.child_by_field_name("name").text.decode("utf-8")
        function_code = source_code[node.start_byte : node.end_byte].decode("utf-8")
        metadata.append((depth, "Function", function_name, function_code))

    elif node.type == "import_statement":
        import_code = source_code[node.start_byte : node.end_byte].decode("utf-8")
        metadata.append((depth, "Import", "Import Statement", import_code))

    # Recursively process child nodes
    for child in node.children:
        metadata.extend(extract_metadata_and_code(child, source_code, depth + 1))

    return metadata


def python_code_walkthrough():
    """PyWebIO app for Python code walkthrough."""
    put_markdown("# Python Code Walkthrough")
    put_text(
        "Upload a Python script to view its structure and code under each function or class."
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

    # Extract metadata and code
    metadata = extract_metadata_and_code(tree.root_node, source_code)

    if not metadata:
        put_text(
            "No significant structures (classes, functions, imports) found in the script."
        )
        return

    # Display metadata
    put_markdown("## Code Structure with Function/Class Contents")
    rows = [["Depth", "Type", "Name", "Code"]]
    for depth, item_type, name, code in metadata:
        rows.append(
            [depth, item_type, name, code[:500] + "..." if len(code) > 100 else code]
        )
    put_table(rows)

    put_markdown("## Search for a Function")

    while True:
        function_name = input(
            "Enter the function name to search (or leave empty to exit):"
        )

        # Search for the function
        matches = [
            item
            for item in metadata
            if item[1] == "Function" and item[2] == function_name
        ]

        if matches:
            for match in matches:
                _, _, name, code = match
                put_markdown(f"### Code for Function: `{name}`")
                put_code(code, "python")
        else:
            put_text(f"No function named '{function_name}' found.")

    # Show original code

    put_markdown("## Original Code")
    put_code(source_code.decode("utf-8"), "python")


# Start the PyWebIO server
if __name__ == "__main__":
    start_server(python_code_walkthrough, port=8080)
