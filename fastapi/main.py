from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from contextlib import asynccontextmanager
from database import engine, get_session
from models import Base, Recipe
from schemas import RecipeIn, RecipeOut, RecipeShortOut


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan, title="API Кулинарной книги", version="1.0")

@app.get(
    "/recipes",
    response_model=List[RecipeShortOut],
    summary="Список рецептов",
    description="Возвращает краткую информацию о рецептах, отсортированную сначала по популярности (count_views ↓), затем по времени приготовления (↑)."
)
async def list_recipes(session: AsyncSession = Depends(get_session)) -> List[Recipe]:
    stmt = select(Recipe).order_by(desc(Recipe.count_views), Recipe.cooking_time)
    result = await session.execute(stmt)
    return list(result.scalars().all())


@app.get(
    "/recipes/{recipe_id}",
    response_model=RecipeOut,
    summary="Детальный рецепт",
    description="Возвращает полную информацию о рецепте и увеличивает счётчик просмотров на 1."
)
async def get_recipe(
    recipe_id: int,
    session: AsyncSession = Depends(get_session)
) -> Recipe:
    result = await session.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    recipe.count_views += 1
    await session.commit()
    await session.refresh(recipe)
    return recipe


@app.post(
    "/recipes",
    response_model=RecipeOut,
    summary="Создать рецепт",
    description="Создаёт новый рецепт с ингредиентами и описанием. Возвращает всю информацию о созданном рецепте."
)


async def create_recipe(
    recipe_in: RecipeIn,
    session: AsyncSession = Depends(get_session)
) -> Recipe:
    new = Recipe(**recipe_in.model_dump())
    session.add(new)
    await session.commit()
    await session.refresh(new)
    return new
