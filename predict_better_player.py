# import modules 
from basketball_reference_utils import get_specific_pair
from machine_learning import FEATURES, STATS
import joblib 
import pandas as pd 
import argparse
import time


def predict_better_player(model_choice, player_name1, player_name2, season1, 
    season2, playoffs=False, career=False): 
    try: 
        if model_choice == 'lr':
            model = joblib.load('./linear_regression.joblib')
        elif model_choice == 'rf':
            model = joblib.load('./random_forest.joblib')
        else: 
            print('Invalid model choice')
            return None

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

        # load scaler and model, make prediction 
        standard_scaler = joblib.load('./standard_scaler.joblib')
        feature_vector = standard_scaler.transform(pd.DataFrame([feature_vector], 
            columns=FEATURES))
        pred = model.predict(feature_vector)
    except: 
        print('Prediction failed')
        pred = None 

    # return prediction to user 
    return pred


if __name__=='__main__':
    # read command line arguments 
    parser = argparse.ArgumentParser(description='Predict better player')
    parser.add_argument('model_choice', help='specify choice of machine learning model (\'rf\' '
        + 'or \'lr\'', type=str)
    parser.add_argument('player1_name', help='specify name of first player', type=str)
    parser.add_argument('player1_season', help='specify season for first player (XXXX-XX)', type=str)
    parser.add_argument('player2_name', help='specify name of first player', type=str)
    parser.add_argument('player2_season', help='specify season for first player (XXXX-XX)', type=str)
    args = parser.parse_args()

    # predict better player 
    player1_name = args.player1_name
    player2_name = args.player2_name
    player1_season = args.player1_season
    player2_season = args.player2_season
    start = time.time()
    pred = predict_better_player(args.model_choice, player1_name, player2_name, 
        player1_season, player2_season)[0]
    end = time.time()
    
    # print prediction details
    if pred is not None:
        print(f'Prediction: {pred}')
        print(f'Prediction time: {end - start} s')
