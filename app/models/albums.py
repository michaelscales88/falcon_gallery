from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Album(Base):
    __tablename__ = 'artist_album'
    left_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('image.id'), primary_key=True)
    artist = relationship("User", back_populates="images")  # Left id
    image = relationship("ImageModel", back_populates="artists")    # Right id
