from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Album(Base):
    __tablename__ = 'image_album'


class ImageAlbum(Base):
    __tablename__ = 'image_album'
    left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
    child = relationship("Child")


class ArtistAlbum(Base):
    __tablename__ = 'artist_album'
    left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
    child = relationship("Child")
