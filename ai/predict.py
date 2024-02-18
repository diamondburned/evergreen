## Import Libraries
# Base
from typing import Any
import pandas as pd
import numpy as np
import json
from pydantic import BaseModel

# Preprocessing
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Pickle
import pickle

from db.models import GameDifficulty


# Beginner algorithms user log


class GameStats(BaseModel):
    score: float
    avgscore: float
    currlevel: GameDifficulty
    timespent: int
    revealanswer: int


# Mock beginner prob-stats, data structures user logs
user_game2 = {
    "probability-statistics": GameStats(
        score=8.0,
        avgscore=8.0,
        currlevel=GameDifficulty.BEGINNER,
        timespent=8,
        revealanswer=0,
    ),
}

user_game3 = {
    "data-structures": GameStats(
        score=4.0,
        avgscore=4.0,
        currlevel=GameDifficulty.BEGINNER,
        timespent=2,
        revealanswer=1,
    ),
}


class Predictor:
    """
    Predictor implements an AI model to predict the next recommended game
    difficulty for the given user stats.
    """

    model: Any

    def __init__(self, modelPath="ai/model/random_forest.pkl"):
        self.model = pickle.load(open(modelPath, "rb"))

    def predict(self, stats: dict[str, GameStats]) -> GameDifficulty:
        df = pd.DataFrame({k: v.model_dump() for k, v in stats.items()})
        df = df.transpose()
        df.reset_index(inplace=True)
        df.rename(columns={"index": "user_id"}, inplace=True)

        # drop user_id
        df = df.drop(columns=["user_id"])

        # Fill NaN
        df.iloc[:, [0, 1, 3, 4]] = df.iloc[:, [0, 1, 3, 4]].fillna(0)

        # Label Encode Manually
        currlevel_mapping = {"beginner": 1, "intermediate": 2, "advanced": 0}
        df["currlevel"] = df["currlevel"].map(currlevel_mapping)

        revealanswer_mapping = {0: 0, 1: 1, 2: 2, 3: 3}
        df["revealanswer"] = df["revealanswer"].map(revealanswer_mapping)

        # Min-Max Normalization
        df["score"] = df["score"] / 10
        df["avgscore"] = df["avgscore"] / 10
        df["currlevel"] = df["currlevel"] / 2
        df["timespent"] = df["timespent"] / 9.9
        df["revealanswer"] = df["revealanswer"] / 3

        input = df

        # Prediction
        pred = self.model.predict(input)

        # Add prediction column
        input["progresstolevel"] = pred

        match pred[0]:
            case "beginner":
                return GameDifficulty.BEGINNER
            case "intermediate":
                return GameDifficulty.INTERMEDIATE
            case "advanced":
                return GameDifficulty.ADVANCED
            case _:
                raise ValueError("Invalid prediction")


if __name__ == "__main__":
    predictor = Predictor()
    predict_a = predictor.predict(user_game2)
    predict_b = predictor.predict(user_game3)

    print(predict_a)
    print(predict_b)

    assert predict_a == GameDifficulty.INTERMEDIATE
    assert predict_b == GameDifficulty.BEGINNER

    print("Done!")
