from fastapi import APIRouter, HTTPException, status

from models.product_model import Product, ProductCreate, ProductUpdate, product_model
from views.product_view import ProductView


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductView])
async def list_products() -> list[Product]:
    return product_model.get_all()


@router.get("/{product_id}", response_model=ProductView)
async def get_product(product_id: int) -> Product:
    product = product_model.get_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.post("", response_model=ProductView, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate) -> Product:
    return product_model.create(product_data)


@router.patch("/{product_id}", response_model=ProductView)
async def update_product(
    product_id: int, product_data: ProductUpdate
) -> Product:
    product = product_model.update(product_id, product_data)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int) -> None:
    if not product_model.delete(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )