from typing import Optional, List
from datetime import date, datetime
from enum import Enum

from sqlmodel import Field, SQLModel, create_engine, Session, Relationship, select

engine = create_engine("postgresql+psycopg2://colive:123qwe@localhost/colive", echo=True)
session = Session(engine)

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


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
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


class Flats(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: Optional[str] =  Field(default=None, unique=True)
    rent: Optional[int]
    tasks: Optional[List["Tasks"]] = Relationship(back_populates="flat")
    user_links: Optional[List["UserFlat"]] = Relationship(back_populates="flat")


class TaskStatus(Enum):
    new: str = "New"
    done: str = "Done"
    canceled: str = "Canceled"


class TaskPriority(Enum):
    low: str = "Low"
    normal: str = "Normal"
    high: str = "High"


class Tasks(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: TaskStatus = Field(default=TaskStatus.new)
    deadline: Optional[datetime]
    priority: Optional[TaskPriority] = Field(default=TaskPriority.normal)
    is_expense: Optional[bool] 
    total: Optional[float]
    creator_id: int = Field(default=None, foreign_key="users.id")
    #creator: User = Relationship(back_populates="user")
    creator: Users = Relationship(
                    sa_relationship_kwargs=dict(primaryjoin="Tasks.creator_id==Users.id",),
                    back_populates="created_tasks")
    assignee_id: Optional[int] = Field(default=None, foreign_key="users.id")
    # assignee: Optional[User] = Relationship(back_populates="user")
    assignee: Optional[Users] = Relationship(
                    sa_relationship_kwargs=dict(primaryjoin="Tasks.assignee_id==Users.id",),
                    back_populates="assigned_tasks")
    flat_id: int = Field(default=None, foreign_key="flats.id")
    flat: Flats = Relationship(back_populates="tasks")


def fill_in_db():
    with session:
        user_a = Users(name="Ann Owner")
        user_b = Users(name="Boris Coliver")
        user_c = Users(name="Clara Coliver")
        user_d = Users(name="Diana Guest")
        user_e = Users(name="Elsa Owner")
        user_f = Users(name="Fred Coliver Guest")

        flat_1 = Flats(name="Astana")
        flat_2 = Flats(name="Hamburg")

        a_1 = UserFlat(user=user_a, flat=flat_1, user_role="Owner")
        b_1 = UserFlat(user=user_b, flat=flat_1, user_role="Coliver")
        c_1 = UserFlat(user=user_c, flat=flat_1, user_role="Coliver")
        d_1 = UserFlat(user=user_d, flat=flat_1, user_role="Guest")

        e_2 = UserFlat(user=user_e, flat=flat_2, user_role="Owner")
        f_2 = UserFlat(user=user_f, flat=flat_2, user_role="Coliver")

        f_1 = UserFlat(user=user_f, flat=flat_1, user_role="Guest")

        t_a_b_1 = Tasks(name="dishes", creator_id=1, assignee_id=2, flat_id=1)
        t_b_c_1 = Tasks(name="dust", creator_id=2, assignee_id=3, flat_id=1)
        t_c_d_1 = Tasks(name="take out garbage", creator_id=3, assignee_id=4, flat_id=1)
        t_d_f_1 = Tasks(name="cook", creator_id=4, assignee_id=6, flat_id=1)
        t_a_c_1 = Tasks(name="walk the dog", creator_id=1, assignee_id=3, flat_id=1)
        t_b_d_1 = Tasks(name="clean cat toilet", creator_id=2, assignee_id=4, flat_id=1)
        t_c_a_1 = Tasks(name="washing", creator_id=3, assignee_id=1, flat_id=1)
        t_e_f_2 = Tasks(name="iron curtains", creator_id=5, assignee_id=6, flat_id=2)


        session.add_all([user_a, user_b, user_c, user_d, user_e, user_f, flat_1, flat_2, a_1, b_1, c_1, d_1, f_1, e_2, f_2, t_a_b_1, t_b_c_1, t_c_d_1, t_d_f_1, t_a_c_1, t_b_d_1, t_c_a_1, t_e_f_2])

        session.commit()


SQLModel.metadata.create_all(engine)
fill_in_db()


def select_flats():
    with session:
        statement = select(Flats)
        results = session.exec(statement)
        for flat in results:
            print(flat)
            print(flat.user_links)
            print("==============")


select_flats()