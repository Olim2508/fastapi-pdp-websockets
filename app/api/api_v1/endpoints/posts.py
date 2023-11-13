from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps
from api.api_v1.utils import get_category_data

router = APIRouter()


@router.get("/")
def read_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
) -> Any:
    """
    Retrieve items.
    category is passed like category=1,2,3
    """
    category_id_list = category.split(",") if category else []
    posts, count = crud.post.get_multi_by_category(db, skip=skip, limit=limit, category_ids=category_id_list)

    posts_data = [
        {
            "id": post.id,
            "title": post.title,
            "author": post.author,
            "category": get_category_data(post),
            "created_at": post.created_at,
        }
        for post in posts
    ]
    return {"count": count, "result": posts_data}


@router.post("/")
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    post_in: schemas.PostCreate,
) -> Any:
    """
    Create new post.
    """
    category = crud.category.get(db=db, id=post_in.category)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    post_data = {
        'title': post_in.title,
        # 'author': post_in.author,
        'content': post_in.content,
    }
    post = crud.post.create_(db=db, obj_in=post_data, category=category, author_id=current_user.id)
    return post


@router.delete("/{id}", response_model=schemas.PostInDBBase)
def delete_post(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete post.
    """
    post = crud.post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post = crud.post.remove(db=db, id=id)
    return post


@router.get("/{id}", response_model=schemas.Post)
def read_post(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get post by ID.
    """
    post = crud.post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    post_in: schemas.PostUpdate,
) -> Any:
    """
    Update post.
    """
    post = crud.post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    category = crud.category.get(db=db, id=post_in.category)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    post = crud.post.update(db=db, db_obj=post, obj_in=post_in)
    return post


@router.get("/user-posts/")
def get_user_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    posts, count = crud.post.get_multi_by_user(db, skip=skip, limit=limit, user=current_user)
    return {
        "count": count,
        "result": posts,
    }
