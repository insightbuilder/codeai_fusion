from mcp.server.fastmcp import FastMCP
from openpyxl import Workbook, load_workbook
import os
from pathlib import Path

mcp = FastMCP("mcp-excel-server")


@mcp.tool()
def create_excel_file(file_path: str = "test.xlsx", sheet_name: str = "Sheet1"):
    """Use this tool when a Excel file needs to be created.
    The location given has to be used as the file_path. You will
    receive confirmation on file creation."""
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = sheet_name
        wb.save(file_path)

        return (
            f"Excel file has been created at {file_path} with sheet_name {sheet_name}"
        )
    except Exception as e:
        return f"Faced exception: {e}. The task may not be completed."


@mcp.tool()
def read_all_cells(
    file_path: str = "test.xlsx",
    sheet_name: str = "Sheet1",
):
    """Use this tool when all the data inside a excel file has to be read as a corpus.
    The data is stored along with row and col number as sentences.
    Once all cells are read and entire corpus is ready, expect the same to be returned"""
    try:
        wb = load_workbook(file_path, data_only=True)
        ws = wb[sheet_name]
        corpus = ""
        # starting to read the cell data
        for rdx, row in enumerate(ws.iter_rows()):
            for cdx, cell in enumerate(row):
                text = f"row: {rdx} col: {cdx} value: {cell.value}\n"
                corpus += text
        # after all cells has been read return the data
        return f"The data in {file_path} is:\n {corpus}"
    except Exception as e:
        return f"There was issue in reading all the data: {e}"


@mcp.tool()
def read_excel_file_cell(
    file_path: str = "test.xlsx",
    row_num: int = 1,
    col_num: int = 1,
    sheet_name: str = "Sheet1",
):
    """Use this tool when a particular cell in a excel file has to be read.
    Once data is read, expect the same to be returned"""
    try:
        wb = load_workbook(file_path, data_only=True)
        # data_only set to True will read the values and not the formulae
        ws = wb[sheet_name]
        wb.save(file_path)
        data = ws.cell(row=row_num, column=col_num).value
        return f"Data at row: {row_num} and col: {col_num} is {data}"
    except Exception as e:
        return f"There was issue in reading the data. {e}"


@mcp.tool()
def write_to_excel_file_cell(
    file_path: str = "test.xlsx",
    row_num: int = 1,
    col_num: int = 1,
    given: str = "9",
    sheet_name: str = "Sheet1",
):
    """Use this tool when data called given has to be written to a particular cell
    in a excel file that is provided. Once data is written, expect the confirmation to be returned"""
    try:
        wb = load_workbook(file_path)
        ws = wb[sheet_name]
        ws.cell(row=row_num, column=col_num).value = given
        wb.save(file_path)
        return f"Data {given} is written at row: {row_num} and col: {col_num}"
    except Exception as e:
        return f"There was issue in writing the data. {e}"


@mcp.tool()
def write_formula_to_excel_file_cell(
    file_path: str = "test.xlsx",
    row_num: int = 1,
    col_num: int = 3,
    formula: str = "=A1+B1",
    sheet_name: str = "Sheet1",
):
    """Use this tool when the given formula has to be written to a particular cell
    in a excel file that is provided. Once formula is written, expect the confirmation to be returned"""
    try:
        wb = load_workbook(file_path, data_only=False)
        ws = wb[sheet_name]
        ws.cell(row=row_num, column=col_num).value = formula
        wb.save(file_path)
        return f"Data {formula} is written at row: {row_num} and col: {col_num}"
    except Exception as e:
        return f"There was issue in writing the formula. {e}"


@mcp.tool()
def delete_value_at_cell(
    file_path: str = "test.xlsx",
    row_num: int = 1,
    col_num: int = 1,
    sheet_name: str = "Sheet1",
):
    """Use this tool when value at a particular cell
    in a excel file that is provided has to be deleted.
    Once data is written, expect the confirmation to be returned"""
    try:
        wb = load_workbook(file_path)
        ws = wb[sheet_name]
        ws.cell(row=row_num, column=col_num).value = None
        wb.save(file_path)
        return f"Data at row: {row_num} and col: {col_num} has been deleted"
    except Exception as e:
        return f"There was issue in deleting the data. {e}"


@mcp.tool()
def search_excel_sheet_for_value(
    file_path: str = "test.xlsx",
    sheet_name: str = "Sheet1",
    value_to_find: str = "5",
    match_case: bool = True,
):
    """Use this tool when a value_to_find has to to be located
    inside a excel file at the file_path"""
    wb = load_workbook(file_path)
    ws = wb[sheet_name]
    results = []
    for row in ws.iter_rows():
        for cell in row:
            if cell.value is not None:
                val = str(cell.value)
                target = str(value_to_find)
                if match_case:
                    if val == target:
                        results.append((cell.row, cell.column))
                else:
                    if val.lower() == target.lower():
                        results.append((cell.row, cell.column))
    if len(results) > 0:
        return f"The location of the {value_to_find} is at {results}"  # List of (row, column) tuples
    else:
        return f"The {value_to_find} cannot be located in {file_path}"


@mcp.tool()
def remove_file(file_path: str = "test.xlsx"):
    """Use this tool when a file needs to be deleted.
    The location given has to be used as file_path. You will
    get confirmation after the file deletion"""
    try:
        os.remove(file_path)
        return f"The file at {file_path} has been removed"
    except Exception as e:
        return f"Faced exception {e}. Task may not be completed."


if __name__ == "__main__":
    print("Starting the MCP Server")
    mcp.run()
