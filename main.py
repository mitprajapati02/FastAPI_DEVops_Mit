from fastapi import FastAPI

from controllers.product_controller import router as product_router


app = FastAPI(title="Product CRUD API")
app.include_router(product_router)

@app.get("/status")
async def read_root():
    return {"status": "ok"}