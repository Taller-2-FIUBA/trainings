"""Defines table structure for each table in the database."""
from typing import List
from sqlalchemy import Boolean, Column, Float, ForeignKey, String, Integer
from sqlalchemy.orm import (
    Mapped, declarative_base, relationship, mapped_column
)

Base = declarative_base()


class TrainingType(Base):
    """Table structure for types of trainings."""

    __tablename__ = "training_type"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name = Column(String)  # cardio, arms, legs, etc.


class Difficulty(Base):
    """Table structure for difficulty of trainings."""

    __tablename__ = "difficulty"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name = Column(String)  # Easy, Medium or Hard


class Exercise(Base):
    """Table structure for exercises."""

    __tablename__ = "exercise"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("training_type.id"))
    name = Column(String)  # walk, run, bicep curls, jumping jacks, etc.
    unit = Column(String, nullable=True)  # Km, minute

    # Relationships
    type: Mapped["TrainingType"] = relationship(lazy="joined")


class TrainingExercise(Base):
    """Table structure for exercises within a training."""

    __tablename__ = "training_exercise"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    training_id: Mapped[int] = mapped_column(ForeignKey("training.id"))
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise.id"))
    count = Column(Integer)
    series = Column(Integer)

    # Relationships
    training: Mapped["Training"] = relationship(
        lazy="joined", back_populates="exercises"
    )
    exercise: Mapped["Exercise"] = relationship(lazy="joined")


class Training(Base):
    """Table structure for trainings."""

    __tablename__ = "training"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trainer_id = Column(String)
    tittle = Column(String)
    description = Column(String)
    type_id: Mapped[int] = mapped_column(ForeignKey("training_type.id"))
    difficulty_id: Mapped[int] = mapped_column(ForeignKey("difficulty.id"))
    media = Column(String)
    blocked: Mapped[bool] = mapped_column(default=False)

    # Relationships
    type: Mapped["TrainingType"] = relationship(lazy="joined")
    difficulty: Mapped["Difficulty"] = relationship(lazy="joined")
    exercises: Mapped[List["TrainingExercise"]] = relationship(
        lazy="joined", back_populates="training"
    )
    user: Mapped["UserTraining"] = relationship(
        lazy="joined", back_populates="training"
    )


class Users(Base):
    """Table structure for user."""

    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String)
    username = Column(String)
    name = Column(String)
    surname = Column(String)
    height = Column(Float)
    weight = Column(Integer)
    birth_date = Column(String)
    location = Column(String)
    registration_date = Column(String)
    is_athlete = Column(Boolean)
    is_blocked = Column(Boolean)

    # Relationships
    trainings: Mapped[List["UserTraining"]] = relationship(
        lazy="joined", back_populates="user"
    )


class UserTraining(Base):
    """Table structure for exercises within a training."""

    __tablename__ = "user_training"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )
    training_id: Mapped[int] = mapped_column(
        ForeignKey("training.id"), primary_key=True
    )

    # Relationships
    user: Mapped["Users"] = relationship(
        lazy="joined", back_populates="trainings"
    )
    training: Mapped["Training"] = relationship(lazy="joined")
