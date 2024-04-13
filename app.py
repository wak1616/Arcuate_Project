from flask import Flask, jsonify, request, render_template, flash
from flask_session import Session

#configure application
app = Flask(__name__)

#Ensure responses aren't cached
@app.after_request
def after_request(response):
    #Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    #Extract parameters from the request
    input_data = request.get_json()
    
    #Perform hidden calculations here:
    result = some_complex_function(input_data['param1'], input_data['param2'])

    #Send back the result of the calculations
    return jsonify(result)

def some_complex_function(param1, param2):
    #function here
    return {'calculatedValue': param1 * param2}


