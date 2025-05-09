from flask import Blueprint, request, jsonify
from ..models.ml_models import MLModels
from ..utils.data_loader import DataLoader

# Initialize models and data loader
ml_models = MLModels()
data_loader = DataLoader()

# Create blueprint
api = Blueprint('api', __name__)

@api.route("/symptoms")
def get_symptoms():
    symptoms_list = data_loader.get_symptoms_list()
    return jsonify(symptoms_list)

@api.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    
    disease = ml_models.predict_disease(symptoms)
    desc, pre, med, die, wrkout = data_loader.get_disease_info(disease)
    
    result = {
        'disease': disease.capitalize(),
        'description': desc,
        'precautions': list(pre),
        'medications': med,
        'diet': die,
        'workout': wrkout
    }
    
    return jsonify(result)

@api.route('/pregnancy', methods=['POST'])
def pregnancy():
    data = request.json
    age = data['age']
    diastolicBP = data['diastolicBP']
    BS = data['BS']
    bodyTemp = data['bodyTemp']
    heartRate = data['heartRate']

    risk_level, color = ml_models.predict_pregnancy_risk(age, diastolicBP, BS, bodyTemp, heartRate)
    return jsonify({
        'risk_level': risk_level,
        'color': color
    })

@api.route('/heart', methods=['POST'])
def heart():
    data = request.json
    sex_dict = {'Male': 0, 'Female': 1}
    cp_dict = {'Low pain': 0, 'Mild pain': 1, 'Moderate pain': 2, 'Extreme pain': 3}
    fbs_dict = {'Yes': 1, 'No': 0}
    exang_dict = {'Yes': 1, 'No': 0}
    thal_dict = {
        'Normal (No Thalassemia)': 0,
        'Fixed Defect (Beta-thalassemia minor)': 1,
        'Reversible Defect (Beta-thalassemia intermedia)': 2,
        'Serious Defect (Beta-thalassemia major)': 3
    }

    input_data = [
        data['age'],
        sex_dict[data['sex']],
        cp_dict[data['cp']],
        data['trestbps'],
        data['chol'],
        fbs_dict[data['fbs']],
        data['restecg'],
        data['thalach'],
        exang_dict[data['exang']],
        data['oldpeak'],
        data['slope'],
        data['ca'],
        thal_dict[data['thal']]
    ]

    prediction_text, color = ml_models.predict_heart_disease(input_data)
    return jsonify({
        'prediction_text': prediction_text,
        'color': color
    })

@api.route('/diabetes', methods=['POST'])
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

    prediction_text, color = ml_models.predict_diabetes(input_data)
    return jsonify({
        'prediction_text': prediction_text,
        'color': color
    }) 