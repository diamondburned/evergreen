## Import Libraries
# Base
import pandas as pd
import numpy as np
import json
# Preprocessing
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
# Pickle
import pickle


# Beginner algorithms user log

# Mock beginner prob-stats, data structures user logs
user_game2 = {
    "probability-statistics": {
        "score": 8.0,
        "avgscore": 8.0,
        "currlevel": "beginner",
        "timespent": 8,
        "revealanswer": 0
    }
}

user_game3 = {
    "data-structures": {
        "score": 4.0,
        "avgscore": 4.0,
        "currlevel": "beginner",
        "timespent": 2,
        "revealanswer": 1
    }
}


# Predict function
def predict_class(game):

    # Preprocessing
    def preprocess(user_game):
        df = pd.DataFrame(user_game)
        df = df.transpose()
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'user_id'}, inplace=True)
        return df

    df = preprocess(game)
    print(df.head)
    
    # drop user_id
    df = df.drop(columns=['user_id'])

    # Fill NaN
    df.iloc[:, [0, 1, 3, 4]] = df.iloc[:, [0, 1, 3, 4]].fillna(0)

    # Label Encode Manually
    currlevel_mapping = {'beginner': 1, 'intermediate': 2, 'advanced': 0}
    df['currlevel'] = df['currlevel'].map(currlevel_mapping)

    revealanswer_mapping = {0: 0, 1: 1, 2: 2, 3: 3}
    df['revealanswer'] = df['revealanswer'].map(revealanswer_mapping)

    # Min-Max Normalization
    df['score'] = df['score'] / 10
    df['avgscore'] = df['avgscore'] / 10
    df['currlevel'] = df['currlevel'] / 2
    df['timespent'] = df['timespent'] / 9.9
    df['revealanswer'] = df['revealanswer'] / 3
    print(df)

    X_test = df

    # Load model
    rf_model = pickle.load(open("ai/model/random_forest.pkl", "rb"))

    # Prediction
    pred = rf_model.predict(X_test)

    # Add prediction column
    X_test['progresstolevel'] = pred
    print(X_test)

    return pred



predict_class(user_game2)
predict_class(user_game3)