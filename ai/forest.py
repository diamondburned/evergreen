## Import Libraries
# Base
import pandas as pd
import numpy as np
import json
# Preprocessing
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
# Modeling
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestClassifier
# Performance
from sklearn.metrics import accuracy_score
# Pickle
import pickle

## Import jsons
with open('ai/mock/initial_mock_user_scores.json', 'r') as file:
    initial = json.load(file)
with open('ai/mock/secondary_mock_user_scores.json', 'r') as file:
    secondary = json.load(file)
with open('ai/mock/seasoned_mock_user_scores.json', 'r') as file:
    seasoned = json.load(file)

## Preprocessing & Feature Engineering
# Initial
initial_df = pd.DataFrame(initial)
initial_df = initial_df.transpose()
initial_df.reset_index(inplace=True)
initial_df.rename(columns={'index': 'user_id'}, inplace=True)

initial_df_probability_statistic = initial_df.iloc[:, 0:2]
initial_df_data_structures = initial_df.iloc[:, [0, 2]]
initial_df_object_oriented_programming = initial_df.iloc[:, [0, 3]]
initial_df_algorithms = initial_df.iloc[:, [0, 4]]
initial_df_dynamic_programming = initial_df.iloc[:, [0, 5]]
initial_df_machine_learning = initial_df.iloc[:, [0, 6]]

def initial_determine_progress(row):
    beginner_tally, intermediate_tally = 0, 0

    for domains in row:
        if isinstance(domains, dict) and 'score' in domains:
            # automatic 'beginner' logic
            if pd.isnull(domains['score']):
                return 'beginner'

            # benchmark + game behavior logic
            if domains['score'] is not None:
                # score-based
                if domains['score'] >= 8.0:
                    intermediate_tally += 1
                else:
                    beginner_tally += 1

                # timespent & revealanswer
                if 'timespent' in domains and 'revealanswer' in domains:
                    timespent_avg = 5.0 # subject to change
                    # case 1: long time & no answer revealed shows persistence
                    if domains['timespent'] >= timespent_avg and domains['revealanswer'] == 0:
                        intermediate_tally += 1
                    # case 2: long time & answer revealed shows having difficulty
                    elif domains['timespent'] >= timespent_avg and domains['revealanswer'] != 0:
                        beginner_tally += 1
                    # case 3: short time & no answer revaled shows ease
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] == 0:
                        intermediate_tally += 1
                    # case 4: short time & answer revealed shows giving up
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] != 0:
                        beginner_tally += 1
                
    # decision-making
    if intermediate_tally >= beginner_tally:
        return 'intermediate'
    else:
        return 'beginner'
    
initial_df_probability_statistic['progresstolevel'] = initial_df_probability_statistic.apply(initial_determine_progress, axis=1)
initial_df_data_structures['progresstolevel'] = initial_df_data_structures.apply(initial_determine_progress, axis=1)
initial_df_object_oriented_programming['progresstolevel'] = initial_df_object_oriented_programming.apply(initial_determine_progress, axis=1)
initial_df_algorithms['progresstolevel'] = initial_df_algorithms.apply(initial_determine_progress, axis=1)
initial_df_dynamic_programming['progresstolevel'] = initial_df_dynamic_programming.apply(initial_determine_progress, axis=1)
initial_df_machine_learning['progresstolevel'] = initial_df_machine_learning.apply(initial_determine_progress, axis=1)

# Secondary
secondary_df = pd.DataFrame(secondary)
secondary_df = secondary_df.transpose()
secondary_df.reset_index(inplace=True)
secondary_df.rename(columns={'index': 'user_id'}, inplace=True)

secondary_df_probability_statistic = secondary_df.iloc[:, 0:2]
secondary_df_data_structures = secondary_df.iloc[:, [0, 2]]
secondary_df_object_oriented_programming = secondary_df.iloc[:, [0, 3]]
secondary_df_algorithms = secondary_df.iloc[:, [0, 4]]
secondary_df_dynamic_programming = secondary_df.iloc[:, [0, 5]]
secondary_df_machine_learning = secondary_df.iloc[:, [0, 6]]

