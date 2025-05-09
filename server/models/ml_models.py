import pickle
import joblib
import pandas as pd
import warnings
from ..config.config import Config

class MLModels:
    def __init__(self):
        # Load main disease prediction model
        with open(Config.NAIVE_BAYES_MODEL, 'rb') as model_file:
            self.svc = pickle.load(model_file)
        
        # Load label encoder
        with open(Config.LABEL_ENCODER, 'rb') as le_file:
            self.le = pickle.load(le_file)
        
        # Load advanced models
        self.pregnancy_model = joblib.load(open(Config.PREGNANCY_MODEL, 'rb'))
        self.heart_model = pickle.load(open(Config.HEART_MODEL, 'rb'))
        self.diabetic_model = pickle.load(open(Config.DIABETES_MODEL, 'rb'))
    
    def predict_disease(self, symptoms):
        symptoms_dict = {symptom: 0 for symptom in self.svc.feature_names_in_}
        for symptom in symptoms:
            symptom = symptom.strip().lower()
            if symptom in symptoms_dict:
                symptoms_dict[symptom] = 1
        
        input_data = pd.DataFrame([symptoms_dict])
        predicted_disease = self.svc.predict(input_data)
        disease_name = self.le.inverse_transform(predicted_disease)[0].strip().lower()
        
        return disease_name
    
    def predict_pregnancy_risk(self, age, diastolicBP, BS, bodyTemp, heartRate):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            predicted_risk = self.pregnancy_model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])
        
        if predicted_risk[0] == 0:
            return "Low Risk", "#29cb15"
        elif predicted_risk[0] == 1:
            return "Medium Risk", "#FF7518"
        else:
            return "High Risk", "red"
    
    def predict_heart_disease(self, input_data):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            heart_prediction = self.heart_model.predict([input_data])
        
        if heart_prediction[0] == 1:
            return "The person is having heart disease", "red"
        else:
            return "The person does not have any heart disease", "#29cb15"
    
    def predict_diabetes(self, input_data):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            prediction = self.diabetic_model.predict([input_data])
        
        if prediction[0] == 1:
            return "The person is diabetic", "red"
        else:
            return "The person is not diabetic", "#29cb15" 