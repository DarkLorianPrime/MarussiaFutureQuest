from typing import Iterable, Dict, Any

from fastapi import Depends
from sqlalchemy import select, func, delete, Select, Result, Delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, get_session, Question, UserQuestion


class Service:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session: AsyncSession = session

    async def get_user(self, user_id: str) -> User:
        stmt: Select = select(User).where(User.user_id == user_id)
        result: Result = await self.session.execute(stmt)
        user: User | None = result.scalar()
        if not user:
            user: User = User(user_id=user_id)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

        return user

    async def get_question(self, questions: Iterable) -> Question | None:
        stmt: Select = select(Question).where(Question.id.not_in(questions)).order_by(func.random()).limit(1)
        result: Result = await self.session.execute(stmt)
        return result.scalar()

    async def set_question_user(self, user: User, question: Question) -> None:
        quest: UserQuestion = UserQuestion(question=question, user=user, answered=False)
        user.questions.append(quest)
        await self.session.commit()

    async def save_question(self, args: Dict[str, Any]) -> None:
        question: Question = Question(**args)
        self.session.add(question)
        await self.session.commit()

    async def answer_question(self, user: User, question: UserQuestion, text: str) -> None:
        question.answered = True
        if question.question.answer == text:
            user.points += question.question.points
        await self.session.commit()

    async def get_required_points(self) -> int:
        stmt: Select = select(func.sum(Question.points)).where(Question.required.is_(True))
        result: Result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def reset_user(self, user: User) -> None:
        user.points = 0
        stmt: Delete = delete(UserQuestion).where(UserQuestion.user_id == user.user_id)
        await self.session.execute(stmt)
        await self.session.commit()
