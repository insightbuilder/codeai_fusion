We'll define:

User Service (handles users)

Order Service (handles orders)

Auth Service (JWT authentication)

```
modular_monolith/
│── app/
│   ├── main.py                # Entry point for FastAPI
│   ├── core/
│   │   ├── database.py        # Database connection setup
│   │   ├── auth.py            # JWT authentication & password hashing
│   ├── routers/
│   │   ├── user_router.py     # User-related API routes
│   │   ├── order_router.py    # Order-related API routes
│   ├── services/
│   │   ├── user_service.py    # Business logic for users
│   │   ├── order_service.py   # Business logic for orders
│   ├── repositories/
│   │   ├── user_repository.py # Database interactions for users
│   │   ├── order_repository.py# Database interactions for orders
│── requirements.txt           # Dependencies
│── README.md                  # Project documentation

```

📁 Folder and Module Purpose

1️⃣ /core/ (Application Core)

database.py: Handles the database connection using
SQLAlchemy.

auth.py: Manages JWT authentication, token
creation, and password hashing.

2️⃣ /routers/ (API Endpoints)

user_router.py: Defines user-related routes
(registration, authentication).

order_router.py: Defines order-related routes
(placing & fetching orders).

3️⃣ /services/ (Business Logic)

user_service.py: Contains user-related logic
(hashing passwords, authentication).

order_service.py: Contains order processing logic.

4️⃣ /repositories/ (Database Layer)
user_repository.py: Contains database queries for
user CRUD operations.

order_repository.py: Contains database queries for
order CRUD operations.
