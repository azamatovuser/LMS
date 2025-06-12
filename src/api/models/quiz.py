from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from api.database import Base

class TimeStampMixin:
    order = Column(Integer)
    created_date = Column(DateTime, default=func.now())

class LocalizationBaseMixin:
    title = Column(String(100))
    description = Column(Text, nullable=True)
    language_type = Column(String(50))

class Quiz(Base, TimeStampMixin):
    __tablename__ = 'quiz_quiz'

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    module_id = Column(Integer, ForeignKey('modules.id'))
    
    quiz_localization = relationship("QuizLocalizationItem", back_populates="quiz", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")

class QuizLocalizationItem(Base, LocalizationBaseMixin):
    __tablename__ = 'quiz_quizlocalizationitem'

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    quiz = relationship("Quiz", back_populates="quiz_localization")

class Question(Base, TimeStampMixin):
    __tablename__ = 'quiz_question'

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    
    question_localization = relationship("QuestionLocalizationItem", back_populates="question", cascade="all, delete-orphan")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")

class QuestionLocalizationItem(Base, LocalizationBaseMixin):
    __tablename__ = 'quiz_questionlocalizationitem'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship("Question", back_populates="question_localization")

class Option(Base, TimeStampMixin):
    __tablename__ = 'quiz_option'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    is_correct = Column(Boolean, default=False)
    
    option_localization = relationship("OptionLocalizationItem", back_populates="option", cascade="all, delete-orphan")

class OptionLocalizationItem(Base, LocalizationBaseMixin):
    __tablename__ = 'quiz_optionlocalizationitem'

    id = Column(Integer, primary_key=True, index=True)
    option_id = Column(Integer, ForeignKey('options.id'))
    option = relationship("Option", back_populates="option_localization")
