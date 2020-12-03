from datetime import datetime

from fastapi import HTTPException, status
from slugify import slugify

from ..database.models import BaseTodo, TodoDoc
from ..database.utils import AIOMC, todos_db, todos_coll


async def get_all_todos(db: AIOMC):
	cursor = db[todos_db][todos_coll].find()
	return [doc async for doc in cursor]


async def get_todo_by_slug(slug: str, db: AIOMC):
	todo = await db[todos_db][todos_coll].find_one({'slug': slug})
	return todo


async def create_todo_by_slug(todo: BaseTodo, slug: str, db: AIOMC):
	doc = todo.dict()
	doc['slug'] = slug
	doc['updated_at'] = datetime.now()

	result = await db[todos_db][todos_coll].insert_one(doc)
	todo = await db[todos_db][todos_coll].find_one({'_id': result.inserted_id})
	return todo


async def update_todo_by_slug(slug: str, data: BaseTodo, doc: TodoDoc, db: AIOMC):
	doc['slug'] = slugify(data.title) if data.title else slug
	doc['title'] = data.title if data.title else doc.title
	doc['status'] = data.status if data.status else doc.status
	doc['priority'] = data.priority if data.priority else doc.priority
	doc['updated_at'] = datetime.now()

	await db[todos_db][todos_coll].replace_one({'slug': slug}, doc)
	return doc


async def delete_todo_by_slug(slug: str, db: AIOMC):
	await db[todos_db][todos_coll].delete_many({'slug': slug})


async def get_todo_or_404(slug: str, db: AIOMC):
	todo = await get_todo_by_slug(slug, db)

	if not todo:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Todo with slug '{slug}' does not exist"
		)

	return todo
