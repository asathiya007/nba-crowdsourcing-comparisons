# import modules
from basketball_reference_utils import get_specific_pair, STATS
import joblib 
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import train_test_split


def construct_dataset():
    # TODO: get data from Firebase table, construct dataset for classification task
    pass 

def train_machine_learning_models(nba_train_features, nba_train_labels, nba_test_features, 
    nba_test_labels):
    # fit and evaluate logistic regression model 
    logistic_regression = LogisticRegression()
    logistic_regression.fit(nba_train_features, nba_train_labels)
    print('Fitted logistic regression model!')
    preds = logistic_regression.predict(nba_test_features)
    print('F1 score: ', f1_score(nba_test_labels, preds) )
    print('Accuracy: ', accuracy_score(nba_test_labels, preds))
    joblib.dump(logistic_regression, './logistic.joblib')
    print('Saved logistic regression model as ./logistic.joblib\n')
    
    # fit and evaluate random forest model 
    random_forest = RandomForestClassifier(n_estimators=10, max_depth=10)
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

    # load model and make prediction 
    model = joblib.load(model_path)
    pred = model.predict_proba(feature_vector)

    # return prediction to user 
    return pred

def machine_learning_pipeline(): 
    # construct dataset from Firebase table data 
    nba_dataset = construct_dataset() 

    # partition dataset for model training 
    (nba_train_features, nba_train_labels, nba_test_features, 
        nba_test_labels) = train_test_split(nba_dataset, test_size=0.2, 
        shuffle=True)

    # train models 
    train_machine_learning_models(nba_train_features, nba_train_labels, 
        nba_test_features, nba_test_labels)

if __name__=='__main__':
    machine_learning_pipeline()