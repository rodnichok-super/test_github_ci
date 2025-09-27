from sqlalchemy import Column, Integer, String, Text
from database import Base


class Recipe(Base):
    __tablename__ = "recipe"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    count_views = Column(Integer, nullable=False, default="0")
    cooking_time = Column(Integer, nullable=False)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

