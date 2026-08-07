from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import relationship

from app.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id")
    )

    round = Column(String)
    date = Column(Date)
    time = Column(Time)
    interviewer = Column(String)
    notes = Column(String)
    result = Column(String)

    application = relationship(
        "Application",
        back_populates="interviews"
    )
