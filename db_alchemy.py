from sqlalchemy import create_engine

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


# engine = create_engine("sqlite:///colive.db", echo=True)
engine = create_engine("postgresql+psycopg2://colive@localhost/colive")
Base = declarative_base()

Session = sessionmaker(bind=engine)
sess = Session()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255), nullable=True, unique=True)
    birth_date = Column(Date(), nullable=True, default=None)


class Flat(Base):
    __tablename__ = "flat"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255), nullable=True)
    rent = Column(Integer, nullable=True)


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    status = Column(Enum('New', 'Done', 'Canceled'))
    deadline = Column(DateTime(), nullable=True, default=None)
    priority = Column(Enum('low', 'normal', 'high'), nullable=True)
    is_expense = Column(Boolean, nullable=True)
    total = Column(Integer, nullable=True)