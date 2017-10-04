from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Link(Base):
    __searchable__ = ['link']

    id = Column(Integer, primary_key=True)
    link = Column(Text)
    link_type = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="links")
