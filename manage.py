import typer
from sqlmodel import select, Session

from db.database import create_database_and_tables, engine
from db.models.users import User
from hash import hash

app = typer.Typer()

@app.command("createsuperuser")
def createsuperuser(username: str, password: str):
    with Session(engine) as session:
        user = session.exec(select(User).filter(User.username==username)).first()

        if user:
            typer.echo("This username is already occupied.")
            return
        
        new_superuser = User(username=username, password_hash=hash(password), superuser=True)
        session.add(new_superuser)
        session.commit()

        typer.echo("Successfully added superuser.")

@app.command()
def ping():
    typer.echo("pong")

if __name__ == "__main__":
    create_database_and_tables()
    app()