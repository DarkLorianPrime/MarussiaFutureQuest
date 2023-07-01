from os import getenv

from sqlalchemy import Integer, Boolean, String, Column, ForeignKey
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

postgres_user = getenv("POSTGRES_USER")
postgres_password = getenv("POSTGRES_PASSWORD")
postgres_host = getenv("POSTGRES_HOST")
postgres_name = getenv("POSTGRES_NAME")

url = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_name}"
engine = create_async_engine(url)

session = async_sessionmaker(bind=engine, class_=AsyncSession)


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with session(expire_on_commit=False) as s:
        yield s


class Base(DeclarativeBase):
    ...


class UserQuestion(Base):
    __tablename__ = "user_question"

    user_id = Column(ForeignKey("user.user_id"), primary_key=True)
    question_id = Column(ForeignKey("question.id"), primary_key=True)
    answered = Column(Boolean)

    user = relationship("User", back_populates="questions", lazy="selectin")
    question = relationship("Question", lazy="selectin")


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[str] = mapped_column(String, primary_key=True)
    points: Mapped[int] = mapped_column(Integer, default=0)
    questions = relationship("UserQuestion", back_populates="user", lazy="selectin")


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    required: Mapped[bool] = mapped_column(Boolean)
    title: Mapped[str] = mapped_column(String)
    tts: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    answer: Mapped[str] = mapped_column(String)
    points: Mapped[int] = mapped_column(Integer)
