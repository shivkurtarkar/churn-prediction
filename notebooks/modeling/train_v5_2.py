##
import dask.dataframe as dd
import numpy as np
from IPython.display import display
from dask.distributed import Client, LocalCluster
import dask

import matplotlib.pyplot as plt
import seaborn as sns

##
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.svm import OneClassSVM
from sklearn.metrics import (confusion_matrix, precision_recall_curve, auc,
                             roc_curve, recall_score, classification_report, f1_score,
                             precision_recall_fscore_support)
import optuna
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss


import joblib

def main(client):
    print("client link:")
    print(client.dashboard_link)  # Clickable link to the dashboard


    ##
    # setup Variables for filepaths
    DATA_DIR="../../data"

    MEMBERS_FILE=f"{DATA_DIR}/members_v3.csv"
    TRANSACTION_FILE=f"{DATA_DIR}/transactions.csv"
    TRAIN_FILE=f"{DATA_DIR}/train.csv"
    USERLOG_FILE=f"{DATA_DIR}/user_logs.csv"
    SAMPLE_SUBMISSION_FILE=f"{DATA_DIR}/sample_submission_zero.csv"

    TRANSACTION_V2_FILE=f"{DATA_DIR}/transactions_v2.csv"
    TRAIN_V2_FILE=f"{DATA_DIR}/train_v2.csv"
    USER_LOGS_V2_FILE=f"{DATA_DIR}/user_logs_v2.csv"
    SAMPLE_SUBMISSION_V2_FILE=f"{DATA_DIR}/sample_submission_v2.csv"

    ##
    OUTPUT_DIR='../../output'

    MODEL_NAME="tunned_LGBMClassifier"

    ##
    print(f"DATA_DIR: {DATA_DIR}")
    print(f"TRANSACTION_FILE: {TRANSACTION_FILE}")
    print(f"USERLOG_FILE: {USERLOG_FILE}")
    print(f"TRAIN_FILE: {TRAIN_FILE}")
    print(f"SAMPLE_SUBMISSION_FILE: {SAMPLE_SUBMISSION_FILE}")
    print(f"MEMBERS_FILE: {MEMBERS_FILE}")
    print()
    print(f"TRANSACTION_V2_FILE: {TRANSACTION_V2_FILE}")
    print(f"USER_LOGS_V2_FILE: {USER_LOGS_V2_FILE}")
    print(f"TRAIN_V2_FILE: {TRAIN_V2_FILE}")
    print(f"SAMPLE_SUBMISSION_V2_FILE: {SAMPLE_SUBMISSION_V2_FILE}")

    ## [markdown]
    # # data prep

    ##
    train = dd.read_csv(TRAIN_FILE)
    # train = dd.concat((train, dd.read_csv(TRAIN_V2_FILE)), axis=0, ignore_index=True).reset_index(drop=True)
    train = dd.concat([train, dd.read_csv(TRAIN_V2_FILE)])

    test = dd.read_csv(SAMPLE_SUBMISSION_V2_FILE)

    ##
    len(train)

    ##
    transactions = dd.read_csv(TRANSACTION_FILE, usecols=['msno'])
    transactions = dd.concat([transactions, dd.read_csv(TRANSACTION_V2_FILE, usecols=['msno'])])
    transactions = dd.DataFrame(transactions['msno'].value_counts().reset_index()).compute()
    transactions.columns = ['msno','trans_count']
    train = train.merge(transactions, how='left', on='msno')
    test = test.merge(transactions, how='left', on='msno')

    ##


    ##
    transactions = dd.read_csv(TRANSACTION_V2_FILE) 
    transactions = transactions.sort_values(by=['transaction_date'], ascending=[False]).reset_index(drop=True)
    transactions = transactions.drop_duplicates(subset=['msno'], keep='first')

    train = dd.merge(train, transactions, how='left', on='msno')
    test = dd.merge(test, transactions, how='left', on='msno')
    # transactions=[]

    ##


    ##
    user_logs = dd.read_csv(USER_LOGS_V2_FILE, usecols=['msno'])
    user_logs = dd.DataFrame(user_logs['msno'].value_counts().reset_index()).compute()
    user_logs.columns = ['msno','logs_count']
    train = dd.merge(train, user_logs, how='left', on='msno')
    test = dd.merge(test, user_logs, how='left', on='msno')
    # user_logs = []; 

    ##
    train

    ##
    def transform_df(df):
        df = dd.DataFrame(df)
        df = df.sort_values(by=['date'], ascending=[False])
        df = df.reset_index(drop=True)
        df = df.drop_duplicates(subset=['msno'], keep='first')
        return df

    def transform_df2(df):
        df = df.sort_values(by=['date'], ascending=[False])
        df = df.reset_index(drop=True)
        df = df.drop_duplicates(subset=['msno'], keep='first')
        return df

    ##
    # last_user_logs = []
    # last_user_logs.append(transform_df(dd.read_csv(USER_LOGS_V2_FILE)))
    # last_user_logs = dd.concat(last_user_logs, axis=0, ignore_index=True).reset_index(drop=True)
    # last_user_logs = transform_df2(last_user_logs)
    # print ('merging user logs features...')
    # train = dd.merge(train, last_user_logs, how='left', on='msno')
    # test = dd.merge(test, last_user_logs, how='left', on='msno')
    # # last_user_logs=[]

    ##
    members = dd.read_csv(MEMBERS_FILE)
    train = dd.merge(train, members, how='left', on='msno')
    test = dd.merge(test, members, how='left', on='msno')
    print('members merge...')

    ##
    gender = {'male':1, 'female':2}
    train['gender'] = train['gender'].map(gender)
    test['gender'] = test['gender'].map(gender)

    ##
    train = train.fillna(0)
    test = test.fillna(0)

    ##
    train = train.compute()
    test = test.compute()

    ##
    del members
    del transactions
    del user_logs


    ##
    import gc
    gc.collect()

    ## [markdown]
    # # training

    ##
    train

    ##
    cols = [ c for c in train.columns if c not in ['is_churn', 'msno']]

    X_train = train[cols]
    y_train = train['is_churn']
    X_test = test[cols]
    # y_train = test['is_churn']

    ##
    from sklearn.neural_network import MLPClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import log_loss

    ## [markdown]
    # ## Mean baseline

    ##
    mean_is_churn = train['is_churn'].mean()
    print(f"mean : {mean_is_churn}")

    print(f"-- Mean baseline Network -- ")
    # Evaluate the model
    y_pred_prob = [mean_is_churn]*X_train.shape[0]
    y_pred = [1 if x > 0.5 else 0 for x in y_pred_prob]

    accuracy = accuracy_score(y_train, y_pred)
    print(f"Train Accuracy: {accuracy:.4f}")

    logloss = log_loss(y_train, y_pred_prob)
    print(f"Train Log Loss: {logloss:.4f}")


    ## [markdown]
    # ## simple feedforward neural netwok

    ##
    # Standardizing data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit_transform(X_test)

    X_train_lgb = X_train.copy()
    X_train_lgb['trans_count'] = X_train_lgb['trans_count'].astype('int64')
    X_train_lgb['logs_count'] = X_train_lgb['logs_count'].astype('int64')

    X_test_lgb = X_test.copy()
    X_test_lgb['trans_count'] = X_test_lgb['trans_count'].astype('int64')
    X_test_lgb['logs_count'] = X_test_lgb['logs_count'].astype('int64')


    print("-----")
    print(X_train.columns)
    print(X_train.head())
    print("-----")


    # Define the objective function for Optuna
    def objective(trial):
        # Define a reduced hyperparameter search space
        param = {
            'objective': 'binary',
            'metric': 'binary_logloss',
            'boosting_type': 'gbdt',
            'learning_rate': trial.suggest_loguniform('learning_rate', 0.01, 0.1),  # Focused range
            'num_leaves': trial.suggest_int('num_leaves', 20, 50),                 # Reduced range
            'min_child_samples': trial.suggest_int('min_child_samples', 10, 30),   # Smaller range
            'n_estimators': trial.suggest_int('n_estimators', 50, 150),            # Moderate boosting rounds
            'max_depth': trial.suggest_int('max_depth', -1, 15),                   # Practical range
        }

        # Split data for validation
        X_train_part, X_valid, y_train_part, y_valid = train_test_split(
            X_train_lgb, y_train, test_size=0.2, random_state=42
        )

        # Train the model
        model = lgb.LGBMClassifier(**param)
        # model = model.train(params, train_data, num_boost_round=100)

        model.fit(X_train_part, y_train_part, eval_set=[(X_valid, y_valid)])
                #   eval_metric='logloss',  verbose=0) # early_stopping_rounds=10,

        # Predict and calculate log loss on the validation set
        y_valid_pred = model.predict_proba(X_valid)[:, 1]
        return log_loss(y_valid, y_valid_pred)

    # Create an Optuna study with fewer trials
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=20)  # Limit to 20 trials

    # Best parameters and score
    print(f"Best Parameters: {study.best_params}")
    print(f"Best Log Loss: {study.best_value:.4f}")

    # Train the final model with the best parameters
    best_params = study.best_params
    model = lgb.LGBMClassifier(**best_params)
    model.fit(X_train_lgb, y_train)

    # Evaluate the final model
    y_train_pred = model.predict_proba(X_train_lgb)[:, 1]
    train_logloss = log_loss(y_train, y_train_pred)
    print(f"Final Training Log Loss: {train_logloss:.4f}")


    print(f"-- LGBM Classifier -- ")
    # Evaluate the model
    y_pred = model.predict(X_train_lgb)
    accuracy = accuracy_score(y_train, y_pred)
    print(f"Train Accuracy: {accuracy:.4f}")

    y_pred_prob = model.predict_proba(X_train_lgb)
    logloss = log_loss(y_train, y_pred_prob)
    print(f"Train Log Loss: {logloss:.4f}")
    mean_prediction=y_pred.mean()
    print(f"mean of prediction : {mean_prediction}")

    ##
    print(f"diff in delta mean pred {mean_is_churn - mean_prediction}")

    ##
    print("predicting ..")
    y_pred = model.predict(X_test_scaled)


    ##
    len(X_test), len(test), len(y_pred)

    ##
    submission = test[['msno', 'is_churn']].copy()
    submission['is_churn'] = y_pred

    ##
    submission.to_csv(f'{OUTPUT_DIR}/submissions/submission_{MODEL_NAME}.csv', index=False)
    ##
    print("submission file saved")
    print("saving model ")
    MODEL_FILE = f"{OUTPUT_DIR}/models/{MODEL_NAME}_model.joblib"
    joblib.dump(model, MODEL_FILE)
    # loaded_model = joblib.load(MODEL_FILE)


if __name__ == '__main__':    
    # Set up a Dask Cluster
    cluster = LocalCluster(n_workers=6, threads_per_worker=1, memory_limit='18GB')
    client = Client(cluster)
    main(client)