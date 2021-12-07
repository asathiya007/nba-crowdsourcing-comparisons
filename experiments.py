# import modules 
from basketball_reference_utils import get_random_pair
from machine_learning import (construct_dataset, FEATURES, DEFAULT_HOLDOUT,
    RF_MAX_DEPTH, RF_NUM_EST, RF_MAX_FEATURES)
import os
import pandas as pd
from predict_better_player import predict_better_player
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import statistics
import time

# declare constants
EXP_DIR_PATH = './experiment_results'
MODEL_PATHS = ['./linear_regression.joblib', './random_forest.joblib']
ITERATIONS = 5


def exp_random_pair_gen_time(): 
    # get scraping times 
    times = [] 
    i = 0
    while i < ITERATIONS:
        start = time.time() 
        _ = get_random_pair()
        end = time.time() 
        times.append(end - start) 
        i += 1
    
    # compute statistics 
    mean = statistics.mean(times)
    median = statistics.median(times)
    range = max(times) - min(times)
    std_dev = statistics.stdev(times)
    variance = statistics.variance(times)
    agg_times = [mean, median, range, std_dev, variance]

    # save results as CSV file 
    columns = ['Mean', 'Median', 'Range', 'Standard Deviation', 'Variance']
    index = ['Random Pair Generation Time (s)']
    random_pair_times_df = pd.DataFrame([agg_times], index=index, columns=columns)
    if not os.path.exists(EXP_DIR_PATH): 
        os.makedirs(EXP_DIR_PATH)
    random_pair_times_df.to_csv(f'{EXP_DIR_PATH}/exp_random_pair_gen_times.csv')

    # return results
    return random_pair_times_df

def exp_construct_dataset_time(): 
    # get dataset construction times 
    times = []
    i = 0
    while i < ITERATIONS:
        start = time.time()
        dataset = construct_dataset()
        end = time.time()
        times.append(end - start)
        i += 1

    # compute statistics 
    mean = statistics.mean(times)
    median = statistics.median(times)
    range = max(times) - min(times)
    std_dev = statistics.stdev(times)
    variance = statistics.variance(times)
    agg_times = [mean, median, range, std_dev, variance]

    # save results as CSV file 
    columns = ['Number of Samples', 'Mean', 'Median', 'Range', 'Standard Deviation', 'Variance']
    index = ['Dataset Construction Time (s)']
    cons_data_times_df = pd.DataFrame([[len(dataset)] + agg_times], index=index, columns=columns)
    if not os.path.exists(EXP_DIR_PATH): 
        os.makedirs(EXP_DIR_PATH)
    cons_data_times_df.to_csv(f'{EXP_DIR_PATH}/exp_cons_dataset_times.csv')

    # return results 
    return cons_data_times_df

def exp_model_training(): 
    # get dataset 
    dataset = pd.read_csv('./nba_crowdsourcing_comparisons.csv')

    # train each model for each holdout value 
    data = []
    for scaler in [None, StandardScaler()]: 
        for _ in range(3): 
            # partition dataset for model training 
            (nba_train_features, nba_test_features, nba_train_labels,
                nba_test_labels) = train_test_split(dataset[FEATURES], 
                    dataset['label'], test_size=DEFAULT_HOLDOUT, shuffle=True)

            # perform scaling
            if scaler is not None: 
                nba_train_features = scaler.fit_transform(nba_train_features)
                nba_test_features = scaler.transform(nba_test_features)

            # train linear regression model 
            linear_regression = LinearRegression()
            start = time.time() 
            linear_regression.fit(nba_train_features, nba_train_labels)
            end = time.time() 
            lr_fit_time = end - start
            preds = linear_regression.predict(nba_test_features)
            lr_mse = mean_squared_error(nba_test_labels, preds)

            # train random forest model 
            random_forest = RandomForestRegressor(n_estimators=RF_NUM_EST, 
                max_depth=RF_MAX_DEPTH, max_features=RF_MAX_FEATURES)
            start = time.time() 
            random_forest.fit(nba_train_features, nba_train_labels)
            end = time.time()
            rf_fit_time = end - start
            preds = random_forest.predict(nba_test_features)
            rf_mse = mean_squared_error(nba_test_labels, preds)

            # store results 
            results = [lr_fit_time, lr_mse, rf_fit_time, rf_mse]
            data.append(results)

    # store data as CSV file
    columns = ['Linear Regression Fit Time (s)', 'Linear Regression MSE', 
        'Random Forest Fit Time (s)', 'Random Forest MSE'] 
    index = ['No Scaling 1', 'No Scaling 2', 'No Scaling 3', 'Standard Scaling 1', 
        'Standard Scaling 2', 'Standard Scaling 3']
    model_training_df = pd.DataFrame(data, index, columns)
    if not os.path.exists(EXP_DIR_PATH): 
        os.makedirs(EXP_DIR_PATH)
    model_training_df.to_csv(f'{EXP_DIR_PATH}/exp_model_training.csv')

    # return results 
    return model_training_df

def exp_model_prediction_time(): 
    # define comparison instances 
    comparisons = [
        ('Michael Jordan', 'Kobe Bryant', '1990-91', '2005-06'), 
        ('Kobe Bryant', 'LeBron James', '2005-06', '2012-13'), 
        ('LeBron James', 'Stephen Curry', '2012-13', '2015-16'),
        ('Tim Duncan', 'Kobe Bryant', '2001-02', '2005-06'),
        ('LeBron James', 'Giannis Antetokounmpo', '2011-12', '2020-21')
    ]

    # make predictions, record times
    times = []
    model_choices = ['lr', 'rf']
    for model_choice in model_choices: 
        model_times = []
        for comp in comparisons:
            start = time.time()
            _ = predict_better_player(model_choice, comp[0], comp[1], comp[2], comp[3])
            end = time.time()
            model_times.append(end - start)
        mean = statistics.mean(model_times)
        median = statistics.median(model_times)
        range = max(model_times) - min(model_times)
        std_dev = statistics.stdev(model_times)
        variance = statistics.variance(model_times)
        times.append([mean, median, range, std_dev, variance])

    # assemble times as CSV file
    index = ['Linear Regression Prediction Time (s)', 'Random Forest Prediction Time (s)']
    columns = ['Mean', 'Median', 'Range', 'Standard Deviation', 'Variance']
    model_pred_times_df = pd.DataFrame(times, index, columns)
    if not os.path.exists(EXP_DIR_PATH): 
        os.makedirs(EXP_DIR_PATH)
    model_pred_times_df.to_csv(f'{EXP_DIR_PATH}/exp_model_pred_times.csv')

    # return results 
    return model_pred_times_df