def secondary_determine_progress(row):
    beginner_tally, intermediate_tally, advanced_tally = 0, 0, 0

    for domains in row:
        if isinstance(domains, dict) and 'score' in domains:
            # benchmark + game behavior logic

            # beginner logic
            if domains['score'] is not None and domains['currlevel'] == 'beginner':
                # score-based
                if domains['score'] >= 8.0:
                    intermediate_tally += 1
                else:
                    beginner_tally += 1

                # timespent & revealanswer
                if 'timespent' in domains and 'revealanswer' in domains:
                    timespent_avg = 5.0 # subject to change
                    # case 1: long time & no answer revealed shows persistence
                    if domains['timespent'] >= timespent_avg and domains['revealanswer'] == 0:
                        intermediate_tally += 1
                    # case 2: long time & answer revealed shows having difficulty
                    elif domains['timespent'] >= timespent_avg and domains['revealanswer'] != 0:
                        beginner_tally += 1
                    # case 3: short time & no answer revaled shows ease
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] == 0:
                        intermediate_tally += 1
                    # case 4: short time & answer revealed shows giving up
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] != 0:
                        beginner_tally += 1

            # intermediate logic
            if domains['score'] is not None and domains['currlevel'] == 'intermediate':
                # score-based
                if domains['score'] >= 8.0:
                    advanced_tally += 1
                else:
                    intermediate_tally += 1

                # timespent & revealanswer
                if 'timespent' in domains and 'revealanswer' in domains:
                    timespent_avg = 5.0 # subject to change
                    # case 1: long time & no answer revealed shows persistence
                    if domains['timespent'] >= timespent_avg and domains['revealanswer'] == 0:
                        advanced_tally += 1
                    # case 2: long time & answer revealed shows having difficulty
                    elif domains['timespent'] >= timespent_avg and domains['revealanswer'] != 0:
                        intermediate_tally += 1
                    # case 3: short time & no answer revaled shows ease
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] == 0:
                        advanced_tally += 1
                    # case 4: short time & answer revealed shows giving up
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] != 0:
                        intermediate_tally += 1
                
    # decision-making
    if advanced_tally > intermediate_tally:
        return 'advanced'
    elif intermediate_tally >= beginner_tally:
        return 'intermediate'
    else:
        return 'beginner'

secondary_df_probability_statistic['progresstolevel'] = secondary_df_probability_statistic.apply(secondary_determine_progress, axis=1)
secondary_df_data_structures['progresstolevel'] = secondary_df_data_structures.apply(secondary_determine_progress, axis=1)
secondary_df_object_oriented_programming['progresstolevel'] = secondary_df_object_oriented_programming.apply(secondary_determine_progress, axis=1)
secondary_df_algorithms['progresstolevel'] = secondary_df_algorithms.apply(secondary_determine_progress, axis=1)
secondary_df_dynamic_programming['progresstolevel'] = secondary_df_dynamic_programming.apply(secondary_determine_progress, axis=1)
secondary_df_machine_learning['progresstolevel'] = secondary_df_machine_learning.apply(secondary_determine_progress, axis=1)

# Seasoned
seasoned_df = pd.DataFrame(seasoned)
seasoned_df = seasoned_df.transpose()
seasoned_df.reset_index(inplace=True)
seasoned_df.rename(columns={'index': 'user_id'}, inplace=True)

seasoned_df_probability_statistic = seasoned_df.iloc[:, 0:2]
seasoned_df_data_structures = seasoned_df.iloc[:, [0, 2]]
seasoned_df_object_oriented_programming = seasoned_df.iloc[:, [0, 3]]
seasoned_df_algorithms = seasoned_df.iloc[:, [0, 4]]
seasoned_df_dynamic_programming = seasoned_df.iloc[:, [0, 5]]
seasoned_df_machine_learning = seasoned_df.iloc[:, [0, 6]]

