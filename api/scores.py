from typing import Annotated, Optional, Sequence
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import col, select
from api.sessions import authorize
from db import Database
from db.models import GameDifficulty, ScoreSubmission
import db

router = APIRouter(tags=["scores"])


@router.get("/scores")
async def list_scores(
    game_category: str,
    game_difficulty: GameDifficulty,
    db: Database = Depends(db.use),
    user_id: str = Depends(authorize),
    before: Annotated[Optional[int], "The score ID to start descending from."] = None,
) -> Sequence[ScoreSubmission]:
    scores_query = await db.exec(
        select(ScoreSubmission)
        .where(
            ScoreSubmission.user_id == user_id
            and ScoreSubmission.game_category == game_category
            and ScoreSubmission.game_difficulty == game_difficulty
            and (ScoreSubmission.id < before if before else True)
        )
        .order_by(col(ScoreSubmission.id).desc())
    )
    scores = scores_query.all()
    return scores


class AverageScoreResponse(BaseModel):
    average_score: float
    total_scores: int


@router.get("/scores/average")
async def average_score(
    game_category: str,
    game_difficulty: GameDifficulty,
    db: Database = Depends(db.use),
    user_id: str = Depends(authorize),
) -> AverageScoreResponse:
    """
    Get the average score for a game.
    """
    # TODO: figure out why SQLModel is scared of
    # func.sum(ScoreSubmission.score).
    all_scores_query = await db.exec(
        select(ScoreSubmission.score).where(
            ScoreSubmission.user_id == user_id
            and ScoreSubmission.game_category == game_category
            and ScoreSubmission.game_difficulty == game_difficulty
        )
    )
    all_scores = all_scores_query.all()
    average_score = 0
    if len(all_scores) > 0:
        sum_scores = sum(all_scores)
        average_score = sum_scores / len(all_scores)
    return AverageScoreResponse(
        total_scores=len(all_scores),
        average_score=average_score,
    )


class SubmitScoreRequest(BaseModel):
    game_category: str
    game_difficulty: GameDifficulty
    score: float
    time_taken: Annotated[float, "Time taken in seconds."]
    revealed_answer: bool


@router.post("/scores")
async def submit_score(
    req: SubmitScoreRequest,
    db: Database = Depends(db.use),
    user_id: str = Depends(authorize),
) -> ScoreSubmission:
    async with db.begin_nested():
        score = ScoreSubmission(
            game_category=req.game_category,
            game_difficulty=req.game_difficulty,
            user_id=user_id,
            score=req.score,
            time_taken=req.time_taken,
            revealed_answer=req.revealed_answer,
        )
        db.add(score)
    await db.refresh(score)
    return score
