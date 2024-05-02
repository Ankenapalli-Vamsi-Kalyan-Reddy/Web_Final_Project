# Dosa Restaurant Backend API

This project implements a REST API backend for a dosa restaurant using FastAPI and SQLite database.

## Setup
## Ensure compatibility with Python version 3 and higher.
1. **Install dependencies:**

   - pip install fastapi
   - pip install pydantic
   - pip install uvicorn

## Database Initialization

2. **To initialize the database, run the following command:**

   python init_db.py

## Endpoints

### Customers

3. **clear overview of the endpoints and their functionality in a concise manner**
- **POST /customers:** Create a new customer.
- **GET /customers/{id}:** Retrieve customer information by ID.
- **DELETE /customers/{id}:** Delete a customer by ID.
- **PUT /customers/{id}:** Update customer information by ID.

These endpoints allow you to manage customer data, including creating, retrieving, updating, and deleting customer records.

### Items

- **POST /items:** Create a new menu item.
- **GET /items/{id}:** Retrieve menu item information by ID.
- **DELETE /items/{id}:** Delete a menu item by ID.
- **PUT /items/{id}:** Update menu item information by ID.

These endpoints enable you to handle menu items, such as adding, viewing, modifying, and removing items from the menu.

### Orders

- **POST /orders:** Place a new order.
- **GET /orders/{id}:** Retrieve order information by ID.
- **DELETE /orders/{id}:** Delete an order by ID.
- **PUT /orders/{id}:** Update order information by ID.

These endpoints facilitate order management, allowing users to create, view, update, and cancel orders.

## To run fastapi server

   uvicorn main:app 
   Note: main is my file name. Replace main with your file name.

After running the above command the server runs successfully by generating a url. Copy the url(http://127.0.0.1:8000) and paste it in a new tab and add /docs to the url. It looks like this http://127.0.0.1:8000/docs. After successfully running the URL we get fastapi interface with all the endpoints. There we can perform all the CRUD operations.

### Important Note for POST Method

While using the POST method for all three tables, ensure that you delete the `"id": 0` generated by FastAPI and fill in the other columns as per your requirements.

