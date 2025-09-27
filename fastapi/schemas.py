from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    title: str = Field(..., description="Название блюда", example="Борщ")
    cooking_time: int = Field(..., description="Время приготовления, мин", example=90)


class RecipeShortOut(RecipeBase):
    id: int = Field(..., description="ID рецепта", example=1)
    count_views: int = Field(..., description="Количество просмотров", example=42)


    class Config:
        from_attributes = True


class RecipeIn(RecipeBase):
    ingredients: str = Field(..., description="Ингредиенты (через запятую)",
                             example="свекла, картофель, капуста")
    description: str = Field(..., description="Пошаговое описание",
                             example="1. Нарезать овощи...\n2. Варить 40 минут...")


class RecipeOut(RecipeShortOut, RecipeIn):
    class Config:
        from_attributes = True
