# NBA Crowdsourcing Comparisons 
Project repository for Georgia Tech CS 6220 course project. Crowdsourcing and machine learning are used to gauge who is better between two NBA players who played at different points in time. 

## Get Started 
1. Create and activate Python virtual environment with `pip`. See this link: `https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/`
2. Install dependencies in `requirements.txt` with `pip` with the command `pip install -r requirements.txt`. 
3. Run the app with this command: `flask run`. 

## Execution Instructions - Train Machine Learning Models
The machine learning models (logistic regression and random forest regressor) and scaler have already been trained and are available as `linear_regression.joblib`, `random_forest.joblib`, and `standard_scaler.joblib`. To retrain the models see the command below. Hyperparameters of the models can be changed in the `machine_learning.py` file. 

We will now explain how to run the command to train the machine learning models: 
1. Run `python predict_better_player.py (use_existing_data)`, where: 
- use_existing_data: 0 to pull the updated, new data from Firebase, any other number to use the existing dataset in `nba_crowdsourcing_comparisons.csv` 
2. Example command: `python predict_better_player.py 1`

This script pulls data from our Firebase databse, which requires a JSON file with a private key. We have this file on our local machines, but for security purposes, we have not included this file in this public GitHub repository. If this is required for grading, please contact one of the team members as the following email addresses: `asathiya6@gatech.edu`, `rchawla36@gatech.edu`, `smanjesh3@gatech.edu`, `pkhorana3@gatech.edu`. 

## Execution Instructions - Predict Better Player 
We will now explain how to run the prediction commands for NBA pair of players:
1. Run `python predict_better_player.py (model) (player1) (XXXX-XX) (player2) (XXXX-XX)`, where:
- model: lr, rf
    - lr: Linear Regression
    - rf: Random Forest
- player1, player2: `FirstName LastName` for the desired player
- XXXX-XX: Season year format, example: `2018-19`
2. Example command: `python predict_better_player.py lr 'Lebron James' '2012-13' 'Michael Jordan' '2002-03'`

The command should output a `prediction score` as well as a `execution time` value in the command line.
The prediction score is a value between 0 and 1 that represents the amount of votes the first player will get over the second player if people had to vote between which of the two players is better. This is a reliable metric for determining who is the better NBA player since voting systems are used to determine NBA All-Star selections as well as the winners of the regular season MVP, Finals MVP, and other awards.  

## Execution Instructions - Experiments
To run the experiments, open the Jupyter notebook `experiments.ipynb` and run the Jupyter notebook cells. The experiments in the notebook measure the performance of our system as it pertains to time and mean-squared error. We also manually ran experiments to observe and analyze the accuracy and symmetry (prediction values that have a sum close to 1 when the order of player 1 and player 2 are swapped when passed to the machine learning model) of our models for players in the same/different decade and position. These results are discussed in the `documentation` folder.

We will now explain how to run the prediction commands for NBA pair of players:
1. Run `python predict_better_player.py (model) (player1) (XXXX-XX) (player2) (XXXX-XX)`, where:
- model: lr, rf
    - lr: Linear Regression
    - rf: Random Forest
- player1, player2: `FirstName LastName` for the desired player
- XXXX-XX: Season year format, example: `2018-19`
2. Example command: `python predict_better_player.py lr 'Lebron James' '2012-13' 'Michael Jordan' '2002-03'`

The command should output a `prediction score` as well as a `execution time` value in the command line.
The prediction score is a value between 0 and 1 that represents the amount of votes the first player will get over the second player if people had to vote between which of the two players is better. This is a reliable metric for determining who is the better NBA player since voting systems are used to determine NBA All-Star selections as well as the winners of the regular season MVP, Finals MVP, and other awards. 

## Acknowledgements 
We would like to thank Professor Ling Liu and the CS 6220 Big Data Systems and Analytics teaching team for guiding us throughout the semester and helping us create a great project. 

## Credits
This project uses the `basketball_reference_scraper` package, which is licensed under the MIT License. Hence, this project will also be licensed under the MIT License. The source for the `basketball_reference_scraper` package can be found [here](https://github.com/vishaalagartha/basketball_reference_scraper).  


