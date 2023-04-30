from typing import Optional, List
from datetime import date, datetime
from enum import Enum

from sqlmodel import Field, SQLModel, create_engine, Session, Relationship

engine = create_engine("postgresql+psycopg2://colive:123qwe@localhost/colive", echo=True)
session = Session(engine)

class UserRole(Enum):
    owner: str = "Owner"
    coliver: str = "Coliver"
    guest: str = "Guest"


class UserFlat(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    flat_id: Optional[int] = Field(default=None, foreign_key="flat.id", primary_key=True)
    # TODO: do we want to allow more that 1 main user for a flat? 
    user_role: UserRole

    user: "User" = Relationship(back_populates="flat_links")
    flat: "Flat" = Relationship(back_populates="user_links")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] =  Field(default=None, unique=True)
    birth_date: Optional[date] 
    flat_links: Optional[List["UserFlat"]] = Relationship(back_populates="user")
    created_tasks: Optional[List["Task"]] = Relationship(
                    sa_relationship_kwargs=dict(
                        primaryjoin="User.id==Task.creator_id",
                        ),
                    back_populates="Task.creator")
    assigned_tasks: Optional[List["Task"]] = Relationship(
                    sa_relationship_kwargs=dict(
                        primaryjoin="User.id==Task.assignee_id",
                        ),
                    back_populates="Task.assignee")


class Flat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: Optional[str] =  Field(default=None, unique=True)
    rent: Optional[int]
    tasks: Optional[List["Task"]] = Relationship(back_populates="flat")
    user_links: Optional[List["UserFlat"]] = Relationship(back_populates="flat")


class TaskStatus(Enum):
    new: str = "New"
    done: str = "Done"
    canceled: str = "Canceled"


class TaskPriority(Enum):
    low: str = "Low"
    normal: str = "Normal"
    high: str = "High"


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: TaskStatus = Field(default=TaskStatus.new)
    deadline: Optional[datetime]
    priority: Optional[TaskPriority] = Field(default=TaskPriority.normal)
    is_expense: Optional[bool] 
    total: Optional[float]
    creator_id: int = Field(default=None, foreign_key="user.id")
    #creator: User = Relationship(back_populates="user")
    creator: User = Relationship(
                    sa_relationship_kwargs=dict(primaryjoin="Task.creator_id==User.id",),
                    back_populates="User.created_tasks")
    assignee_id: Optional[int] = Field(default=None, foreign_key="user.id")
    # assignee: Optional[User] = Relationship(back_populates="user")
    assignee: Optional[User] = Relationship(
                    sa_relationship_kwargs=dict(primaryjoin="Task.assignee_id==User.id",),
                    back_populates="User.assigned_tasks")
    flat_id: int = Field(default=None, foreign_key="flat.id")
    flat: Flat = Relationship(back_populates="tasks")
    




def fill_in_db():
    with session:
        user_a = User(name="Ann Owner")
        user_b = User(name="Boris Coliver")
        user_c = User(name="Clara Coliver")
        user_d = User(name="Diana Guest")
        user_e = User(name="Elsa Owner")
        user_f = User(name="Fred Coliver Guest")

        flat_1 = Flat(name="Astana")
        flat_2 = Flat(name="Hamburg")

        a_1 = UserFlat(user=user_a, flat=flat_1, user_role="Owner")
        b_1 = UserFlat(user=user_b, flat=flat_1, user_role="Coliver")
        c_1 = UserFlat(user=user_c, flat=flat_1, user_role="Coliver")
        d_1 = UserFlat(user=user_d, flat=flat_1, user_role="Guest")

        e_2 = UserFlat(user=user_e, flat=flat_2, user_role="Owner")
        f_2 = UserFlat(user=user_f, flat=flat_2, user_role="Coliver")

        f_1 = UserFlat(user=user_f, flat=flat_1, user_role="Guest")

        session.add_all([user_a, user_b, user_c, user_d, user_e, user_f, flat_1, flat_2, a_1, b_1, c_1, d_1, f_1, e_2, f_2])

        session.commit()


SQLModel.metadata.create_all(engine)
fill_in_db()