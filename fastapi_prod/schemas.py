from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field

JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JsonDict = Dict[str, JsonValue]


class RecipeBase(BaseModel):
    title: str = Field(..., description="Название блюда")
    cooking_time: int = Field(..., description="Время приготовления, мин")


class RecipeShortOut(RecipeBase):
    id: int = Field(..., description="ID рецепта")
    count_views: int = Field(..., description="Количество просмотров")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Борщ",
                "cooking_time": 90,
                "count_views": 42,
            }
        },
    }


class RecipeIn(RecipeBase):
    ingredients: str = Field(...,
                             description="Ингредиенты (через запятую)")
    description: str = Field(..., description="Пошаговое описание")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "title": "Борщ",
                "cooking_time": 90,
                "ingredients": "свекла, картофель, капуста",
                "description": "1. Нарезать овощи..."
                               "\n2. Варить 40 минут...",
            }
        },
    }


class RecipeOut(RecipeShortOut, RecipeIn):
    model_config = {"from_attributes": True}
