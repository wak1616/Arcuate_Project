import math
import pandas as pd
import numpy as np
import xgboost as xgb


def calculate_single_arcuate_sweep(age, eye, sex, WTW, Mean_K, cassini_corneal_astigmatism, iolmaster700_corneal_astigmatism, steep_axis):
    # Load model
    model = xgb.Booster()
    model.load_model("model_full_ver6.json")

    # Define a single entry in a dataframe
    single_entry = pd.DataFrame({
    'Age': [age],
    'TCA_Cassini_Astigmatism_Component_Half': [cassini_corneal_astigmatism/2],
    'Sex': pd.Categorical([sex]),
    'Eye': pd.Categorical([eye]),
    'WTW_IOLMaster': [WTW],
    'MeanK_IOLMaster': [Mean_K],
    'Steep_Axis': [steep_axis],
    'TK_IOLMaster_Astigmatism_Component_Half': [iolmaster700_corneal_astigmatism/2],
    'Residual_Astigmatism': [0]   # Residual astigmatism is set to zero because that is our goal
    })

    # Define features and order of features to input into the model
    features = ['Age', 'Eye', 'Sex', 'WTW_IOLMaster', 'MeanK_IOLMaster', 'TK_IOLMaster_Astigmatism_Component_Half', 'TCA_Cassini_Astigmatism_Component_Half', 'Residual_Astigmatism']
    
    # Create a new dataframe with the features in the correct order
    Xnew = single_entry[features]

    # Convert single_entry to a dmatrix
    dnew= xgb.DMatrix(data=Xnew, enable_categorical=True)

    # Predict the arcuate astigmatism
    Predicted_Arcuate_Sweep_Single= np.round(model.predict(dnew))
    Predicted_Arcuate_Sweep_Single = np.maximum(Predicted_Arcuate_Sweep_Single, 0)

    return(Predicted_Arcuate_Sweep_Single).item()


def arcuatestartend(sweep, location):
    # Flip arcuate central location by 180 degrees to fit CANVAS angle plot (where zero is located at 3 o clock and axis spins clockwise)
    location = 360 if location == 0 else 360 - location

    # Calculate start and end angles in degrees
    arcstart_deg = (location - sweep / 2) % 360
    arcend_deg = (location + sweep / 2) % 360
    
    # Convert to radians
    arcstart = math.radians(arcstart_deg)
    arcend = math.radians(arcend_deg)

    return (arcstart, arcend)
