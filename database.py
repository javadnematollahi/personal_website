from sqlmodel import SQLModel, Session, create_engine, select, Field
from pydantic import BaseModel

class User(SQLModel, table=True):
    __table_args__ = {'extend_existing': True} 
    id: int = Field(default=None, primary_key=True)
    username: str = Field()
    password: str = Field()



engine = create_engine("sqlite:///./database.db", echo=True)
# engine = create_engine("postgresql://root:BdrDaRdnBGd5XMM96SHKA1z4@personalwebsiteusers:5432/postgres")
SQLModel.metadata.create_all(engine)

# pydantic model for request validation
class RegisterModel(BaseModel):
    username: str
    password: str
    confirmpassword: str

class LoginModel(BaseModel):
    username: str
    password: str


class Database:
    def __init__(self) -> None:
        pass

    def read_from_database(self, username, password):
        with Session(engine) as db:
            statement = select(User).where(User.username==username, User.password==password)
            result = db.exec(statement).first()
        return result
    
    def read_from_database_by_username(self, username):
        with Session(engine) as db:
            statement = select(User).where(User.username==username)
            result = db.exec(statement).first()
        return result
    
    def add_to_database(self, username, password):
        with Session(engine) as db:
            user = User(username=username, 
                             password=password)
            db.add(user)
            db.commit()

    def delete_from_database(self, username, password):
        with Session(engine) as db:
            statement = select(User).where(User.username==username, User.password==password)
            res = db.exec(statement).first()

            if res is None:
                print(f"There's no user as {username} in database")
            else:
                db.delete(res)
                db.commit()
