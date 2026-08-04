from sqlalchemy import Column, Integer, String

from app.database import Base


class Application(Base):

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String, nullable=False)

    role = Column(String, nullable=False)

    salary = Column(Integer, nullable=False)

    status = Column(String, nullable=False)