def seasoned_determine_progress(row):
    beginner_tally, intermediate_tally, advanced_tally, done_tally = 0, 0, 0, 0

    for domains in row:
        if isinstance(domains, dict) and 'score' in domains:
            # benchmark + game behavior logic

            # beginner logic
            if domains['score'] is not None and domains['currlevel'] == 'beginner':
                # score-based
                if domains['score'] >= 8.0:
                    intermediate_tally += 1
                else:
                    beginner_tally += 1

                # timespent & revealanswer
                if 'timespent' in domains and 'revealanswer' in domains:
                    timespent_avg = 5.0 # subject to change
                    # case 1: long time & no answer revealed shows persistence
                    if domains['timespent'] >= timespent_avg and domains['revealanswer'] == 0:
                        intermediate_tally += 1
                    # case 2: long time & answer revealed shows having difficulty
                    elif domains['timespent'] >= timespent_avg and domains['revealanswer'] != 0:
                        beginner_tally += 1
                    # case 3: short time & no answer revaled shows ease
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] == 0:
                        intermediate_tally += 1
                    # case 4: short time & answer revealed shows giving up
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] != 0:
                        beginner_tally += 1

            # intermediate logic
            if domains['score'] is not None and domains['currlevel'] == 'intermediate':
                # score-based
                if domains['score'] >= 8.0:
                    advanced_tally += 1
                else:
                    intermediate_tally += 1

                # timespent & revealanswer
                if 'timespent' in domains and 'revealanswer' in domains:
                    timespent_avg = 5.0 # subject to change
                    # case 1: long time & no answer revealed shows persistence
                    if domains['timespent'] >= timespent_avg and domains['revealanswer'] == 0:
                        advanced_tally += 1
                    # case 2: long time & answer revealed shows having difficulty
                    elif domains['timespent'] >= timespent_avg and domains['revealanswer'] != 0:
                        intermediate_tally += 1
                    # case 3: short time & no answer revaled shows ease
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] == 0:
                        advanced_tally += 1
                    # case 4: short time & answer revealed shows giving up
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] != 0:
                        intermediate_tally += 1

            # advanced logic
            if domains['score'] is not None and domains['currlevel'] == 'advanced':
                # score-based
                if domains['score'] >= 8.0:
                    done_tally += 1
                else:
                    advanced_tally += 1

                # timespent & revealanswer
                if 'timespent' in domains and 'revealanswer' in domains:
                    timespent_avg = 5.0 # subject to change
                    # case 1: long time & no answer revealed shows persistence
                    if domains['timespent'] >= timespent_avg and domains['revealanswer'] < 2:
                        done_tally += 1
                    # case 2: long time & answer revealed shows having difficulty
                    elif domains['timespent'] >= timespent_avg and domains['revealanswer'] >= 2:
                        advanced_tally += 1
                    # case 3: short time & no answer revaled shows ease
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] < 2:
                        done_tally += 1
                    # case 4: short time & answer revealed shows giving up
                    elif domains['timespent'] < timespent_avg and domains['revealanswer'] >= 2:
                        advanced_tally += 1
                
    # decision-making
    if done_tally > advanced_tally:
        return 'done'
    elif advanced_tally > intermediate_tally:
        return 'advanced'
    elif intermediate_tally >= beginner_tally:
        return 'intermediate'
    else:
        return 'beginner'

seasoned_df_probability_statistic['progresstolevel'] = seasoned_df_probability_statistic.apply(seasoned_determine_progress, axis=1)
seasoned_df_data_structures['progresstolevel'] = seasoned_df_data_structures.apply(seasoned_determine_progress, axis=1)
seasoned_df_object_oriented_programming['progresstolevel'] = seasoned_df_object_oriented_programming.apply(seasoned_determine_progress, axis=1)
seasoned_df_algorithms['progresstolevel'] = seasoned_df_algorithms.apply(seasoned_determine_progress, axis=1)
seasoned_df_dynamic_programming['progresstolevel'] = seasoned_df_dynamic_programming.apply(seasoned_determine_progress, axis=1)
seasoned_df_machine_learning['progresstolevel'] = seasoned_df_machine_learning.apply(seasoned_determine_progress, axis=1)

# Domain concatenation & restructure df
probability_statistics_df_final = pd.concat([
    initial_df_probability_statistic, 
    secondary_df_probability_statistic, 
    seasoned_df_probability_statistic
], ignore_index=True)

nested_cols = ['score', 'avgscore', 'currlevel', 'timespent', 'revealanswer']
for col in nested_cols:
    probability_statistics_df_final[col] = probability_statistics_df_final['probability_statistics'].apply(lambda x: x.get(col) if isinstance(x, dict) else None)

# drop user_id, domain
probability_statistics_df_final = probability_statistics_df_final.drop(columns=['probability_statistics', 'user_id'])

data_structures_df_final = pd.concat([
    initial_df_data_structures,
    secondary_df_data_structures,
    seasoned_df_data_structures
], ignore_index=True)

for col in nested_cols:
    data_structures_df_final[col] = data_structures_df_final['data_structures'].apply(lambda x: x.get(col) if isinstance(x, dict) else None)

# drop user_id, domain
data_structures_df_final = data_structures_df_final.drop(columns=['data_structures', 'user_id'])

object_oriented_programming_df_final = pd.concat([
    initial_df_object_oriented_programming,
    secondary_df_object_oriented_programming,
    seasoned_df_object_oriented_programming
], ignore_index=True)

