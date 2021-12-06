# import modules
from basketball_reference_utils import get_specific_pair, STATS
import firebase_admin
from firebase_admin import credentials, db
import joblib 
import logging
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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

def construct_dataset():
    # connect to database 
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
        player1_votes = responses[question][player1_name]
        player2_votes = responses[question][player2_name]
        label = None
        if player1_votes > player2_votes: 
            label = 0
        elif player2_votes > player1_votes: 
            label = 1
        
        # add sample to dataset 
        if label is None: 
            continue 
        dataset.append(feature_vector + [label])

        # add flipped sample to dataset 
        flipped_label = 1 if label == 0 else 0
        flipped_feature_vector = (feature_vector[len(feature_vector) // 2 :] 
            + feature_vector[: len(feature_vector) // 2])
        dataset.append(flipped_feature_vector + [flipped_label])

    # create dataframe 
    dataset_df = pd.DataFrame(dataset, columns=columns)
    try: 
        dataset_df.to_csv('./nba_crowdsourcing_comparisons.csv', index=False) 
    except: 
        logging.warn('Dataset could not be saved as CSV file')

    # return dataset
    return dataset_df

def _train_machine_learning_models(nba_train_features, nba_train_labels, nba_test_features, 
    nba_test_labels):
    # fit and evaluate logistic regression model 
    logistic_regression = LogisticRegression()
    logistic_regression.fit(nba_train_features, nba_train_labels)
    print('Fitted logistic regression model!')
    preds = logistic_regression.predict(nba_test_features)
    print('F1 score: ', f1_score(nba_test_labels, preds) )
    print('Accuracy: ', accuracy_score(nba_test_labels, preds))
    joblib.dump(logistic_regression, './logistic_regression.joblib')
    print('Saved logistic regression model as ./logistic_regression.joblib\n')
    
    # fit and evaluate random forest model 
    random_forest = RandomForestClassifier(n_estimators=5, max_depth=20)
    random_forest.fit(nba_train_features, nba_train_labels)
    print('Fitted random forest model!')
    preds = random_forest.predict(nba_test_features)
    print('F1 score: ', f1_score(nba_test_labels, preds) )
    print('Accuracy: ', accuracy_score(nba_test_labels, preds))
    joblib.dump(random_forest, './random_forest.joblib')
    print('Saved random forest model as ./random_forest.joblib\n')

def predict_better_player(model_path, player_name1, player_name2, season1, 
    season2, playoffs=False, career=False): 
    # get players' stats 
    player1_stats, _, player2_stats, _ = get_specific_pair(player_name1, 
        player_name2, season1, season2, playoffs=playoffs, career=career)
    
    # create feature vector 
    feature_vector1 = []
    feature_vector2 = []
    for stat in STATS: 
        feature_vector1.append(player1_stats[stat])
        feature_vector2.append(player2_stats[stat])
    feature_vector = feature_vector1 + feature_vector2

    # load scaler and model, then make prediction 
    std_scaler = None 
    try: 
        std_scaler = joblib.load('./std_scaler.joblib')
    except: 
        logging.warn('Could not load standard scaler')
        return None
    feature_vector = pd.DataFrame([feature_vector], columns=FEATURES)
    feature_vector = std_scaler.transform(feature_vector)

    model = joblib.load(model_path)
    pred = model.predict_proba(feature_vector)

    # return prediction to user 
    return pred

def machine_learning_pipeline(): 
    # construct dataset from Firebase table data 
    nba_dataset = construct_dataset() 

    # extract features and labels 
    nba_features = nba_dataset[FEATURES]
    nba_labels = nba_dataset['label']

    # partition dataset for model training 
    (nba_train_features, nba_test_features, nba_train_labels,
        nba_test_labels) = train_test_split(nba_features, nba_labels, test_size=0.2, 
        shuffle=True)

    # perform scaling, save scaler 
    std_scaler = StandardScaler()
    nba_train_features = std_scaler.fit_transform(nba_train_features)
    nba_test_features = std_scaler.transform(nba_test_features)
    joblib.dump(std_scaler, './std_scaler.joblib')

    # train models 
    _train_machine_learning_models(nba_train_features, nba_train_labels, 
        nba_test_features, nba_test_labels)

if __name__=='__main__':
    machine_learning_pipeline()