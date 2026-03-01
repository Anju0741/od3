from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import bcrypt

from database import engine
from auth import create_access_token, get_current_user
from models import SignupRequest, LoginRequest


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/signup")
def signup(data: SignupRequest):
    with engine.connect() as conn:
        user = conn.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": data.username},
        ).fetchone()

        if user:
            raise HTTPException(
                status_code=400,
                detail="Username already exists",
            )

        hashed_pw = bcrypt.hashpw(
            data.password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

        conn.execute(
            text(
                "INSERT INTO users (username, password_hash) "
                "VALUES (:username, :password)"
            ),
            {
                "username": data.username,
                "password": hashed_pw,
            },
        )

        conn.commit()

    return {"message": "Signup successful"}


@app.post("/login")
def login(data: LoginRequest):
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT password_hash FROM users "
                "WHERE username = :username"
            ),
            {"username": data.username},
        ).fetchone()

        if not result:
            raise HTTPException(
                status_code=400,
                detail="Invalid credentials",
            )

        stored_hash = result[0].encode("utf-8")

        if not bcrypt.checkpw(
            data.password.encode("utf-8"),
            stored_hash,
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid credentials",
            )

    token = create_access_token({"sub": data.username})

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@app.get("/me")
def read_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}


@app.get("/")
def root():
    return {"status": "backend running"}
