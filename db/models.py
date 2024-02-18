import enum
from typing import Annotated, Optional
from pydantic import BaseModel
from sqlmodel import BLOB, SQLModel, Column, JSON
from sqlmodel import Field  # type: ignore
from datetime import datetime
from utils.id import generate_uuid, generate_token


class User(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    email: Optional[str] = Field(default=None, unique=True)
    passhash: Optional[str] = Field(default=None)
    avatar_hash: Optional[str] = Field(default=None, foreign_key="asset.hash")
    display_name: Optional[str] = Field(default=None)
    registered_at: Optional[datetime] = Field(default=None)

    def is_anonymous(self) -> bool:
        """
        This function returns True if the user is anonymous.
        A user is no longer anonymous if they choose to assign the user an email
        and password for later login.
        """
        return self.email is None


class GameDifficulty(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ScoreSubmission(SQLModel, table=True):
    class RoundInfo(BaseModel):
        score: float
        revealed_answer: bool

    id: int | None = Field(default=None, primary_key=True)
    game_category: str = Field()
    game_difficulty: GameDifficulty = Field()
    user_id: str = Field(foreign_key="user.id", index=True)
    rounds: Annotated[list[RoundInfo], "All the scores for each turn of the game"] = (
        Field(sa_column=Column(JSON))
    )
    average_score: Annotated[float, "The average score of all the turns"] = Field()
    time_taken: Annotated[float, "Time taken for the game in seconds."] = Field()
    submitted_at: datetime = Field(default_factory=datetime.utcnow)


class UserAIModel(SQLModel, table=True):
    game_category: str = Field(primary_key=True)
    game_difficulty: GameDifficulty = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", primary_key=True)
    model: bytes = Field(sa_column=Column(BLOB))


class Session(SQLModel, table=True):
    token: str = Field(primary_key=True, default_factory=generate_token)
    user_id: Optional[str] = Field(foreign_key="user.id")
    expires_at: datetime = Field(default_factory=datetime.utcnow)


class Asset(SQLModel, table=True):
    """
    An asset is any arbitrary binary data that can be stored in the database.
    It is identified by the base64-encoded SHA-256 hash of the data.
    Content types are supplied by the server.
    """

    hash: str = Field(primary_key=True)
    data: bytes
    created_at: datetime = Field(default_factory=datetime.utcnow)
    content_type: str
    alt: str | None = Field(default=None)
