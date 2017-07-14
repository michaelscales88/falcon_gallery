from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from app import app
import os


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def rebase():
    # Import models to include in the Base
    from app.models import User
    from app.models import Image
    from app.models import ImageModel
    Base.metadata.create_all(bind=engine)


def init_db():
    # Import models to include in the Base
    from app.models import User
    from app.models import Image
    from app.models import ImageModel
    Base.metadata.create_all(bind=engine)

    # Get images currently in gallery
    existing_imgs = os.listdir(app.config['GALLERY_ROOT_DIR'])
    session = db_session()
    # Reflect images into database
    for img in existing_imgs:
        if Image.allowed_extension(img, extensions=app.config['ALLOWED_EXTENSIONS']):
            image = ImageModel(file_name=img)
            session.add(image)
    session.commit()
    db_session.remove()
