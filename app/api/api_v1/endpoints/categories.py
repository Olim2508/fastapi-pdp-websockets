from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
) -> Any:
    """
    Create new category.
    """
    category = crud.category.create(db=db, obj_in=category_in)
    return category


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """
    categories = crud.category.get_multi(db, skip=skip, limit=limit)
    return categories


@router.get("/{id}", response_model=schemas.Category)
def read_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get category by ID.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{id}", response_model=schemas.Category)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    category_in: schemas.CategoryUpdate,
) -> Any:
    """
    Update an item.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.update(db=db, db_obj=category, obj_in=category_in)
    return category


@router.delete("/{id}", response_model=schemas.Category)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an item.
    """
    category = crud.category.get(db=db, id=id)
    crud.post.delete_posts_of_category(db=db, category=category)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.remove(db=db, id=id)
    return category


@router.get("/test-api")
def get_test_api() -> Any:
    return []
