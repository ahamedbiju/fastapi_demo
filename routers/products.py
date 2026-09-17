from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from db_models import Product as DBProduct
from db_models import User as DBUser
from models import Product, ProductCreate, ProductUpdate, User
from auth import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(DBProduct).all()


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    new_product = DBProduct(
        name=product.name,
        price=product.price,
        owner_id=current_user.id,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.put("/{product_id}", response_model=Product)
def put_product(
    product_id: int,
    updated_product: Product,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if updated_product.id != product_id:
        raise HTTPException(
            status_code=400,
            detail="Product ID in the path and request body do not match",
        )

    product.name = updated_product.name
    product.price = updated_product.price

    db.commit()
    db.refresh(product)

    return product


@router.patch("/{product_id}", response_model=Product)
def patch_product(
    product_id: int,
    updated_product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    updates = updated_product.model_dump(exclude_unset=True)
    updates.pop("owner_id", None)

    for key, value in updates.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}


@router.get("/{product_id}/owner", response_model=User)
def get_product_owner(product_id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product.owner