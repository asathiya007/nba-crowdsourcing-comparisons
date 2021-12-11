# NBA Crowdsourcing Comparisons 
Project repository for Georgia Tech CS 6220 course project. Crowdsourcing and machine learning are used to gauge who is better between two NBA players who played at different points in time. 

## Get Started 
1. Create and activate Python virtual environment. 
2. Install dependencies in `requirements.txt` with `pip`. 
3. Run the app with this command: `flask run`. 


## Execution Instructions
We will now explain how to run the prediction commands for NBA pair of players:

1. Navigate to the source directory `nba-crowdsourcing-comparisons/`
2. Run `python predict_better_player.py (model) (player1) (XXXX-XX) (player2) (XXXX-XX)`, where:
- model: lr, rf
    - lr: Linear Regression
    - rf: Random Forest
- player1, player2: `FirstName LastName` for the desired player
- XXXX-XX: Season year format, example: `2018-19`
3. Example command: `python predict_better_player.py lr 'Lebron James' '2012-13' 'Michael Jordan' '2002-03'`

The command should output a `prediction score` as well as a `execution time` value in the command line.

## Credits 
This project uses the `basketball_reference_scraper` package, which is licensed under the MIT License. Hence, this project will also be licensed under the MIT License. The source for the `basketball_reference_scraper` package can be found [here](https://github.com/vishaalagartha/basketball_reference_scraper).  


