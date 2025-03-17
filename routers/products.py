from fastapi import APIRouter

from schemas.schemas import Product

# Se puede agregar un prefix a la ruta de la API, y los metodos de la ruta se agregarán automáticamente, por ejemplo:
# el primer método de la ruta es: /products
# el segundo método de la ruta es: /products/{id}

router = APIRouter(
    prefix="/products", tags=["products"], responses={404: {"message": "Not found"}}
)

product_list = [
    Product(id=1, name="Product 1", price=100),
    Product(id=2, name="Product 2", price=200),
    Product(id=3, name="Product 3", price=300),
]


@router.get("/", response_model=list[Product])
async def get_products():
    return product_list


@router.get("/{id}", response_model=Product)
async def get_product(id: int):
    return Product(id=id, name="Product 1", price=100)


@router.post("/", response_model=Product, status_code=201)
async def create_product(product: Product) -> Product:
    return product


@router.put("/", response_model=Product, status_code=200)
async def update_product(product: Product) -> Product:
    return product


@router.delete("/{id}", response_model=dict, status_code=200)
async def delete_product(id: int) -> dict:
    return {"message": f"Product deleted successfully{id}"}
