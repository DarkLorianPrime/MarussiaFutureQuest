from typing import Iterable

from fastapi import Depends
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, get_session, Question, UserQuestion

state: dict = {}


class Service:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session: AsyncSession = session

    async def get_user(self, user_id: str) -> User:
        stmt = select(User).where(User.user_id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar()
        if not user:
            user = User(user_id=user_id)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

        return user

    async def get_question(self, questions: Iterable) -> Question:
        stmt = select(Question).where(Question.id.not_in(questions)).order_by(func.random()).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def set_question_user(self, user: User, question: Question) -> None:
        quest = UserQuestion(question=question, user=user, answered=False)
        user.questions.append(quest)
        await self.session.commit()

    async def save_question(self, args):
        question = Question(**args)
        self.session.add(question)
        await self.session.commit()

    async def answer_question(self, user, question: UserQuestion, text):
        question.answered = True
        if question.question.answer == text:
            user.points += question.question.points
        await self.session.commit()

    async def get_required_points(self):
        stmt = select(func.sum(Question.points)).where(Question.required.is_(True))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def reset_user(self, user):
        user.points = 0
        stmt = delete(UserQuestion).where(UserQuestion.user_id == user.user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        # user.questions[:] = []
