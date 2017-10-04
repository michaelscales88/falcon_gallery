from sqlalchemy import Column, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.file_system import ImageFile
from app.database import Base


class Image(ImageFile, Base):

    __searchable__ = ['display_name', 'about']

    id = Column(Integer, primary_key=True)
    file_name = Column(Text, unique=True)
    display_name = Column(Text, index=True)
    about = Column(Text)
    last_seen = Column(DateTime)
    views = Column(Integer, default=0)
    artist_id = Column(Integer, ForeignKey('user.id'))
    artist = relationship("User", back_populates="images")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name = self.filename
        self.display_name = self.filename.split('.')[0]

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
