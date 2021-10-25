# import modules 
from flask import Flask, request, jsonify

# initialize Flask app 
app = Flask(__name__)

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
