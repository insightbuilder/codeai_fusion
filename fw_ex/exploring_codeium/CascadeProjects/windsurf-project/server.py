import grpc
from concurrent import futures
import store_pb2
import store_pb2_grpc
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, Product, Inventory, Order, OrderItem
from datetime import datetime

engine = create_engine('sqlite:///store.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class StoreService(store_pb2_grpc.StoreServiceServicer):
    def CreateCustomer(self, request, context):
        session = Session()
        try:
            customer = Customer(
                name=request.name,
                email=request.email,
                phone=request.phone,
                address=request.address
            )
            session.add(customer)
            session.commit()
            
            return store_pb2.CustomerResponse(
                success=True,
                message="Customer created successfully",
                customer=store_pb2.Customer(
                    id=customer.id,
                    name=customer.name,
                    email=customer.email,
                    phone=customer.phone,
                    address=customer.address
                )
            )
        except Exception as e:
            session.rollback()
            return store_pb2.CustomerResponse(
                success=False,
                message=str(e)
            )
        finally:
            session.close()
    
    def GetCustomer(self, request, context):
        session = Session()
        try:
            customer = session.query(Customer).filter_by(id=request.id).first()
            if not customer:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Customer not found')
                return store_pb2.Customer()
            
            return store_pb2.Customer(
                id=customer.id,
                name=customer.name,
                email=customer.email,
                phone=customer.phone,
                address=customer.address
            )
        finally:
            session.close()
    
    def ListCustomers(self, request, context):
        session = Session()
        try:
            customers = session.query(Customer).all()
            return store_pb2.CustomerListResponse(
                customers=[
                    store_pb2.Customer(
                        id=c.id,
                        name=c.name,
                        email=c.email,
                        phone=c.phone,
                        address=c.address
                    ) for c in customers
                ]
            )
        finally:
            session.close()
    
    def CreateProduct(self, request, context):
        session = Session()
        try:
            product = Product(
                name=request.name,
                description=request.description,
                price=request.price
            )
            session.add(product)
            session.commit()
            
            # Create initial inventory entry
            inventory = Inventory(product_id=product.id, quantity=0)
            session.add(inventory)
            session.commit()
            
            return store_pb2.ProductResponse(
                success=True,
                message="Product created successfully",
                product=store_pb2.Product(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    price=product.price
                )
            )
        except Exception as e:
            session.rollback()
            return store_pb2.ProductResponse(
                success=False,
                message=str(e)
            )
        finally:
            session.close()
    
    def GetProduct(self, request, context):
        session = Session()
        try:
            product = session.query(Product).filter_by(id=request.id).first()
            if not product:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Product not found')
                return store_pb2.Product()
            
            return store_pb2.Product(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price
            )
        finally:
            session.close()
    
    def ListProducts(self, request, context):
        session = Session()
        try:
            products = session.query(Product).all()
            return store_pb2.ProductListResponse(
                products=[
                    store_pb2.Product(
                        id=p.id,
                        name=p.name,
                        description=p.description,
                        price=p.price
                    ) for p in products
                ]
            )
        finally:
            session.close()
    
    def UpdateInventory(self, request, context):
        session = Session()
        try:
            inventory = session.query(Inventory).filter_by(product_id=request.product_id).first()
            if not inventory:
                return store_pb2.InventoryResponse(
                    success=False,
                    message="Product not found in inventory"
                )
            
            # Instead of adding, we'll directly set the new quantity
            new_quantity = request.quantity_change
            if new_quantity < 0:
                return store_pb2.InventoryResponse(
                    success=False,
                    message="Quantity cannot be negative"
                )
            
            inventory.quantity = new_quantity
            session.commit()
            
            return store_pb2.InventoryResponse(
                success=True,
                message="Inventory updated successfully",
                current_quantity=inventory.quantity
            )
        except Exception as e:
            session.rollback()
            return store_pb2.InventoryResponse(
                success=False,
                message=str(e)
            )
        finally:
            session.close()
    
    def GetInventory(self, request, context):
        session = Session()
        try:
            inventory = session.query(Inventory).join(Product).filter(
                Inventory.product_id == request.id
            ).first()
            
            if not inventory:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Inventory not found')
                return store_pb2.InventoryItem()
            
            return store_pb2.InventoryItem(
                product_id=inventory.product_id,
                quantity=inventory.quantity,
                product=store_pb2.Product(
                    id=inventory.product.id,
                    name=inventory.product.name,
                    description=inventory.product.description,
                    price=inventory.product.price
                )
            )
        finally:
            session.close()
    
    def ListInventory(self, request, context):
        session = Session()
        try:
            inventory_items = session.query(Inventory).join(Product).all()
            return store_pb2.InventoryListResponse(
                items=[
                    store_pb2.InventoryItem(
                        product_id=item.product_id,
                        quantity=item.quantity,
                        product=store_pb2.Product(
                            id=item.product.id,
                            name=item.product.name,
                            description=item.product.description,
                            price=item.product.price
                        )
                    ) for item in inventory_items
                ]
            )
        finally:
            session.close()
    
    def CreateOrder(self, request, context):
        session = Session()
        try:
            # Validate customer exists
            customer = session.query(Customer).filter_by(id=request.customer_id).first()
            if not customer:
                return store_pb2.OrderResponse(
                    success=False,
                    message="Customer not found"
                )
            
            # Validate products and check inventory
            total_price = 0
            order_items = []
            
            for item in request.items:
                inventory = session.query(Inventory).filter_by(product_id=item.product_id).first()
                if not inventory:
                    return store_pb2.OrderResponse(
                        success=False,
                        message=f"Product {item.product_id} not found in inventory"
                    )
                
                if inventory.quantity < item.quantity:
                    return store_pb2.OrderResponse(
                        success=False,
                        message=f"Insufficient inventory for product {item.product_id}"
                    )
                
                # Calculate item price
                product = session.query(Product).filter_by(id=item.product_id).first()
                total_price += product.price * item.quantity
                
                # Create OrderItem
                order_items.append(OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity
                ))
                
                # Update inventory
                inventory.quantity -= item.quantity
            
            # Create order
            order = Order(
                customer_id=request.customer_id,
                total_price=total_price,
                status="PENDING",
                order_date=datetime.now(),
                items=order_items
            )
            
            session.add(order)
            session.commit()
            
            return store_pb2.OrderResponse(
                success=True,
                message="Order created successfully",
                order=store_pb2.Order(
                    id=order.id,
                    customer_id=order.customer_id,
                    items=[
                        store_pb2.OrderItem(
                            product_id=item.product_id,
                            quantity=item.quantity
                        ) for item in order.items
                    ],
                    status=order.status,
                    total_price=order.total_price,
                    order_date=order.order_date.isoformat(),
                    customer=store_pb2.Customer(
                        id=customer.id,
                        name=customer.name,
                        email=customer.email,
                        phone=customer.phone,
                        address=customer.address
                    )
                )
            )
        except Exception as e:
            session.rollback()
            return store_pb2.OrderResponse(
                success=False,
                message=str(e)
            )
        finally:
            session.close()
    
    def GetOrder(self, request, context):
        session = Session()
        try:
            order = session.query(Order).join(Customer).filter(Order.id == request.id).first()
            if not order:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Order not found')
                return store_pb2.Order()
            
            return store_pb2.Order(
                id=order.id,
                customer_id=order.customer_id,
                items=[
                    store_pb2.OrderItem(
                        product_id=item.product_id,
                        quantity=item.quantity
                    ) for item in order.items
                ],
                status=order.status,
                total_price=order.total_price,
                order_date=order.order_date.isoformat(),
                customer=store_pb2.Customer(
                    id=order.customer.id,
                    name=order.customer.name,
                    email=order.customer.email,
                    phone=order.customer.phone,
                    address=order.customer.address
                )
            )
        finally:
            session.close()
    
    def ListOrders(self, request, context):
        session = Session()
        try:
            orders = session.query(Order).join(Customer).all()
            return store_pb2.OrderListResponse(
                orders=[
                    store_pb2.Order(
                        id=order.id,
                        customer_id=order.customer_id,
                        items=[
                            store_pb2.OrderItem(
                                product_id=item.product_id,
                                quantity=item.quantity
                            ) for item in order.items
                        ],
                        status=order.status,
                        total_price=order.total_price,
                        order_date=order.order_date.isoformat(),
                        customer=store_pb2.Customer(
                            id=order.customer.id,
                            name=order.customer.name,
                            email=order.customer.email,
                            phone=order.customer.phone,
                            address=order.customer.address
                        )
                    ) for order in orders
                ]
            )
        finally:
            session.close()
    
    def UpdateOrderStatus(self, request, context):
        session = Session()
        try:
            order = session.query(Order).filter_by(id=request.order_id).first()
            if not order:
                return store_pb2.OrderResponse(
                    success=False,
                    message="Order not found"
                )
            
            order.status = request.new_status
            session.commit()
            
            return store_pb2.OrderResponse(
                success=True,
                message="Order status updated successfully",
                order=store_pb2.Order(
                    id=order.id,
                    customer_id=order.customer_id,
                    items=[
                        store_pb2.OrderItem(
                            product_id=item.product_id,
                            quantity=item.quantity
                        ) for item in order.items
                    ],
                    status=order.status,
                    total_price=order.total_price,
                    order_date=order.order_date.isoformat()
                )
            )
        except Exception as e:
            session.rollback()
            return store_pb2.OrderResponse(
                success=False,
                message=str(e)
            )
        finally:
            session.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_StoreServiceServicer_to_server(StoreService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
