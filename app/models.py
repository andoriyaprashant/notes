from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    notes = relationship("Note", back_populates="owner")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="notes")


class SharedNote(Base):
    __tablename__ = "shared_notes"

    id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey("notes.id"))
    shared_with_user_id = Column(Integer, ForeignKey("users.id"))


class NoteHistory(Base):
    __tablename__ = "note_history"

    id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey("notes.id"))

    old_title = Column(String)
    old_content = Column(Text)

    edited_at = Column(DateTime, default=datetime.utcnow)