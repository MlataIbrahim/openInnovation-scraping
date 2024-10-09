from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

app = FastAPI()

client = MongoClient('mongodb://mongodb:27017')
db = client['steam_market']

def serialize_product(product):
    product["_id"] = str(product["_id"])
    return product

@app.get("/products/")
def get_products(offset: int = 0, limit: int = 10):
    """
    Get paginated products from MongoDB.
    """
    try:
        products_cursor = db.steam_market_items.find().skip(offset).limit(limit)
        products = [serialize_product(product) for product in products_cursor]

        if not products:
            raise HTTPException(status_code=404, detail="No products found")

        return {
            "offset": offset,
            "limit": limit,
            "total": db.steam_market_items.count_documents({}),
            "products": products
        }
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
