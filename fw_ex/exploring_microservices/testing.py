import requests

# Add a new product
product = {"name": "Laptop", "price": 999.99}
response = requests.post("http://localhost:5001/product", json=product)
print("Add Product Response:", response.json())

# Get all products
response = requests.get("http://localhost:5001/products")
print("Get Products Response:", response.json())

# Add a new order
order = {"product_id": 1, "quantity": 2}
response = requests.post("http://localhost:5002/order", json=order)
print("Add Order Response:", response.json())

# Get all orders
response = requests.get("http://localhost:5002/orders")
print("Get Orders Response:", response.json())
