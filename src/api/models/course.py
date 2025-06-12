from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from api.database import Base

class TimeStampMixin:
    order = Column(Integer)
    created_date = Column(DateTime, default=func.now())

class LocalizationBaseMixin:
    title = Column(String(100))
    description = Column(Text)
    language_type = Column(String(50))

class Course(Base, TimeStampMixin):
    __tablename__ = 'course_course'

    id = Column(Integer, primary_key=True, index=True)
    course_localization = relationship("CourseLocalizationItem", back_populates="course", cascade="all, delete-orphan")
    modules = relationship("Module", back_populates="course")

class CourseLocalizationItem(Base, LocalizationBaseMixin):
    __tablename__ = 'course_courselocalizationitem'

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship("Course", back_populates="course_localization")

class Module(Base, TimeStampMixin):
    __tablename__ = 'course_module'

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=True)
    course = relationship("Course", back_populates="modules")
    module_localization = relationship("ModuleLocalizationItem", back_populates="module", cascade="all, delete-orphan")
    lessons = relationship("Lesson", back_populates="module")

class ModuleLocalizationItem(Base, LocalizationBaseMixin):
    __tablename__ = 'course_modulelocalizationitem'

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey('modules.id'))
    module = relationship("Module", back_populates="module_localization")

class Lesson(Base, TimeStampMixin):
    __tablename__ = 'course_lesson'

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=True)
    module = relationship("Module", back_populates="lessons")
    lesson_localization = relationship("LessonLocalizationItem", back_populates="lesson", cascade="all, delete-orphan")

class LessonLocalizationItem(Base, LocalizationBaseMixin):
    __tablename__ = 'course_lessonlocalizationitem'

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    lesson = relationship("Lesson", back_populates="lesson_localization")
    image = Column(String)  # For storing image path/URL
