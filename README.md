# Product API with JWT Authentication
This API provides endpoints to manage products, using Flask and SQLAlchemy with JWT-based authentication.

## Features
* JWT Authentication: Secure access to all endpoints.
* CRUD Operations: Create, Read, Update, Delete operations on products.
* Input Validation: Validate incoming data with marshmallow.
* Pagination: Use query parameters limit and skip for pagination.

## Prerequisites
* Python 3.6 or higher
* pip (Python package installer)

## Installation
1. Clone the Repository
```
git clone https://github.com/raithal98/BirdVision.git
cd BirdVision
```
2.  Install dependencies
```
pip install -r requirements.txt
```
3. Setup the SQLite Database
```
python3 restApi.py
```

## Authentication Endpoints
1. Register Endpoint: POST /register
```
curl -X POST -H "Content-Type: application/json" -d '{"username":"user1","password":"password123"}' http://127.0.0.1:5000/register
```
2. Login Endpoint: POST /login
```
curl -X POST -H "Content-Type: application/json" -d '{"username":"user1","password":"password123"}' http://127.0.0.1:5000/login
```
3. Get All Products Endpoint: GET /products
```
curl -H "Authorization: Bearer <JWT>" http://127.0.0.1:5000/products
```
4. Get a Product by ID Endpoint: GET /products/{id}
```
curl -H "Authorization: Bearer <JWT>" http://127.0.0.1:5000/products/1
```
5. Create a New Product Endpoint: POST /products
```
curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"title":"New Product","description":"A great product","price":19.99}' http://127.0.0.1:5000/products
```
6. Update a Product by ID Endpoint: PUT /products/{id}
```
curl -X PUT -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" -d '{"title":"Updated Product","description":"Updated description","price":29.99}' http://127.0.0.1:5000/products/1
```
7. Delete a Product by ID Endpoint: DELETE /products/{id}
```
curl -X DELETE -H "Authorization: Bearer <JWT>" http://127.0.0.1:5000/products/1
```