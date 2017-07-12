from sqlalchemy import Column, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import generic_repr
from app.database import Base


@generic_repr
class User(Base):
    __searchable__ = ['nickname']

    id = Column(Integer, primary_key=True)
    nickname = Column(Text, index=True, unique=True)
    email = Column(Text, index=True, unique=True)
    about_me = Column(Text)
    last_seen = Column(DateTime)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

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

    # def avatar(self, size):
    #     return 'http://www.gravatar.com/avatar/{avatar}?d=mm&s={size}'.format(
    #         avatar=md5(self.email.encode('utf-8')).hexdigest(),
    #         size=size
    #     )

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    # def follow(self, user):
    #     if not self.is_following(user):
    #         self.followed.append(user)
    #         return self
    #
    # def unfollow(self, user):
    #     if self.is_following(user):
    #         self.followed.remove(user)
    #         return self
    #
    # def is_following(self, user):
    #     return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    #
    # def followed_posts(self):
    #     return (
    #         Post
    #         .query
    #         .join(
    #             followers, (followers.c.followed_id == Post.user_id)    # Join table, Join condition
    #         ).filter(
    #             followers.c.follower_id == self.id
    #         )
    #         .order_by(
    #             Post.timestamp.desc()
    #         )
    #     )
