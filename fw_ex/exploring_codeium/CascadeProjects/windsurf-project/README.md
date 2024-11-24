# gRPC Store Management Server

## Overview
This is a gRPC-based store management server with SQLite database integration. It provides services for managing customers, products, inventory, and orders.

## Features
- Create, Read, Update, Delete operations for Customers
- Product management
- Inventory tracking
- Order processing

## Prerequisites
- Python 3.8+
- pip

## Setup
1. Clone the repository
2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Generate gRPC code
```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. store.proto
```

## Running the Server
```bash
python3 server.py
```

## Database
- SQLite database is automatically created as `store.db`
- Uses SQLAlchemy ORM for database interactions

## Services
The server provides gRPC services for:
- Customers
- Products
- Inventory
- Orders

## Error Handling
- Comprehensive error logging
- gRPC status codes for different error scenarios

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
[Your License Here]
