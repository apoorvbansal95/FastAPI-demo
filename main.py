from uuid import uuid4

from fastapi import FastAPI, Query, HTTPException
app=FastAPI()
from app.schema.product import Product
from services.products import add_products, getAllProducts
from datetime import datetime

@app.get("/")
def root():
    return {"message":"HEllo world"}

@app.get("/items/{itemId}")
def getItem(itemId: int ):
    products=["laptop", "mobile", "tablet", "watch"]
    return products[itemId]

# @app.get("/products")
# def getallItems():
#     return getAllProducts()

@app.get("/products")
def list_products(name: str= Query(default=None, min_length=4, max_length=50 , description="search product by name"), 
                  sort_by_price: bool=Query(default=False, description="sort by price"), 
                   order: str=Query(default="asc", description="Sort order when sort_by_price is true (asc, desc)"), 
                   limit: int=Query(default=5, ge=1, le=100, description="Number of results") ):
    products=getAllProducts()
    
    if name:
        needle=name.strip().lower()
        products=[p for p in products if needle in p.get("name", "").lower()]
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    
    if sort_by_price:
        reverse= order=="desc" 
        products=sorted(products, key=lambda x:x.get("price", 0), reverse=reverse)
    products=products[0:limit]
    total= len(products)
    return {"total":total,"products":products}


@app.post("/products", status_code=201)
def create_product(product:Product):
    product_dict=product.model_dump()
    product_dict["id"]=str(uuid4())
    product_dict["created_at"]=datetime.utcnow().isoformat()+"Z"
    try:
        add_products(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return product.model_dump(mode="json")