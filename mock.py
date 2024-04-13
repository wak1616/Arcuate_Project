# mock.py

# Simulate data that would come from the request
data = {
    'age': 55,
    'corneal_astigmatism': 0.65,
    'steep_axis': 165,
    'eye': 'right'
}

age = int(data.get('age'))
eye = data.get('eye')
corneal_astigmatism = float(data.get('corneal_astigmatism'))
steep_axis = int(data.get('steep_axis'))

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
arcuate1 = {'arcuate_length': 0, 'arcuate_axis': steep_axis}
if 0 <= steep_axis < 180:
    arcuate2 = {'arcuate_length': 0, 'arcuate_axis': steep_axis + 180}
elif 180 <= steep_axis <= 360:
    arcuate2 = {'arcuate_length': 0, 'arcuate_axis': steep_axis - 180}

#Determine initial recomended incision length regardless of axis or age
if corneal_astigmatism < 0.3:
    print("error")
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
    print("error")

#define what against-the-rule astigmatism is (values correspondn to degrees)
ATR = [(0, 30), (150, 210), (330, 360)]
def is_ATR(degree):
    return any(start <= degree <= end for start, end in ATR)

#Increase total astigmatism length by 5 degrees if against-the-rule (ATR) asgtigmatism
if is_ATR(steep_axis) and arcuate2 is None:
    arcuate1['arcuate_length'] += 5
elif is_ATR(steep_axis):
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

result = {
    'arcuate1': arcuate1,
    'arcuate2': arcuate2  # This could also be conditionally modified or set to "Not Applicable"
}

# Print the result for inspection
print(result)