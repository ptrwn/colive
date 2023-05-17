from typing import Optional, List
from datetime import date, datetime
from enum import Enum

from sqlmodel import Field, SQLModel, Relationship


class UserRole(Enum):
    owner: str = "Owner"
    coliver: str = "Coliver"
    guest: str = "Guest"


class UserFlat(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    flat_id: Optional[int] = Field(default=None, foreign_key="flats.id", primary_key=True)
    # TODO: do we want to allow more that 1 main user for a flat? 
    user_role: UserRole

    user: "Users" = Relationship(back_populates="flat_links")
    flat: "Flats" = Relationship(back_populates="user_links")


class UsersBase(SQLModel):
    name: str

class Users(UsersBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: Optional[str] =  Field(default=None, unique=True)
    birth_date: Optional[date] 
    flat_links: Optional[List["UserFlat"]] = Relationship(back_populates="user")
    created_tasks: Optional[List["Tasks"]] = Relationship(
                    sa_relationship_kwargs=dict(
                        primaryjoin="Users.id==Tasks.creator_id",
                        ),
                    back_populates="creator")
    assigned_tasks: Optional[List["Tasks"]] = Relationship(
                    sa_relationship_kwargs=dict(
                        primaryjoin="Users.id==Tasks.assignee_id",
                        ),
                    back_populates="assignee")

class UserInFlat(UsersBase):
    id: int





class FlatsBase(SQLModel):
    name: str
    address: Optional[str] =  Field(default=None, unique=True)
    rent: Optional[float]

class Flats(FlatsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_links: Optional[List["UserFlat"]] = Relationship(back_populates="flat")
    tasks: Optional[List["Tasks"]] = Relationship(back_populates="flat")

class FlatsGet(FlatsBase):
    users: Optional[List["UserInFlat"]]
    tasks: Optional[List["TaskInFlat"]]



class FlatsGetAll(FlatsBase):
    id: int
    users: Optional[List["UserInFlat"]]
    tasks: Optional[List["TaskInFlat"]]



class TaskStatus(Enum):
    new: str = "New"
    done: str = "Done"
    canceled: str = "Canceled"


class TaskPriority(Enum):
    low: str = "Low"
    normal: str = "Normal"
    high: str = "High"


class TasksBase(SQLModel):
    name: str
    status: TaskStatus = Field(default=TaskStatus.new)
    deadline: Optional[datetime]
    priority: Optional[TaskPriority] = Field(default=TaskPriority.normal)
    is_expense: Optional[bool] 
    total: Optional[float]


class Tasks(TasksBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creator_id: int = Field(default=None, foreign_key="users.id")
    assignee_id: Optional[int] = Field(default=None, foreign_key="users.id")
    creator: Users = Relationship(
                    sa_relationship_kwargs=dict(primaryjoin="Tasks.creator_id==Users.id",),
                    back_populates="created_tasks")
    assignee: Optional[Users] = Relationship(
                    sa_relationship_kwargs=dict(primaryjoin="Tasks.assignee_id==Users.id",),
                    back_populates="assigned_tasks")
    flat_id: int = Field(default=None, foreign_key="flats.id")
    flat: Flats = Relationship(back_populates="tasks")

class TaskInFlat(TasksBase):
    id: int
    creator_id: int
    assignee_id: Optional[int]



FlatsGet.update_forward_refs(UserInFlat=UserInFlat) 
FlatsGet.update_forward_refs(TaskInFlat=TaskInFlat) 