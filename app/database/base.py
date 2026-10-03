from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
    # where Base is the parent class for all your db models
    # all db tables will be based on this
    
    