for col in nested_cols:
    object_oriented_programming_df_final[col] = object_oriented_programming_df_final['object_oriented_programming'].apply(lambda x: x.get(col) if isinstance(x, dict) else None)

# drop user_id, domain
object_oriented_programming_df_final = object_oriented_programming_df_final.drop(columns=['object_oriented_programming', 'user_id'])

algorithms_df_final = pd.concat([
    initial_df_algorithms,
    secondary_df_algorithms,
    seasoned_df_algorithms
], ignore_index=True)

for col in nested_cols:
    algorithms_df_final[col] = algorithms_df_final['algorithms'].apply(lambda x: x.get(col) if isinstance(x, dict) else None)

# drop user_id, domain
algorithms_df_final = algorithms_df_final.drop(columns=['algorithms', 'user_id'])

dynamic_programming_df_final = pd.concat([
    initial_df_dynamic_programming,
    secondary_df_dynamic_programming,
    seasoned_df_dynamic_programming
], ignore_index=True)

for col in nested_cols:
    dynamic_programming_df_final[col] = dynamic_programming_df_final['dynamic_programming'].apply(lambda x: x.get(col) if isinstance(x, dict) else None)

# drop user_id, domain
dynamic_programming_df_final = dynamic_programming_df_final.drop(columns=['dynamic_programming', 'user_id'])

machine_learning_df_final = pd.concat([
    initial_df_machine_learning,
    secondary_df_machine_learning,
    seasoned_df_machine_learning
], ignore_index=True)

for col in nested_cols:
    machine_learning_df_final[col] = machine_learning_df_final['machine_learning'].apply(lambda x: x.get(col) if isinstance(x, dict) else None)

# drop user_id, domain
machine_learning_df_final = machine_learning_df_final.drop(columns=['machine_learning', 'user_id'])

# Fill NaN
probability_statistics_df_final.iloc[:, [1, 2, 4, 5]] = probability_statistics_df_final.iloc[:, [1, 2, 4, 5]].fillna(0)
data_structures_df_final.iloc[:, [1, 2, 4, 5]] = data_structures_df_final.iloc[:, [1, 2, 4, 5]].fillna(0)
object_oriented_programming_df_final.iloc[:, [1, 2, 4, 5]] = object_oriented_programming_df_final.iloc[:, [1, 2, 4, 5]].fillna(0)
algorithms_df_final.iloc[:, [1, 2, 4, 5]] = algorithms_df_final.iloc[:, [1, 2, 4, 5]].fillna(0)
dynamic_programming_df_final.iloc[:, [1, 2, 4, 5]] = dynamic_programming_df_final.iloc[:, [1, 2, 4, 5]].fillna(0)
machine_learning_df_final.iloc[:, [1, 2, 4, 5]] = machine_learning_df_final.iloc[:, [1, 2, 4, 5]].fillna(0)

# Label Encode
label_encoder = LabelEncoder()
probability_statistics_df_final['currlevel'] = label_encoder.fit_transform(probability_statistics_df_final['currlevel'])
data_structures_df_final['currlevel'] = label_encoder.fit_transform(data_structures_df_final['currlevel'])
object_oriented_programming_df_final['currlevel'] = label_encoder.fit_transform(object_oriented_programming_df_final['currlevel'])
algorithms_df_final['currlevel'] = label_encoder.fit_transform(algorithms_df_final['currlevel'])
dynamic_programming_df_final['currlevel'] = label_encoder.fit_transform(dynamic_programming_df_final['currlevel'])
machine_learning_df_final['currlevel'] = label_encoder.fit_transform(machine_learning_df_final['currlevel'])

probability_statistics_df_final['revealanswer'] = label_encoder.fit_transform(probability_statistics_df_final['revealanswer'])
data_structures_df_final['revealanswer'] = label_encoder.fit_transform(data_structures_df_final['revealanswer'])
object_oriented_programming_df_final['revealanswer'] = label_encoder.fit_transform(object_oriented_programming_df_final['revealanswer'])
algorithms_df_final['revealanswer'] = label_encoder.fit_transform(algorithms_df_final['revealanswer'])
dynamic_programming_df_final['revealanswer'] = label_encoder.fit_transform(dynamic_programming_df_final['revealanswer'])
machine_learning_df_final['revealanswer'] = label_encoder.fit_transform(machine_learning_df_final['revealanswer'])

