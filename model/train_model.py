"""
JUPEB Academic Performance Prediction Model Training Script
This script trains a Random Forest classifier to predict student performance categories.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train_model():
    """
    Train the Random Forest model on JUPEB dataset.
    Returns the trained model, label encoders, and accuracy score.
    """
    print("=" * 60)
    print("EDU-PREDICT: JUPEB Performance Prediction Model Training")
    print("=" * 60)
    
    # Load dataset
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                'jupeb_synthetic_dataset_1500.csv')
    print(f"\n[1/6] Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"      Dataset loaded: {len(df)} samples")
    
    # Define feature columns
    categorical_features = [
        'subject_combination',
        'gender',
        'study_resources',
        'behavioural_pattern'
    ]
    
    numerical_features = [
        'ca_score_40',
        'attendance_rate_percent',
        'mock_exam_score_100',
        'study_hours_per_week',
        'stress_level_1_10'
    ]
    
    # Initialize label encoders dictionary
    label_encoders = {}
    
    # Create a copy of dataframe for processing
    df_processed = df.copy()
    
    print("\n[2/6] Encoding categorical features...")
    # Encode categorical features
    for feature in categorical_features:
        le = LabelEncoder()
        df_processed[feature] = le.fit_transform(df_processed[feature])
        label_encoders[feature] = le
        print(f"      - {feature}: {list(le.classes_)}")
    
    # Encode target variable
    print("\n[3/6] Encoding target variable...")
    target_encoder = LabelEncoder()
    df_processed['performance_category_encoded'] = target_encoder.fit_transform(
        df_processed['performance_category']
    )
    print(f"      Categories: {list(target_encoder.classes_)}")
    
    # Prepare features and target
    X = df_processed[numerical_features + categorical_features]
    y = df_processed['performance_category_encoded']
    
    print("\n[4/6] Splitting dataset (80% train, 20% test)...")
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"      Training samples: {len(X_train)}")
    print(f"      Testing samples: {len(X_test)}")
    
    print("\n[5/6] Training Random Forest Classifier...")
    # Initialize and train Random Forest model
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    # Train the model
    rf_model.fit(X_train, y_train)
    
    # Evaluate model
    train_accuracy = rf_model.score(X_train, y_train)
    test_accuracy = rf_model.score(X_test, y_test)
    
    print(f"      Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    print(f"      Testing Accuracy:  {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Feature importance
    print("\n[6/6] Feature Importance:")
    feature_importance = pd.DataFrame({
        'feature': numerical_features + categorical_features,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for _, row in feature_importance.iterrows():
        print(f"      - {row['feature']}: {row['importance']:.4f}")
    
    # Save model and encoders
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    encoders_path = os.path.join(os.path.dirname(__file__), 'encoders.pkl')
    target_encoder_path = os.path.join(os.path.dirname(__file__), 'target_encoder.pkl')
    
    joblib.dump(rf_model, model_path)
    joblib.dump(label_encoders, encoders_path)
    joblib.dump(target_encoder, target_encoder_path)
    
    print(f"\n{'=' * 60}")
    print("Model Training Complete!")
    print(f"{'=' * 60}")
    print(f"Model saved to: {model_path}")
    print(f"Encoders saved to: {encoders_path}")
    print(f"Target encoder saved to: {target_encoder_path}")
    
    return rf_model, label_encoders, target_encoder, test_accuracy


if __name__ == "__main__":
    train_model()