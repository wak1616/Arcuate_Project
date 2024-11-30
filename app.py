from flask import Flask, jsonify, request, render_template, flash
from flask_session import Session

import helpers
from helpers import arcuatestartend, calculate_single_arcuate_sweep

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
    return render_template("index.html", current_page='home')

@app.route('/calculate', methods=['POST'])
def calculate():
    #Extract parameters from the request
    data = request.get_json() #turns the "stringified" JSON into a Python dictionary called "data"

    # accessing the individual values from the dictionary "data" and  converts them to appropriate types (just to make sure):
    age = int(data.get('age'))
    eye = data.get('eye')
    sex = data.get('sex')
    cassini_corneal_astigmatism = float(data.get('cassini_corneal_astigmatism'))
    iolmaster700_corneal_astigmatism = float(data.get('iolmaster700_corneal_astigmatism'))
    steep_axis = int(data.get('steep_axis'))
    Mean_K = float(data.get('Mean_K'))
    WTW = float(data.get('WTW'))
    
    # Run function to calculate and return arcuate info back to script
    print(f"Calculating arcuate sweep with parameters: age={age}, eye={eye}, sex={sex}, WTW={WTW}, Mean_K={Mean_K}, cassini_corneal_astigmatism={cassini_corneal_astigmatism}, iolmaster700_corneal_astigmatism={iolmaster700_corneal_astigmatism}, steep_axis={steep_axis}")
    Predicted_Arcuate_Sweep_Single = calculate_single_arcuate_sweep(age, eye, sex, WTW, Mean_K, cassini_corneal_astigmatism, iolmaster700_corneal_astigmatism, steep_axis)
    print(f"Calculated sweep: {Predicted_Arcuate_Sweep_Single}")
    
    # Define the axes of the 2 different arcuates
    axis1 = steep_axis
    axis2 = steep_axis + 180

    #Run through arcstartend function that generates arcuate start and end values (with degrees altered for Canvas and in radians)
    arc1start, arc1end = arcuatestartend(Predicted_Arcuate_Sweep_Single, axis1)
    arc2start, arc2end = arcuatestartend(Predicted_Arcuate_Sweep_Single, axis2)

    #Set up variables which will show the arcuate parameters in string format
    arcuate1text = f"Arcuate 1: {round(Predicted_Arcuate_Sweep_Single)} degrees length at {axis1}°"
    arcuate2text = f"Arcuate 2: {round(Predicted_Arcuate_Sweep_Single) } degrees length at {axis2}°"

    #Send back the result of the calculations for arcuate drawings on canvas image
    return jsonify({
    'arcuate1text': arcuate1text,
    'arcuate2text': arcuate2text,
    'arc1start': arc1start,
    'arc1end': arc1end,
    'arc2start': arc2start,
    'arc2end': arc2end
    }), 200

@app.route("/about")
def about():
    return render_template("about.html", current_page='about')