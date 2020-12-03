from datetime import datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseConfig, BaseModel, Field
from typing import List, Optional


class Status(str, Enum):
	pending = 'pending'
	ongoing = 'ongoing'
	complete = 'complete'


class Priority(str, Enum):
	high = 'high'
	medium = 'medium'
	low = 'low'


class BaseTodo(BaseModel):
	title: str 
	priority: Priority = Priority.medium
	status: Status = Status.pending

	class Config(BaseConfig):
		allow_population_by_field_name = True


class DBModel(BaseModel):
	id: Optional[str] = None
	created_at: Optional[datetime] = Field(..., alias='createdAt')
	updated_at: Optional[datetime] = Field(..., alias='updatedAt')


class TodoDoc(DBModel, BaseTodo):
	slug: str


class TodoList(BaseModel):
	count: int
	todos: List[TodoDoc]


def todo_helper(todo):
	todo_id = str(todo['_id'])
	created = ObjectId(todo['_id']).generation_time
	return TodoDoc(**todo, created_at=created, id=todo_id)