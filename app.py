# import modules 
from flask import Flask, json, request, jsonify, url_for
from basketball_reference_utils import get_specific_pair

# initialize Flask app 
app = Flask(__name__)



@app.route('/')
def index():
    return "<p>CS 62000 NBA Crowdsourcing Project</p>"



@app.route('/stats/<player1>/<player2>/<season1>/<season2>')
def stats(player1=None, player2=None, season1=None, season2=None):
    
    player1 = player1.replace("_", " ")
    player2 = player2.replace("_", " ")
    
    player1stats, player1url, player2stats, player2url = get_specific_pair(player1, player2, season1, season2)

    stats1 = player1stats.to_json()
    stats2 = player2stats.to_json()

    statsTotal = stats1 + stats2

    return statsTotal

    



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
