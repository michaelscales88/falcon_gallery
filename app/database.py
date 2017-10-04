from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app import app
from .model import Base

db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db_engine))

Base.query = db_session.query_property()


def init_db():

    # Import models to include in the Base
    from app.models import Image
    from app.models import Link
    from app.models import User

    Base.metadata.create_all(bind=db_engine)

# Create metadata for the application
init_db()
