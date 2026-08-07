from fastapi import FastAPI
from products import products

app = FastAPI()

@app.get("/")
def welcome_page():
    return "Welcome to FastAPI"

@app.get("/products")
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return "Product not found"

@app.get("/products/search/{product_name}")
def get_product_by_name(product_name: str):
    for product in products:
        if product["name"] == product_name:
            return product
    return "Product not found"


@app.get("/greet")
def greet(name: str):
    return f"Hello, {name}!, what do you want?"



