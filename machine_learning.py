# import modules
import argparse
from basketball_reference_utils import get_specific_pair, STATS
import firebase_admin
from firebase_admin import credentials, db
import joblib 
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import time 

# declare constants 
FEATURES = [
    'ppg1',
    'apg1',
    'rpg1', 
    'bpg1',
    'spg1',
    'tov1',
    'gp1',
    'mp1',
    'sp1',
    'ppg2',
    'apg2',
    'rpg2',
    'bpg2',
    'spg2',  
    'tov2',
    'gp2', 
    'mp2',   
    'sp2'
]
DEFAULT_HOLDOUT = 0.20
RF_NUM_EST=10
RF_MAX_DEPTH=10
RF_MAX_FEATURES=None


def construct_dataset():
    # connect to database 
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            './basketball-crowdsourcing-firebase-adminsdk-rmel8-fd8a465175.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://basketball-crowdsourcing-default-rtdb.firebaseio.com/'
        })

    # get questions and responses 
    questions_ref, responses_ref = db.reference('/questions'), db.reference(
        '/questionResponses')
    questions, responses = questions_ref.get(), responses_ref.get()

    # assemble dataset 
    columns = [
        'name1', 
        'season1', 
        'ppg1',
        'apg1',
        'rpg1', 
        'bpg1',
        'spg1',
        'tov1',
        'gp1',
        'mp1',
        'sp1',
        'name2', 
        'season2',
        'ppg2',
        'apg2',
        'rpg2',
        'bpg2',
        'spg2',  
        'tov2',
        'gp2', 
        'mp2',   
        'sp2',
        'label'
    ]
    dataset = []
    for question in questions.keys(): 
        # get player and season info 
        player1 = questions[question]['player1']
        player1_dict = dict()
        for key in player1.keys(): 
            player1_dict[key.strip()] = player1[key]
        player1_name = player1['name']
        player1_season = player1['season']
        player2 = questions[question]['player2']
        player2_dict = dict()
        for key in player2.keys(): 
            player2_dict[key.strip()] = player2[key]
        player2_name = player2_dict['name']
        player2_season = player2_dict['season']

        # if player 1 or player 2 name is undefined, skip to next sample 
        if player1_name.strip() == 'undefined' or player2_name.strip() == 'undefined':
            continue

        # get player stats
        player1_stats, _, player2_stats, _ = get_specific_pair(player1_name, 
            player2_name, player1_season, player2_season)
        
        # create feature vector 
        feature_vector = []
        feature_vector.append(player1_name)
        feature_vector.append(player1_season)
        for stat in STATS: 
            feature_vector.append(player1_stats[stat])
        feature_vector.append(player2_name)
        feature_vector.append(player2_season)
        for stat in STATS: 
            feature_vector.append(player2_stats[stat])
        
        # get label
        label = None 
        try: 
            player1_votes = responses[question][player1_name]
            player2_votes = responses[question][player2_name]
            label = player1_votes / (player1_votes + player2_votes)
        except:
            continue
        
        # add sample to dataset 
        if label is None: 
            continue 
        dataset.append(feature_vector + [label])

        # add flipped sample to dataset 
        flipped_label = 1 - label
        flipped_feature_vector = (feature_vector[len(feature_vector) // 2 :] 
            + feature_vector[: len(feature_vector) // 2])
        dataset.append(flipped_feature_vector + [flipped_label])

    # create dataframe 
    dataset_df = pd.DataFrame(dataset, columns=columns)
    dataset_df.to_csv('./nba_crowdsourcing_comparisons.csv', index=False) 

    # return dataset
    return dataset_df

def train_machine_learning_models(nba_train_features, nba_train_labels, nba_test_features, 
    nba_test_labels):
    # fit and evaluate linear regression model 
    linear_regression = LinearRegression()
    linear_regression.fit(nba_train_features, nba_train_labels)
    print('Trained linear regression model')
    preds = linear_regression.predict(nba_test_features)
    lr_mse = mean_squared_error(nba_test_labels, preds)
    print('Mean Squared Error: ', lr_mse)
    joblib.dump(linear_regression, './linear_regression.joblib')
    print('Saved linear regression model as ./linear_regression.joblib\n')
    
    # fit and evaluate random forest model 
    random_forest = RandomForestRegressor(
        n_estimators=RF_NUM_EST,
        max_depth=RF_MAX_DEPTH, 
        max_features=RF_MAX_FEATURES
    )
    random_forest.fit(nba_train_features, nba_train_labels)
    print('Trained random forest model')
    preds = random_forest.predict(nba_test_features)
    rf_mse = mean_squared_error(nba_test_labels, preds)
    print('Mean Squared Error: ', rf_mse)
    joblib.dump(random_forest, './random_forest.joblib')
    print('Saved random forest model as ./random_forest.joblib\n')

    # return accuracies and F1 scores 
    return linear_regression, lr_mse, random_forest, rf_mse

def machine_learning_pipeline(use_existing_data=1): 
    # construct dataset from Firebase table data 
    if use_existing_data == 0 or not os.path.exists(
        './nba_crowdsourcing_comparisons.csv'): 
        nba_dataset = construct_dataset() 
    else: 
        nba_dataset = pd.read_csv('./nba_crowdsourcing_comparisons.csv')
        print('Loaded existing dataset\n')

    # extract features and labels 
    nba_features = nba_dataset[FEATURES]
    nba_labels = nba_dataset['label']    

    # partition dataset for model training, standard-scale features
    (nba_train_features, nba_test_features, nba_train_labels,
        nba_test_labels) = train_test_split(nba_features, nba_labels, 
        test_size=DEFAULT_HOLDOUT, shuffle=True)
    standard_scaler = StandardScaler()
    nba_train_features = standard_scaler.fit_transform(nba_train_features)
    nba_test_features = standard_scaler.transform(nba_test_features)
    joblib.dump(standard_scaler, './standard_scaler.joblib')
    print('Prepared data for model training\n')

    # train models 
    train_machine_learning_models(nba_train_features, nba_train_labels, 
        nba_test_features, nba_test_labels)

if __name__=='__main__':
    # parse command line arguments 
    parser = argparse.ArgumentParser(description='machine learning pipeline args')
    parser.add_argument('use_existing_data', help='int - 0 to obtain updated data from' 
        + ' database, any other number to use existing dataset', type=int)
    args = parser.parse_args()

    # execute machine learning pipeline
    print(f'Executing machine learning pipeline\n')
    start = time.time() 
    machine_learning_pipeline(args.use_existing_data)
    end = time.time()
    print(f'Execution time of machine learning pipeline: {end - start} s')
