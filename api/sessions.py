from typing import AsyncGenerator
from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from db import Database
from db.models import *
from ai.models import *
from sqlmodel import select
from datetime import datetime, timedelta
import secrets
import hashlib
import hmac
import db


SESSION_EXPIRY = timedelta(days=7)
SESSION_RENEW_AFTER = timedelta(days=1)


async def authorize(
    creds: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Database = Depends(db.use),
) -> AsyncGenerator[str, None]:
    """
    This function asserts the authorization header and returns the user ID if
    the token is valid.
    """

    authorization = creds.credentials
    now = datetime.now()

    session_query = await db.exec(
        select(Session).where(
            Session.token == authorization and Session.expires_at > now
        )
    )
    session = session_query.first()
    if session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # If the session is after the renew threshold, renew the session.
    # Don't always renew the session, as that would force a database write on
    # every request.
    if (session.expires_at - SESSION_EXPIRY) + SESSION_RENEW_AFTER < now:
        async with db.begin_nested():
            session.expires_at = datetime.now() + SESSION_EXPIRY
            db.add(session)
            await db.commit()

    assert session.user_id is not None
    yield session.user_id


router = APIRouter(tags=["sessions"])


class SessionResponse(BaseModel):
    token: str
    user_id: str
    expires_at: datetime
    is_anonymous: bool


@router.post("/sessions")
async def create_session(
    db: Database = Depends(db.use),
) -> SessionResponse:
    """
    Create a new session assigned to a new and anonymous user.
    The user may later choose to register and log in.
    """
    async with db.begin_nested():
        user = User(training_model=UserTrainingModel())
        db.add(user)

    await db.refresh(user)

    async with db.begin_nested():
        session = Session(user_id=user.id)
        db.add(session)

    await db.refresh(session)

    return SessionResponse(
        **session.model_dump(),
        is_anonymous=True,
    )


class RegisterSessionRequest(BaseModel):
    email: str
    password: str


@router.post("/sessions/register")
async def register_session(
    req: RegisterSessionRequest,
    db: Database = Depends(db.use),
    user_id: str = Depends(authorize),
) -> None:
    """
    Register a user with an email and password.
    The user must be anonymous to register.
    """
    user = await db.get_one(User, user_id)
    if not user.is_anonymous():
        raise HTTPException(status_code=400, detail="User already registered")

    user.email = req.email
    user.passhash = hash_password(req.password)
    db.add(user)


class LoginSessionRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(
    req: LoginSessionRequest,
    db: Database = Depends(db.use),
) -> SessionResponse:
    """
    Log in with an email and password.
    """
    user_query = await db.exec(select(User).where(User.email == req.email))
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # passhash cannot be None if email is not None
    assert user.passhash is not None

    if not verify_password(req.password, user.passhash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    async with db.begin_nested():
        session = Session(user_id=user.id)
        db.add(session)

    await db.refresh(session)

    return SessionResponse(
        **session.model_dump(),
        is_anonymous=False,
    )


def generate_token() -> str:
    """
    This function generates a random token.
    """
    return secrets.token_urlsafe(32)


def hash_password(password: str) -> str:
    """
    This function hashes a password.
    """
    salt = secrets.token_bytes(16)
    hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return f"{salt.hex()}${hash.hex()}"


def verify_password(password: str, shash: str) -> bool:
    """
    This function verifies a password.
    """
    ssalt, shash = shash.split("$")
    osalt = bytes.fromhex(ssalt)
    ohash = bytes.fromhex(shash)
    return hmac.compare_digest(
        ohash,
        hashlib.pbkdf2_hmac("sha256", password.encode(), osalt, 100000),
    )
