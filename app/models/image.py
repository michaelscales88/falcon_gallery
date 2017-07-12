from sqlalchemy import Column, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import Timestamp, generic_repr

from app.database import Base


@generic_repr
class Image(Timestamp, Base):
    __searchable__ = ['name', 'about']

    id = Column(Integer, primary_key=True)
    file_name = Column(Text, unique=True)
    name = Column(Text, index=True)
    about = Column(Text)
    last_seen = Column(DateTime)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def get(cls, file_name):
        try:
            return cls.query.get(file_name)
        except KeyError:
            return None

    # def thumbnail(self, size):
    #     return 'http://www.gravatar.com/avatar/{avatar}?d=mm&s={size}'.format(
    #         avatar=md5(self.email.encode('utf-8')).hexdigest(),
    #         size=size
    #     )
