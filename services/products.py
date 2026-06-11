from typing import List, Dict
import json
from pathlib import Path

DATA_FILE= Path(__file__).parent.parent/"data"/"products.json"

def load_products()->List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
def getAllProducts()->List[Dict]:
    return load_products()


def save_products(products:List[Dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

def add_products(product:Dict):
    products=getAllProducts()
    if any(p["sku"]==product["sku"] for p in products):
        raise ValueError(f"Product with SKU {product['sku']} already exists.")
    products.append(product)
    save_products(products)
    return product
