from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import pickle
import joblib
import warnings
import json

warnings.filterwarnings('ignore', category=UserWarning)

# Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

try:
    # Load datasets
    precautions = pd.read_csv("datasets/Symptoms-Disease Datasets/precautions_df.csv")
    workout = pd.read_csv("datasets/Symptoms-Disease Datasets/workout_df.csv")
    description = pd.read_csv("datasets/Symptoms-Disease Datasets/description.csv", encoding='latin-1')
    medications = pd.read_csv('datasets/Symptoms-Disease Datasets/medications.csv')
    diets = pd.read_csv("datasets/Symptoms-Disease Datasets/diets.csv")

    # Load the unique symptoms data
    unique_symptoms = pd.read_csv("datasets/Symptoms-Disease Datasets/unique_symptoms.csv")

    # Load models with error handling
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Load main disease prediction model
        with open('datasets/Symptoms-Disease Datasets/NaiveBayes.pkl', 'rb') as model_file:
            svc = pickle.load(model_file)

        # Load label encoder
        with open('datasets/Symptoms-Disease Datasets/label_encoder.pkl', 'rb') as le_file:
            le = pickle.load(le_file)

        # Load advanced models
        pregnancy_model = joblib.load("datasets/advance/models/pregnancy_model.pkl")
        heart_model = pickle.load(open("datasets/advance/models/Heart.sav", 'rb'))
        diabetic_model = pickle.load(open("datasets/advance/models/Diabetes.sav", 'rb'))

except Exception as e:
    print(f"Error loading models or data: {str(e)}")
    raise

# Normalize column names and data to handle inconsistencies
workout.rename(columns={'disease': 'Disease'}, inplace=True)

def normalize_column(df, column_name):
    df[column_name] = df[column_name].str.strip().str.lower()

for df in [description, precautions, medications, workout, diets]:
    normalize_column(df, 'Disease')

# Function to predict disease based on symptoms
def predict_disease(symptoms):
    symptoms_dict = {symptom: 0 for symptom in svc.feature_names_in_}
    for symptom in symptoms:
        symptom = symptom.strip().lower()
        if symptom in symptoms_dict:
            symptoms_dict[symptom] = 1
    
    input_data = pd.DataFrame([symptoms_dict])
    predicted_disease = svc.predict(input_data)
    disease_name = le.inverse_transform(predicted_disease)[0].strip().lower()
    
    return disease_name

# Helper function to fetch recommendations
def helper(disease):
    # Initialize variables to store recommendations
    desc = 'No description available'
    pre = ['No precautions available']
    med = ['No medications available']
    die = ['No diet information available']
    wrkout = ['No workout information available']

    # Fetch description if disease exists in description dataset
    if disease in description['Disease'].values:
        desc = description[description['Disease'] == disease]['Description'].values[0]

    # Fetch precautions if disease exists in precautions dataset
    if disease in precautions['Disease'].values:
        pre = []
        precaution_columns = [col for col in precautions.columns if 'Precaution_' in col]
        precautions_list = precautions[precautions['Disease'] == disease][precaution_columns].values[0]
        for precaution in precautions_list:
            if pd.notna(precaution):
                pre.append(precaution)

    # Fetch medications if disease exists in medications dataset
    if disease in medications['Disease'].values:
        med = []
        medication_columns = [col for col in medications.columns if 'Medication_' in col]
        medications_list = medications[medications['Disease'] == disease][medication_columns].values[0]
        for medication in medications_list:
            if pd.notna(medication):
                med.append(medication)

    # Fetch diets if disease exists in diets dataset
    if disease in diets['Disease'].values:
        diet_columns = [col for col in diets.columns if 'Diet_' in col]
        diets_list = diets[diets['Disease'] == disease][diet_columns].values[0]
        die = []
        for diet in diets_list:
            if pd.notna(diet):
                die.append(diet)

    # Fetch workouts if disease exists in workout dataset
    if disease in workout['Disease'].values:
        workout_columns = [col for col in workout.columns if 'workout_' in col]
        workouts_list = workout[workout['Disease'] == disease][workout_columns].values[0]
        wrkout = []
        for workout_item in workouts_list:
            if pd.notna(workout_item):
                wrkout.append(workout_item)

    return desc, pre, med, die, wrkout

# API Routes
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to AI Health Guard API",
        "version": "1.0",
        "endpoints": {
            "/api/symptoms": "GET - Get list of all symptoms",
            "/api/analyze": "POST - Analyze symptoms and get disease prediction",
            "/api/pregnancy": "POST - Get pregnancy risk assessment",
            "/api/heart": "POST - Get heart disease prediction",
            "/api/diabetes": "POST - Get diabetes prediction"
        }
    })

@app.route("/api/symptoms")
def get_symptoms():
    symptoms_list = unique_symptoms['symptom'].tolist()
    return jsonify(symptoms_list)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    
    disease = predict_disease(symptoms)
    desc, pre, med, die, wrkout = helper(disease)
    
    result = {
        'disease': disease.capitalize(),
        'description': desc,
        'precautions': list(pre),
        'medications': med,
        'diet': die,
        'workout': wrkout
    }
    
    return jsonify(result)

