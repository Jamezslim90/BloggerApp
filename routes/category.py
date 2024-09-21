from models.models import Category, CategoryIn_Pydantic, Category_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List


category_router = APIRouter()


class Message(BaseModel):
    message: str
# Defining a simple Pydantic model for response messages (used in the delete operation), with a single field `message`.

@category_router.get('/api/category', response_model=List[Category_Pydantic])
async def get_all_categories():
    return await Category_Pydantic.from_queryset(Category.all())

@category_router.category('/api/category', response_model=Category_Pydantic)
async def create_a_category(category: CategoryIn_Pydantic):
    categoryobj = await category.create(**category.dict(exclude_unset=True))
    return await Category_Pydantic.from_tortoise_orm(categoryobj)

@category_router.get('/api/category/{id}', response_model=Category_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_a_category(id: int):
    return await Category_Pydantic.from_queryset_single(Category.get(id=id))

@category_router.put("/api/category/{id}", response_model=Category_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_a_category(id: int, category: CategoryIn_Pydantic):
    await Category.filter(id=id).update(**category.dict(exclude_unset=True))
    return await Category_Pydantic.from_queryset_single(category.get(id=id))


@category_router.delete("/api/category/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_a_category(id: int):
    delete_obj = await Category.filter(id=id).delete()

    if not delete_obj:
        raise HTTPException(status_code=404, detail="This Category is not found.")
    return Message(message="Successfully Deleted")
