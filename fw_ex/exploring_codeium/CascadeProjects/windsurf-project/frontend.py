from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
import grpc
import store_pb2
import store_pb2_grpc

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure secret key
bootstrap = Bootstrap5(app)

# gRPC channel
channel = grpc.insecure_channel('localhost:50051')
stub = store_pb2_grpc.StoreServiceStub(channel)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        try:
            customer = store_pb2.Customer(
                name=request.form['name'],
                email=request.form['email'],
                phone=request.form['phone'],
                address=request.form['address']
            )
            response = stub.CreateCustomer(customer)
            if response.success:
                flash('Customer created successfully!', 'success')
            else:
                flash(f'Error: {response.message}', 'error')
        except grpc.RpcError as e:
            flash(f'Error: {e.details()}', 'error')
    
    try:
        response = stub.ListCustomers(store_pb2.Empty())
        customers_list = response.customers
    except grpc.RpcError as e:
        flash(f'Error loading customers: {e.details()}', 'error')
        customers_list = []
    
    return render_template('customers.html', customers=customers_list)

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        try:
            product = store_pb2.Product(
                name=request.form['name'],
                description=request.form['description'],
                price=float(request.form['price'])
            )
            response = stub.CreateProduct(product)
            if response.success:
                flash('Product created successfully!', 'success')
            else:
                flash(f'Error: {response.message}', 'error')
        except grpc.RpcError as e:
            flash(f'Error: {e.details()}', 'error')
    
    try:
        response = stub.ListProducts(store_pb2.Empty())
        products_list = response.products
    except grpc.RpcError as e:
        flash(f'Error loading products: {e.details()}', 'error')
        products_list = []
    
    return render_template('products.html', products=products_list)

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        try:
            inventory_update = store_pb2.InventoryUpdate(
                product_id=int(request.form['product_id']),
                quantity=int(request.form['quantity'])
            )
            response = stub.UpdateInventory(inventory_update)
            if response.success:
                flash('Inventory updated successfully!', 'success')
            else:
                flash(f'Error: {response.message}', 'error')
        except grpc.RpcError as e:
            flash(f'Error: {e.details()}', 'error')
    
    try:
        # Get products for the dropdown
        products_response = stub.ListProducts(store_pb2.Empty())
        products_list = products_response.products
        
        # Get inventory items
        inventory_response = stub.ListInventory(store_pb2.Empty())
        inventory_list = inventory_response.items
    except grpc.RpcError as e:
        flash(f'Error loading data: {e.details()}', 'error')
        products_list = []
        inventory_list = []
    
    return render_template('inventory.html', 
                         products=products_list,
                         inventory=inventory_list)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        try:
            # Process order items
            order_items = []
            product_ids = request.form.getlist('items[][product_id]')
            quantities = request.form.getlist('items[][quantity]')
            
            for product_id, quantity in zip(product_ids, quantities):
                if product_id and quantity:
                    order_items.append(store_pb2.OrderItem(
                        product_id=int(product_id),
                        quantity=int(quantity)
                    ))
            
            order = store_pb2.Order(
                customer_id=int(request.form['customer_id']),
                items=order_items
            )
            
            response = stub.CreateOrder(order)
            if response.success:
                flash('Order created successfully!', 'success')
            else:
                flash(f'Error: {response.message}', 'error')
        except grpc.RpcError as e:
            flash(f'Error: {e.details()}', 'error')
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'error')
    
    try:
        # Get customers for the dropdown
        customers_response = stub.ListCustomers(store_pb2.Empty())
        customers_list = customers_response.customers
        
        # Get products for the dropdown
        products_response = stub.ListProducts(store_pb2.Empty())
        products_list = products_response.products
        
        # Get orders
        orders_response = stub.ListOrders(store_pb2.Empty())
        orders_list = orders_response.orders
    except grpc.RpcError as e:
        flash(f'Error loading data: {e.details()}', 'error')
        customers_list = []
        products_list = []
        orders_list = []
    
    return render_template('orders.html',
                         customers=customers_list,
                         products=products_list,
                         orders=orders_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