@app.route('/api/pregnancy', methods=['POST'])
def pregnancy():
    data = request.json
    age = data['age']
    diastolicBP = data['diastolicBP']
    BS = data['BS']
    bodyTemp = data['bodyTemp']
    heartRate = data['heartRate']

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        predicted_risk = pregnancy_model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])

    if predicted_risk[0] == 0:
        risk_level = "Low Risk"
        color = "#29cb15"
    elif predicted_risk[0] == 1:
        risk_level = "Medium Risk"
        color = "#FF7518"
    else:
        risk_level = "High Risk"
        color = "red"

    return jsonify({
        'risk_level': risk_level,
        'color': color
    })

@app.route('/api/heart', methods=['POST'])
def heart():
    try:
        data = request.json
        
        # Input validation
        required_fields = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                         'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Validate numeric ranges
        if not (20 <= float(data['age']) <= 80):
            return jsonify({'error': 'Age must be between 20 and 80'}), 400
        if not (90 <= float(data['trestbps']) <= 200):
            return jsonify({'error': 'Resting blood pressure must be between 90 and 200'}), 400
        if not (120 <= float(data['chol']) <= 570):
            return jsonify({'error': 'Cholesterol must be between 120 and 570'}), 400
        if not (60 <= float(data['thalach']) <= 220):
            return jsonify({'error': 'Maximum heart rate must be between 60 and 220'}), 400
        if not (0 <= float(data['oldpeak']) <= 6.2):
            return jsonify({'error': 'ST depression must be between 0 and 6.2'}), 400
        if not (1 <= float(data['slope']) <= 3):
            return jsonify({'error': 'Slope must be between 1 and 3'}), 400
        if not (0 <= float(data['ca']) <= 3):
            return jsonify({'error': 'Number of major vessels must be between 0 and 3'}), 400

        # Convert string inputs to appropriate types
        try:
            age = float(data['age'])
            trestbps = float(data['trestbps'])
            chol = float(data['chol'])
            restecg = float(data['restecg'])
            thalach = float(data['thalach'])
            oldpeak = float(data['oldpeak'])
            slope = float(data['slope'])
            ca = float(data['ca'])
        except ValueError as e:
            return jsonify({'error': 'Invalid numeric value provided'}), 400

        # Mapping dictionaries
        sex_dict = {'Male': 0, 'Female': 1}
        cp_dict = {
            'Low pain': 0,      # Typical Angina
            'Mild pain': 1,     # Atypical Angina
            'Moderate pain': 2, # Non-anginal Pain
            'Extreme pain': 3   # Asymptomatic
        }
        fbs_dict = {'Yes': 1, 'No': 0}
        exang_dict = {'Yes': 1, 'No': 0}
        thal_dict = {
            'Normal': 0,                # Normal
            'Fixed': 1,                 # Fixed Defect
            'Reversible': 2,           # Reversible Defect
            'Serious': 3               # Serious Defect
        }

        # Extract thal value from the full string
        thal_value = data['thal'].split()[0]  # Get first word (e.g., "Normal" from "Normal (No Thalassemia)")
        
        if thal_value not in thal_dict:
            return jsonify({'error': f'Invalid thalassemia value. Must be one of: {", ".join(thal_dict.keys())}'}), 400

        # Prepare input data
        input_data = [
            age,
            sex_dict[data['sex']],
            cp_dict[data['cp']],
            trestbps,
            chol,
            fbs_dict[data['fbs']],
            restecg,
            thalach,
            exang_dict[data['exang']],
            oldpeak,
            slope,
            ca,
            thal_dict[thal_value]
        ]

        # Make prediction
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            heart_prediction = heart_model.predict([input_data])
        
        # Prepare response
        if heart_prediction[0] == 1:
            prediction_text = 'High Risk: Likely to have heart disease'
            color = "#FF0000"  # Red
        else:
            prediction_text = 'Low Risk: Less likely to have heart disease'
            color = "#29cb15"  # Green

        return jsonify({
            'prediction_text': prediction_text,
            'color': color
        })

    except KeyError as e:
        return jsonify({'error': f'Invalid value for field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diabetes', methods=['POST'])
def diabetes():
    data = request.json
    input_data = [
        data['Pregnancies'],
        data['Glucose'],
        data['BloodPressure'],
        data['SkinThickness'],
        data['Insulin'],
        data['BMI'],
        data['DiabetesPedigreeFunction'],
        data['Age']
    ]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        prediction = diabetic_model.predict([input_data])

    if prediction[0] == 1:
        prediction_text = 'The person is diabetic'
        color = "red"
    else:
        prediction_text = 'The person is not diabetic'
        color = "#29cb15"

    return jsonify({
        'prediction_text': prediction_text,
        'color': color
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)