import db as database
from db import Database
from db.models import *
from sqlmodel import select, update


async def get_pickled_data_for_user_game(
    game_category: str,
    game_difficulty: GameDifficulty,
    user_id: str,
    db: Database,
) -> bytes | None:
    """
    This function returns the pickled data for the user's AI model for the given game.
    If the user does not have a model for the given game, None is returned.
    """
    db_model = await db.get(UserAIModel, (game_category, game_difficulty, user_id))
    return db_model.model if db_model is not None else None


async def save_pickled_data_for_user_game(
    game_category: str,
    game_difficulty: GameDifficulty,
    user_id: str,
    model: bytes,
    db: Database,
) -> None:
    """
    This function saves the pickled data for the user's AI model for the given game.
    If the user already has a model for the given game, it is overwritten.
    """
    async with db.begin_nested():
        db_model = await db.get(UserAIModel, (game_category, game_difficulty, user_id))
        if db_model is None:
            db_model = UserAIModel(
                game_category=game_category,
                game_difficulty=game_difficulty,
                user_id=user_id,
                model=model,
            )
        else:
            db_model.model = model
        db.add(db_model)


if __name__ == "__main__":
    import asyncio

    database.set_sqlite_path(":memory:")

    async def test():
        await database.init_db()

        async with database.get() as db:
            async with db.begin_nested():
                user = User()
                db.add(user)
            await db.refresh(user)

            pickle = await get_pickled_data_for_user_game(
                game_category="chess",
                game_difficulty=GameDifficulty.BEGINNER,
                user_id=user.id,
                db=db,
            )
            assert pickle is None

            await save_pickled_data_for_user_game(
                game_category="chess",
                game_difficulty=GameDifficulty.BEGINNER,
                user_id=user.id,
                model=b"test",
                db=db,
            )

            pickle = await get_pickled_data_for_user_game(
                game_category="chess",
                game_difficulty=GameDifficulty.BEGINNER,
                user_id=user.id,
                db=db,
            )
            assert pickle == b"test"

    asyncio.run(test())
    print("All tests passed!")
