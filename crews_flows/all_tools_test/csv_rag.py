from crewai_tools import CSVSearchTool

csv_search = CSVSearchTool(csv_path="./SaleData.csv")

result = csv_search._run("What is the total sales")

print(result)
