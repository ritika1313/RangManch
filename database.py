from sqlmodel import SQLModel, Session, create_engine
# SQLModel -> used to create/manage database tables
# Session -> used to interact with the database
# create_engine -> used to connection/engine for the database

DATABASE_URL = "sqlite:///rangmanch.db"

engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    """Create all tables defined by SQLModel Class"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Depedency that provides a database session per request"""
    with Session(engine) as session:
        yield session
