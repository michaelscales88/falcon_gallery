from sqlalchemy import Column, Text, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import generic_repr
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import Base


@generic_repr
class User(Base):
    __searchable__ = ['display_name', 'about_me']

    id = Column(Integer, primary_key=True)
    display_name = Column(Text, index=True, unique=True)
    email = Column(Text, index=True, unique=True)
    password_hash = Column(Text)
    about_me = Column(Text)
    last_seen = Column(DateTime)
    images = relationship("Image", back_populates='artist')

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

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
        if User.query.filter_by(display_name=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(display_name=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    def upload(self, image):
        if not self.is_tracked(image):
            self.images.append(image)
            return self

    def remove(self, image):
        if self.is_tracked(image):
            self.images.remove(image)
            return self

    def is_tracked(self, image):
        return image in self.images

    # def avatar(self, size):
    #     return 'http://www.gravatar.com/avatar/{avatar}?d=mm&s={size}'.format(
    #         avatar=md5(self.email.encode('utf-8')).hexdigest(),
    #         size=size
    #     )