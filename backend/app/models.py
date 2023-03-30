from sqlalchemy import Column, Integer, String, ForeignKey 
from ORM import Base

class users(Base):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

class links(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


