from datetime import datetime
from typing import Annotated, Optional, Sequence
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import col, select
from api.sessions import authorize
from db import Database
from db.models import GameDifficulty, ScoreSubmission
import db
import ai.predict

router = APIRouter(tags=["scores"])


@router.get("/scores")
async def list_scores(
    game_category: Optional[str] = None,
    game_difficulty: Optional[GameDifficulty] = None,
    db: Database = Depends(db.use),
    user_id: str = Depends(authorize),
    from_time: Annotated[
        Optional[datetime], "Time to start listing scores from."
    ] = None,
    to_time: Annotated[Optional[datetime], "Time to stop listing scores at."] = None,
) -> Sequence[ScoreSubmission]:
    scores_query = await db.exec(
        select(ScoreSubmission)
        .where(
            ScoreSubmission.user_id == user_id
            and (
                game_category is None or ScoreSubmission.game_category == game_category
            )
            and (
                game_difficulty is None
                or ScoreSubmission.game_difficulty == game_difficulty
            )
            and (from_time is None or ScoreSubmission.submitted_at >= from_time)
            and (to_time is None or ScoreSubmission.submitted_at <= to_time)
        )
        .order_by(col(ScoreSubmission.id).desc())
    )
    scores = scores_query.all()
    return scores


class SubmitScoreRequest(BaseModel):
    game_category: str
    game_difficulty: GameDifficulty
    rounds: list[ScoreSubmission.RoundInfo]
    average_score: float
    time_taken: Annotated[float, "Time taken in seconds."]


class SubmitScoreResponse(BaseModel):
    id: int
    game_category: str
    game_difficulty: GameDifficulty
    rounds: list[ScoreSubmission.RoundInfo]
    average_score: float
    time_taken: float
    submitted_at: datetime

    # TODO: add fields from the prediction model.


@router.post("/scores")
async def submit_score(
    req: SubmitScoreRequest,
    db: Database = Depends(db.use),
    user_id: str = Depends(authorize),
) -> SubmitScoreResponse:
    async with db.begin_nested():
        score = ScoreSubmission(
            game_category=req.game_category,
            game_difficulty=req.game_difficulty,
            user_id=user_id,
            rounds=req.rounds,
            average_score=req.average_score,
            time_taken=req.time_taken,
        )
        db.add(score)

    await db.refresh(score)
    assert score.id is not None

    return SubmitScoreResponse(
        id=score.id,
        game_category=score.game_category,
        game_difficulty=score.game_difficulty,
        rounds=score.rounds,
        average_score=score.average_score,
        time_taken=score.time_taken,
        submitted_at=score.submitted_at,
    )


recommendationPredictor = ai.predict.Predictor()


@router.get("/scores/recommend")
async def recommend_difficulty(
    game_category: str,
    db: Database = Depends(db.use),
    user_id: str = Depends(authorize),
) -> GameDifficulty:
    # For the sake of live demo:
    if game_category == "data-structures":
        stats = ai.predict.user_game2
        return recommendationPredictor.predict(stats)

    last_game_query = await db.exec(
        select(ScoreSubmission)
        .where(
            ScoreSubmission.user_id == user_id
            and ScoreSubmission.game_category == game_category
        )
        .order_by(col(ScoreSubmission.id).desc())
        .limit(1)
    )
    last_game = last_game_query.first()
    if last_game is None:
        return GameDifficulty.BEGINNER

    print(last_game.model_dump())

    revealed_answers = 0
    for r in last_game.rounds:
        print(last_game.model_dump(), r)
        if r.revealed_answer:
            revealed_answers += 1

    stats = ai.predict.GameStats(
        score=last_game.average_score,
        avgscore=last_game.average_score,
        currlevel=last_game.game_difficulty,
        timespent=round(last_game.time_taken),
        revealanswer=revealed_answers,
    )
    return recommendationPredictor.predict(stats)
