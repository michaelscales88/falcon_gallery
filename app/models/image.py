from sqlalchemy import Column, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import Timestamp, generic_repr
from datetime import datetime
from app.database import Base


@generic_repr
class Image(Timestamp, Base):
    __searchable__ = ['display_name', 'about']

    id = Column(Integer, primary_key=True)
    file_name = Column(Text, unique=True)
    display_name = Column(Text, index=True)
    about = Column(Text)
    last_seen = Column(DateTime)
    views = Column(Integer, default=0)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def get(cls, file_name):
        try:
            return cls.query.get(file_name)
        except KeyError:
            return None

    def viewed(self):
        # Count views for ranking algorithm
        self.last_seen = datetime.utcnow()
        self.views += 1
