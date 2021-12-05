# import modules 
from flask import Flask, jsonify
from basketball_reference_utils import get_specific_pair, get_random_pair


# initialize Flask app 
app = Flask(__name__)


@app.route('/')
def index():
    return "<p>CS 6220 NBA Crowdsourcing Project</p>"

@app.route('/stats/<player1>/<player2>/<season1>/<season2>')
def stats(player1=None, player2=None, season1=None, season2=None):
    
    player1 = player1.replace("_", " ")
    player2 = player2.replace("_", " ")
    
    player1stats, player1url, player2stats, player2url = None, None, None, None
    while (player1stats is None or player1url is None or player2stats is None or 
        player2url is None):  
        player1stats, player1url, player2stats, player2url = get_specific_pair(
            player1, player2, season1, season2)
    
    res = {
        'player1': {
            'stats': player1stats, 
            'img': player1url
        }, 
        'player2': {
            'stats': player2stats, 
            'img': player2url
        }
    }

    return jsonify(res)

@app.route('/stats/random')
def randomStats():
    
    player1stats, player1url, player2stats, player2url = None, None, None, None
    while (player1stats is None or player1url is None or player2stats is None or 
        player2url is None):  
        player1stats, player1url, player2stats, player2url = get_random_pair()
    
    res = {
        'player1': {
            'stats': player1stats, 
            'img': player1url
        }, 
        'player2': {
            'stats': player2stats, 
            'img': player2url
        }
    }

    print(res)

    return jsonify(res)
    


@app.route('/test')
def hello_world():
    '''
    Test endpoint to verify that API is running. 
    '''

    # return message confirming API is running  
    responseDict = {
        'msg': 'NBA Crowdsourcing Comparisons API running!'
    }
    return jsonify(responseDict)
