from fastapi import APIRouter, Depends, HTTPException, status
from slugify import slugify

from .crud import (
    create_todo_by_slug,
    delete_todo_by_slug,
    get_all_todos,
    get_todo_by_slug,
    get_todo_or_404,
    update_todo_by_slug,
)
from ..database.models import BaseTodo, TodoList, TodoDoc, todo_helper
from ..database.utils import AIOMC, get_database

router = APIRouter()


@router.get("/", response_model=TodoList)
async def list_todos(db: AIOMC = Depends(get_database)):
    todos = await get_all_todos(db)
    formatted = [todo_helper(todo) for todo in todos]
    return TodoList(count=len(todos), todos=formatted)


@router.get("/{slug}", response_model=TodoDoc)
async def retrieve_todo(slug: str, db: AIOMC = Depends(get_database)):
    todo = await get_todo_or_404(slug, db)
    return todo_helper(todo)


@router.post("/", response_model=TodoDoc, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: BaseTodo, db: AIOMC = Depends(get_database)):
    slug = slugify(todo.title)
    exists = await get_todo_by_slug(slug, db)

    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Todo with slug '{slug}' already exists",
        )

    todo = await create_todo_by_slug(todo, slug, db)
    return todo_helper(todo)


@router.put("/{slug}", response_model=TodoDoc)
async def update_todo(
    slug: str, data: BaseTodo, db: AIOMC = Depends(get_database)
):
    doc = await get_todo_or_404(slug, db)
    updated = await update_todo_by_slug(slug, data, doc, db)
    return todo_helper(updated)


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(slug: str, db: AIOMC = Depends(get_database)):
    _ = await get_todo_or_404(slug, db)
    await delete_todo_by_slug(slug, db)
