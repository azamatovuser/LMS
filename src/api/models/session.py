from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, func, Enum
from sqlalchemy.orm import relationship
from api.database import Base
import enum

class Status(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    COMPLETED = "completed"

class TimeStampMixin:
    status = Column(Enum(Status), default=Status.CLOSED)
    created_date = Column(DateTime, default=func.now())

class UserCourseSession(Base, TimeStampMixin):
    __tablename__ = 'user_course_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('account_account.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

class UserModuleSession(Base, TimeStampMixin):
    __tablename__ = 'user_module_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('account_account.id'))
    module_id = Column(Integer, ForeignKey('modules.id'))
    score = Column(Float)

class UserLessonSession(Base, TimeStampMixin):
    __tablename__ = 'user_lesson_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('account_account.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.id'))

class UserAnswerSession(Base, TimeStampMixin):
    __tablename__ = 'user_answer_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('account_account.id'))
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    correct = Column(Integer)
    not_correct = Column(Integer)

class Answer(Base, TimeStampMixin):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('account_account.id'))
    option_id = Column(Integer, ForeignKey('options.id'))