# probability_statistics_df_final['progresstolevel'] = label_encoder.fit_transform(probability_statistics_df_final['progresstolevel'])
# data_structures_df_final['progresstolevel'] = label_encoder.fit_transform(data_structures_df_final['progresstolevel'])
# object_oriented_programming_df_final['progresstolevel'] = label_encoder.fit_transform(object_oriented_programming_df_final['progresstolevel'])
# algorithms_df_final['progresstolevel'] = label_encoder.fit_transform(algorithms_df_final['progresstolevel'])
# dynamic_programming_df_final['progresstolevel'] = label_encoder.fit_transform(dynamic_programming_df_final['progresstolevel'])
# machine_learning_df_final['progresstolevel'] = label_encoder.fit_transform(machine_learning_df_final['progresstolevel'])

# Normalize
scaler = MinMaxScaler()
probability_statistics_df_final.iloc[:, 1:] = scaler.fit_transform(probability_statistics_df_final.iloc[:, 1:])
data_structures_df_final.iloc[:, 1:] = scaler.fit_transform(data_structures_df_final.iloc[:, 1:])
object_oriented_programming_df_final.iloc[:, 1:] = scaler.fit_transform(object_oriented_programming_df_final.iloc[:, 1:])
algorithms_df_final.iloc[:, 1:] = scaler.fit_transform(algorithms_df_final.iloc[:, 1:])
dynamic_programming_df_final.iloc[:, 1:] = scaler.fit_transform(dynamic_programming_df_final.iloc[:, 1:])
machine_learning_df_final.iloc[:, 1:] = scaler.fit_transform(machine_learning_df_final.iloc[:, 1:])

## Classification Modeling
# X, y objects
ps_X = probability_statistics_df_final.iloc[:, 1:]
ds_X = data_structures_df_final.iloc[:, 1:]
oop_X = object_oriented_programming_df_final.iloc[:, 1:]
a_X = algorithms_df_final.iloc[:, 1:]
dp_X = dynamic_programming_df_final.iloc[:, 1:]
ml_X = machine_learning_df_final.iloc[:, 1:]

ps_y = (probability_statistics_df_final.iloc[:, 0])
ds_y = data_structures_df_final.iloc[:, 0]
oop_y = object_oriented_programming_df_final.iloc[:, 0]
a_y = algorithms_df_final.iloc[:, 0]
dp_y = dynamic_programming_df_final.iloc[:, 0]
ml_y = machine_learning_df_final.iloc[:, 0]

# K-fold cross-validation
def random_forest_cv(X, y, max_depth=20, min_samples_split=2, min_samples_leaf=2, n_estimators=100):
    n_splits, avgacc = 10, 0
    kfold = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    accuracies = []
    model = None

    for train_index, test_index in kfold.split(X):
        X_train_fold, X_test_fold = X.iloc[train_index], X.iloc[test_index]
        y_train_fold, y_test_fold = y.iloc[train_index], y.iloc[test_index]

        # Initialize the Random Forest model
        model = RandomForestClassifier(
            random_state=42,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            n_estimators=n_estimators
        )
        # Fit the model
        model.fit(X_train_fold, y_train_fold)
        # Predict on the test fold
        predictions = model.predict(X_test_fold)
        # Calculate accuracy
        accuracy = accuracy_score(y_test_fold, predictions)
        accuracies.append(accuracy)
    
    # Calculate the average accuracy across all folds
    avgacc = np.mean(accuracies)
    
    return avgacc, model

domain_Xy = [
    (ps_X, ps_y),
    (ds_X, ds_y),
    (oop_X, oop_y),
    (a_X, a_y),
    (dp_X, dp_y),
    (ml_X, ml_y)
]

## Evaluation
# Per domain
for i, (X, y) in enumerate(domain_Xy):
    avgacc = random_forest_cv(X, y)
    print(f"Domain {i+1}: Average accuracy is {avgacc}")

# Fully
X_df_final = pd.concat([
    ps_X, ds_X, oop_X, a_X, dp_X, ml_X
], ignore_index=True)

y_df_final = pd.concat([
    ps_y, ds_y, oop_y, a_y, dp_y, ml_y
], ignore_index=True)

Xy = [
    (X_df_final, y_df_final)
]

final_model = None

for i, (X, y) in enumerate(Xy):
    avgacc, model = random_forest_cv(X, y)
    print(f"Domain {i+1}: Average accuracy is {avgacc}")
    final_model = model

## Pickle
if final_model is not None:
    pickle.dump(final_model, open('ai/model/random_forest.pkl', 'wb'))
                