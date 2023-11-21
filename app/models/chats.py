from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base import Base
from .base import CreateUpdateDate

if TYPE_CHECKING:
    from .category import Category  # noqa: F401
    from .user import User  # noqa: F401


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from db.base import Base


class Conversation(Base, CreateUpdateDate):
    __tablename__ = 'conversation'

    id = Column(Integer, primary_key=True, index=True)

    # Many-to-Many relationship with users
    participants = relationship('User', secondary='conversation_participant', back_populates='conversations')
    messages = relationship('Message', back_populates='conversation')


class ConversationParticipant(Base, CreateUpdateDate):
    __tablename__ = 'conversation_participant'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversation.id'), primary_key=True)


class Message(Base, CreateUpdateDate):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('user.id'))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation_id = Column(Integer, ForeignKey('conversation.id'))
    conversation = relationship('Conversation', back_populates='messages')
