from sqlmodel import SQLModel, create_engine

sqlite_uri = "sqlite:///./blog.sqlite3"
engine = create_engine(sqlite_uri, connect_args={"check_same_thread": False})


def create_database_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
