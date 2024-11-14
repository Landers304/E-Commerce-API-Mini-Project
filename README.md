# E-Commerce API

Welcome to the **E-Commerce API** project! This API is designed to manage e-commerce platforms by providing CRUD operations for products, users, and orders. It also features secure user authentication with JWT (JSON Web Tokens).

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [API Endpoints](#api-endpoints)
4. [Usage](#usage)

## Features

- **User registration** and authentication using JWT tokens.
- **Product management**: CRUD (Create, Read, Update, Delete) operations for products.
- **Secure endpoints**: JWT-based authorization for secure routes.
- **Order management**: Place, view, and manage orders.
- **Database integration**: MySQL database used for persistent storage.

## Installation

To get started with this project, you need to install the necessary dependencies and set up your local development environment.

### Prerequisites

- Python 3.x
- MySQL or another compatible database
- Virtual environment (optional but recommended)

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ecommerce-api.git
    cd ecommerce-api
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Configure your database**:
    - Create a MySQL database and set up the connection settings in your `.env` file or configuration.
    - The database should be named `ecommerce_db` (you can adjust the name in the config).

6. **Run the application**:
    ```bash
    python app.py
    ```

## API Endpoints

Here are the available endpoints for the **E-Commerce API**.

### 1. Authentication

- **POST** `/auth/register` - Register a new user.
- **POST** `/auth/login` - Login an existing user and receive a JWT.

### 2. Products

- **GET** `/products` - Get all products.
- **POST** `/products` - Create a new product.
- **PUT** `/products/<product_id>` - Update an existing product.
- **DELETE** `/products/<product_id>` - Delete a product.

### 3. Orders

- **GET** `/orders` - Get all orders.
- **POST** `/orders` - Place a new order.

### 4. Users (admin only)

- **GET** `/users` - Get a list of users (admin only).
- **DELETE** `/users/<user_id>` - Delete a user (admin only).

> **Note**: All endpoints except `/auth/register` and `/auth/login` require authentication via a JWT token. Use the token obtained after logging in.

## Usage

To interact with the API, you can use a tool like **Postman** or **Insomnia**, or send HTTP requests directly using `curl` or any other client.
