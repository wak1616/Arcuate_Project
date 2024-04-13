from flask import Flask, jsonify, request, render_template, flash
from flask_session import Session

from helpers import arcuatestartend

def calculate():

    data = {'age': 45, 'eye': "left", 'corneal_astigmatism': 1, 'steep_axis': 350}

    age = int(data.get('age'))
    eye = data.get('eye')
    corneal_astigmatism = float(data.get('corneal_astigmatism'))
    steep_axis = int(data.get('steep_axis'))

    #Define what against-the-rule astigmatism is (values correspond to degrees)
    def is_ATR(degree):
        ATR = [(0, 30), (150, 210), (330, 360)]
        return any(start <= degree <= end for start, end in ATR)

    print(f"Initial values: age={age}, eye={eye}, corneal_astigmatism={corneal_astigmatism}, steep_axis={steep_axis}")

    #if starting steep axis is near main incision (for right or left eye), then change steep axis to 180 deg away
    if eye == "right":
        if 150 <= steep_axis < 180:
            steep_axis = steep_axis + 180
        elif steep_axis == 180:
            steep_axis = 0
        elif 180 < steep_axis <= 210:
            steep_axis = steep_axis - 180
    if eye == "left" and (0 <= steep_axis <= 30 or 330 <= steep_axis <= 360):
        if 330 <= steep_axis < 360:
            steep_axis = steep_axis - 180
        elif steep_axis == 0 or steep_axis == 360:
            steep_axis = 180
        elif 0 < steep_axis <= 30:
            steep_axis = steep_axis + 180

    #Set up 2 dictionaries that will specify arcuate1 and arcuate2 with correct steep axes
    arcuate1 = {'arcuate_length': None, 'arcuate_axis': steep_axis}
    if 0 <= steep_axis < 180:
        arcuate2 = {'arcuate_length': None, 'arcuate_axis': steep_axis + 180}
    elif 180 <= steep_axis <= 360:
        arcuate2 = {'arcuate_length': None, 'arcuate_axis': steep_axis - 180}

    #Determine initial recommended incision length regardless of axis or age
    if corneal_astigmatism < 0.3:
        return jsonify({'error': "Astigmatism must be above 0.3"}), 400
    elif 0.3 <= corneal_astigmatism <= 0.40:
        arcuate1['arcuate_length'] = 20
        arcuate2 = None
    elif 0.4 < corneal_astigmatism <= 0.63:
        arcuate1['arcuate_length'] = 30
        arcuate2 = None
    elif 0.63 < corneal_astigmatism <= 0.88:
        arcuate1['arcuate_length'] = 20
        arcuate2['arcuate_length'] = 20
    elif 0.88 < corneal_astigmatism <= 1.1:
        arcuate1['arcuate_length'] = 25
        arcuate2['arcuate_length'] = 25
    elif 1.1 < corneal_astigmatism <= 1.25:
        arcuate1['arcuate_length'] = 30
        arcuate2['arcuate_length'] = 30
    elif corneal_astigmatism > 1.25:
        return jsonify ({'error': 'Astigmatism must be below 1.25. Recommend toric IOL instead'}), 400

    #Increase total astigmatism length by 5 degrees if against-the-rule (ATR) asgtigmatism
    if is_ATR(steep_axis) and arcuate2 is None:
        arcuate1['arcuate_length'] += 5
    elif is_ATR(steep_axis) and arcuate2 is not None:
        arcuate1['arcuate_length'] += 2.5
        arcuate2['arcuate_length'] += 2.5

    #Modify arcuate incision lengths for age of patient
    if age < 50:
        if arcuate2 is None:
                arcuate1['arcuate_length'] += 5
        else:
            arcuate1['arcuate_length'] += 2.5
            arcuate2['arcuate_length'] += 2.5
    elif 71 <= age <= 80:
        if arcuate2 is None:
                arcuate1['arcuate_length'] -= 5
        else:
            arcuate1['arcuate_length'] -= 2.5
            arcuate2['arcuate_length'] -= 2.5
    elif age > 80:
        if arcuate2 is None:
                arcuate1['arcuate_length'] -= 10
        else:
            arcuate1['arcuate_length'] -= 5
            arcuate2['arcuate_length'] -= 5



    #Run through functions that generates arcuate start and end values (with degrees altered for Canvas and in radians)
    arc1start, arc1end = arcuatestartend(arcuate1['arcuate_length'], arcuate1['arcuate_axis'])
    if arcuate2 == None:
        arc2start, arc2end = None, None
    else:
        arc2start, arc2end = arcuatestartend(arcuate2['arcuate_length'], arcuate2['arcuate_axis'])

    #Round the arcuate lengths to the nearest integer
    arcuate1['arcuate_length'] = round(arcuate1['arcuate_length'])
    if arcuate2 != None:
        arcuate2['arcuate_length'] = round(arcuate2['arcuate_length'])

    #Send back the result of the calculations
    result = {
    'arcuate1': arcuate1,
    'arcuate2': arcuate2 if arcuate2 else "Not Applicable",
    'arc1start': arc1start,
    'arc1end': arc1end,
    'arc2start': arc2start,
    'arc2end': arc2end
    }
    print(f"Final result: {result}")
      #Set up variables which will show the arcuate parameters in string format
    arcuate1text = f"Arcuate 1: {arcuate1['arcuate_length']} degrees length at {arcuate1['arcuate_axis']}°"
    if arcuate2 == None:
        arcuate2text = f"Arcuate 2: Not Applicable"
    else:
        arcuate2text = f"Arcuate 2: {arcuate2['arcuate_length']} degrees length at {arcuate2['arcuate_axis']}°"
    print(arcuate1text)
    print(arcuate2text)

    return result

calculate()