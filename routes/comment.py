from models.models import Comment, CommentIn_Pydantic, Comment_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List


comment_router = APIRouter()


class Message(BaseModel):
    message: str
# Defining a simple Pydantic model for response messages (used in the delete operation), with a single field `message`.

@comment_router.get('/api/comment', response_model=List[Comment_Pydantic])
async def get_all_comments():
    return await Comment_Pydantic.from_queryset(Comment.all())

@comment_router.post('/api/comment', response_model=Comment_Pydantic)
async def create_a_comment(comment: CommentIn_Pydantic):
    commentobj = await Comment.create(**comment.dict(exclude_unset=True))
    return await Comment_Pydantic.from_tortoise_orm(commentobj)

@comment_router.get('/api/comment/{id}', response_model=Comment_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_a_comment(id: int):
    return await Comment_Pydantic.from_queryset_single(Comment.get(id=id))

@comment_router.put("/api/comment/{id}", response_model=Comment_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_a_comment(id: int, comment: CommentIn_Pydantic):
    await Comment.filter(id=id).update(**comment.dict(exclude_unset=True))
    return await Comment_Pydantic.from_queryset_single(comment.get(id=id))


@comment_router.delete("/api/comment/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_a_comment(id: int):
    delete_obj = await Comment.filter(id=id).delete()

    if not delete_obj:
        raise HTTPException(status_code=404, detail="This Comment is not found.")
    return Message(message="Successfully Deleted")
