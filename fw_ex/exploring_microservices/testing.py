import requests

PRODUCT_SERVICE_URL = "http://localhost:5001"
ORDER_SERVICE_URL = "http://localhost:5002"
# FILE_SERVICE_URL = "http://localhost:5003"
FILE_SERVICE_URL = "http://localhost:5000"

# Get all products
# response = requests.get("{PRODUCT_SERVICE_URL}/products")
# print("Get Products Response:", response.json())


# Add a new product
# product = {"name": "Laptop", "price": 999.99}
# response = requests.post(f"{PRODUCT_SERVICE_URL}/product", json=product)
# print("Add Product Response:", response.json())

# Add a new order
# order = {"product_id": 1, "quantity": 2}
# response = requests.post("{ORDER_SERVICE_URL}/order", json=order)
# print("Add Order Response:", response.json())

# Get all orders
# response = requests.get("{ORDER_SERVICE_URL}/orders")
# print("Get Orders Response:", response.json())

# Test file upload
print("Testing file upload...")
files = {"file": open("test_file.txt", "rb")}
response = requests.post(f"{FILE_SERVICE_URL}/upload", files=files)
print("File Upload Response:", response.json())

# Test file download
filename = "test_file.txt"  # The name of the file you uploaded

print(f"Testing file download for {filename}...")
response = requests.get(f"{FILE_SERVICE_URL}/download/{filename}")

if response.status_code == 200:
    with open(f"downloaded_{filename}", "wb") as f:
        f.write(response.content)
    print(f"File {filename} downloaded successfully.")
else:
    print(f"Failed to download file {filename}. Status Code: {response.status_code}")
