from sqlalchemy import Column, Text, DateTime, Integer, ForeignKey, Boolean
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship, backref

from app.database import Base


class User(Base):
    __searchable__ = ['alias', 'about_me']

    id = Column(Integer, primary_key=True)
    alias = Column(Text, index=True, unique=True)
    email = Column(Text, unique=True)
    avatar = Column(Text, unique=True)
    first_name = Column(Text)
    last_name = Column(Text)
    password_hash = Column(Text)
    about_me = Column(Text)
    last_seen = Column(DateTime)
    images = relationship("Image", back_populates='artist')
    links = relationship("Link", back_populates='user')

    def __json__(self):
        return list(self.__mapper__.columns.keys())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @classmethod
    def get(cls, id):
        try:
            return cls.query.get(id)
        except KeyError:
            return None

    @staticmethod
    def make_unique_display_name(nickname):
        if User.query.filter_by(alias=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(alias=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    def upload_image(self, image):
        if not self.tracked(image, self.images):
            self.images.append(image)
            return self

    def remove_image(self, image):
        if self.tracked(image, self.images):
            self.images.remove(image)
            return self

    def add_link(self, link):
        if not self.tracked(link, self.links):
            self.links.append(link)
            return self

    def remove_link(self, link):
        if self.tracked(link, self.links):
            self.links.remove(link)
            return self

    @staticmethod
    def tracked(obj, collection):
        return obj in collection
