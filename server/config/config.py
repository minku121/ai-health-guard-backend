import os

class Config:
    # Flask configuration
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000
    
    # CORS configuration
    CORS_ORIGINS = [
        'http://localhost:5173',  # Vite dev server
        'http://localhost:3000',  # Alternative dev port
        'https://your-frontend-domain.com'  # Production frontend domain
    ]
    
    # Base paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATASET_PATH = os.path.join(BASE_DIR, 'datasets')
    
    # Model paths
    NAIVE_BAYES_MODEL = os.path.join(DATASET_PATH, 'naive_bayes_model.pkl')
    LABEL_ENCODER = os.path.join(DATASET_PATH, 'label_encoder.pkl')
    PREGNANCY_MODEL = os.path.join(DATASET_PATH, 'pregnancy_model.pkl')
    HEART_MODEL = os.path.join(DATASET_PATH, 'heart_model.pkl')
    DIABETES_MODEL = os.path.join(DATASET_PATH, 'diabetes_model.pkl')
    
    # Dataset paths
    PRECAUTIONS_DF = os.path.join(DATASET_PATH, 'precautions.csv')
    WORKOUT_DF = os.path.join(DATASET_PATH, 'workout.csv')
    DESCRIPTION_DF = os.path.join(DATASET_PATH, 'description.csv')
    MEDICATIONS_DF = os.path.join(DATASET_PATH, 'medications.csv')
    DIETS_DF = os.path.join(DATASET_PATH, 'diets.csv')
    UNIQUE_SYMPTOMS_DF = os.path.join(DATASET_PATH, 'unique_symptoms.csv') 