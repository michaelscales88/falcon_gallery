from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import Timestamp, generic_repr
from sqlalchemy.ext.declarative import declared_attr
from app.database import Base


@generic_repr
class Link(Timestamp, Base):
    __searchable__ = ['link']

    id = Column(Integer, primary_key=True)
    link = Column(Text)
    link_type = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="links")

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
