import pandas as pd
from ..config.config import Config

class DataLoader:
    def __init__(self):
        # Load datasets
        self.precautions = pd.read_csv(Config.PRECAUTIONS_DF)
        self.workout = pd.read_csv(Config.WORKOUT_DF)
        self.description = pd.read_csv(Config.DESCRIPTION_DF, encoding='latin-1')
        self.medications = pd.read_csv(Config.MEDICATIONS_DF)
        self.diets = pd.read_csv(Config.DIETS_DF)
        self.unique_symptoms = pd.read_csv(Config.UNIQUE_SYMPTOMS_DF)
        
        # Normalize column names and data
        self.workout.rename(columns={'disease': 'Disease'}, inplace=True)
        self._normalize_columns()
    
    def _normalize_columns(self):
        for df in [self.description, self.precautions, self.medications, self.workout, self.diets]:
            df['Disease'] = df['Disease'].str.strip().str.lower()
    
    def get_symptoms_list(self):
        return self.unique_symptoms['symptom'].tolist()
    
    def get_disease_info(self, disease):
        # Initialize variables
        desc = 'No description available'
        pre = ['No precautions available']
        med = ['No medications available']
        die = ['No diet information available']
        wrkout = ['No workout information available']

        # Get description
        if disease in self.description['Disease'].values:
            desc = self.description[self.description['Disease'] == disease]['Description'].values[0]

        # Get precautions
        if disease in self.precautions['Disease'].values:
            pre = []
            precaution_columns = [col for col in self.precautions.columns if 'Precaution_' in col]
            precautions_list = self.precautions[self.precautions['Disease'] == disease][precaution_columns].values[0]
            for precaution in precautions_list:
                if pd.notna(precaution):
                    pre.append(precaution)

        # Get medications
        if disease in self.medications['Disease'].values:
            med = []
            medication_columns = [col for col in self.medications.columns if 'Medication_' in col]
            medications_list = self.medications[self.medications['Disease'] == disease][medication_columns].values[0]
            for medication in medications_list:
                if pd.notna(medication):
                    med.append(medication)

        # Get diets
        if disease in self.diets['Disease'].values:
            diet_columns = [col for col in self.diets.columns if 'Diet_' in col]
            diets_list = self.diets[self.diets['Disease'] == disease][diet_columns].values[0]
            die = []
            for diet in diets_list:
                if pd.notna(diet):
                    die.append(diet)

        # Get workouts
        if disease in self.workout['Disease'].values:
            workout_columns = [col for col in self.workout.columns if 'workout_' in col]
            workouts_list = self.workout[self.workout['Disease'] == disease][workout_columns].values[0]
            wrkout = []
            for workout_item in workouts_list:
                if pd.notna(workout_item):
                    wrkout.append(workout_item)

        return desc, pre, med, die, wrkout 