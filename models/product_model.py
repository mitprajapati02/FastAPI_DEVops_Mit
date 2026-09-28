from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=500)
    price: float | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)


class ProductModel:
    """In-memory product model and CRUD operations."""

    def __init__(self) -> None:
        self._products: list[Product] = [
            Product(
                id=1,
                name="Notebook",
                description="A5 ruled notebook",
                price=4.99,
                quantity=25,
            ),
            Product(
                id=2,
                name="Ballpoint Pen",
                description="Blue ink ballpoint pen",
                price=1.49,
                quantity=100,
            ),
        ]
        self._next_id = 3

    def get_all(self) -> list[Product]:
        return self._products

    def get_by_id(self, product_id: int) -> Product | None:
        return next(
            (product for product in self._products if product.id == product_id),
            None,
        )

    def create(self, product_data: ProductCreate) -> Product:
        product = Product(id=self._next_id, **product_data.model_dump())
        self._products.append(product)
        self._next_id += 1
        return product

    def update(
        self, product_id: int, product_data: ProductUpdate
    ) -> Product | None:
        product = self.get_by_id(product_id)
        if product is None:
            return None

        updated_product = product.model_copy(
            update=product_data.model_dump(exclude_unset=True)
        )
        product_index = self._products.index(product)
        self._products[product_index] = updated_product
        return updated_product

    def delete(self, product_id: int) -> bool:
        product = self.get_by_id(product_id)
        if product is None:
            return False

        self._products.remove(product)
        return True


product_model = ProductModel()