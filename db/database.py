from sqlmodel import create_engine, SQLModel

sqlite_uri = "sqlite3:///./blog.sqlite3"
engine = create_engine(sqlite_uri, connect_args={"check_same_thread":False})

def create_database_and_tables() -> None:
    SQLModel.metadata.create_all(engine)