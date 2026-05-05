"""
EDU-PREDICT: JUPEB Academic Performance Prediction System
Main Flask Application

A final year Computer Science project for predicting JUPEB student
performance using Machine Learning (Random Forest Classification).
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'edu-predict-jupeb-2024-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# ============================================
# DATABASE MODELS
# ============================================

class User(db.Model):
    """User model for student authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with predictions
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify user password."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Prediction(db.Model):
    """Prediction history model."""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Input features
    ca_score_40 = db.Column(db.Integer, nullable=False)
    attendance_rate_percent = db.Column(db.Integer, nullable=False)
    mock_exam_score_100 = db.Column(db.Integer, nullable=False)
    study_hours_per_week = db.Column(db.Integer, nullable=False)
    subject_combination = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    study_resources = db.Column(db.String(50), nullable=False)
    behavioural_pattern = db.Column(db.String(50), nullable=False)
    stress_level_1_10 = db.Column(db.Integer, nullable=False)
    
    # Prediction result
    predicted_category = db.Column(db.String(50), nullable=False)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ca_score_40': self.ca_score_40,
            'attendance_rate_percent': self.attendance_rate_percent,
            'mock_exam_score_100': self.mock_exam_score_100,
            'study_hours_per_week': self.study_hours_per_week,
            'subject_combination': self.subject_combination,
            'gender': self.gender,
            'study_resources': self.study_resources,
            'behavioural_pattern': self.behavioural_pattern,
            'stress_level_1_10': self.stress_level_1_10,
            'predicted_category': self.predicted_category,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


# ============================================
# MACHINE LEARNING MODEL LOADING
# ============================================

# Global variables for ML model and encoders
model = None
label_encoders = None
target_encoder = None

def load_model():
    """Load the trained Random Forest model and encoders."""
    global model, label_encoders, target_encoder
    
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')
    encoders_path = os.path.join(os.path.dirname(__file__), 'model', 'encoders.pkl')
    target_encoder_path = os.path.join(os.path.dirname(__file__), 'model', 'target_encoder.pkl')
    
    try:
        model = joblib.load(model_path)
        label_encoders = joblib.load(encoders_path)
        target_encoder = joblib.load(target_encoder_path)
        print("[✓] Machine Learning model loaded successfully!")
        print(f"[✓] Model expects features in order: {model.feature_names_in_}")
    except Exception as e:
        print(f"[!] Error loading model: {e}")
        print("[!] Please run model/train_model.py first to train the model.")


# ============================================
# AUTHENTICATION DECORATORS
# ============================================

def login_required(f):
    """Decorator to require login for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_recommendation(category):
    """
    Get recommendation message based on predicted performance category.
    
    Args:
        category: Predicted performance category (Excellent, Good, Average, At Risk)
    
    Returns:
        Dictionary with message and card class
    """
    recommendations = {
        'Excellent': {
            'message': 'Outstanding performance! Keep maintaining your excellent study habits. '
                      'Your dedication and consistency are paying off. Consider mentoring '
                      'fellow students to reinforce your knowledge.',
            'short_message': 'Keep up the excellent work!',
            'card_class': 'success',
            'icon': 'trophy',
            'color': '#28a745'
        },
        'Good': {
            'message': 'Great job! You are on the right track. With a little more effort '
                      'on time management and consistent revision, you can reach the '
                      'Excellent category. Stay focused!',
            'short_message': 'Good progress! Keep pushing forward.',
            'card_class': 'info',
            'icon': 'star',
            'color': '#17a2b8'
        },
        'Average': {
            'message': 'You have potential but need to improve your study strategies. '
                      'Consider increasing study hours, attending more classes, and '
                      'seeking help from tutors. Small changes can make a big difference!',
            'short_message': 'Room for improvement. Stay committed!',
            'card_class': 'warning',
            'icon': 'exclamation-circle',
            'color': '#ffc107'
        },
        'At Risk': {
            'message': 'Immediate attention needed! Please consult with your academic '
                      'advisor and teachers. Consider joining study groups, reducing '
                      'stress levels, and creating a structured study plan. '
                      'It is never too late to turn things around!',
            'short_message': 'Action required! Seek help immediately.',
            'card_class': 'danger',
            'icon': 'exclamation-triangle',
            'color': '#dc3545'
        }
    }
    
    return recommendations.get(category, recommendations['Average'])


def make_prediction(data):
    """
    Make prediction using the trained Random Forest model.
    
    Args:
        data: Dictionary containing student features
    
    Returns:
        Predicted category string
    """
    # Create DataFrame with single row
    df = pd.DataFrame([data])
    
    # Encode categorical features
    for feature, encoder in label_encoders.items():
        if feature in df.columns:
            # Handle unseen categories
            try:
                df[feature] = encoder.transform(df[feature])
            except ValueError:
                # If category not seen during training, use most frequent
                df[feature] = 0
    
    # Ensure correct feature order
    feature_order =  [
    'ca_score_40',
    'attendance_rate_percent',
    'mock_exam_score_100',
    'study_hours_per_week',
    'stress_level_1_10',   # ✅ moved here
    'subject_combination',
    'gender',
    'study_resources',
    'behavioural_pattern'
]
    
    X = df[feature_order]
    
    # Make prediction
    prediction_encoded = model.predict(X)[0]
    prediction_category = target_encoder.inverse_transform([prediction_encoded])[0]
    
    return prediction_category


# ============================================
# ROUTES - AUTHENTICATION
# ============================================

@app.route('/')
def index():
    """Home page route."""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validate input
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return redirect(url_for('login'))
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            # Login successful
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            session['user_email'] = user.email
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('predict'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration route."""
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validate input
        if not full_name or not email or not password:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))
        
        # Create new user
        new_user = User(full_name=full_name, email=email)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('signup'))
    
    return render_template('signup.html')


@app.route('/logout')
def logout():
    """User logout route."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ============================================
# ROUTES - MAIN APPLICATION
# ============================================

@app.route('/predict')
@login_required
def predict():
    """Prediction form page."""
    return render_template('predict.html')


@app.route('/history')
@login_required
def history():
    """Prediction history page."""
    user_predictions = Prediction.query.filter_by(user_id=session['user_id'])\
                                       .order_by(Prediction.created_at.desc()).all()
    return render_template('history.html', predictions=user_predictions)


@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')


# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/predict', methods=['POST'])
@login_required
def api_predict():
    """
    API endpoint for making predictions.
    
    Expected JSON payload:
    {
        "ca_score_40": int (0-40),
        "attendance_rate_percent": int (0-100),
        "mock_exam_score_100": int (0-100),
        "study_hours_per_week": int,
        "subject_combination": str ("Science", "Arts", "Commercial"),
        "gender": str ("Male", "Female"),
        "study_resources": str ("Textbooks", "YouTube", "Tutorials", "Mixed"),
        "behavioural_pattern": str ("Motivated", "Stressed", "Struggling"),
        "stress_level_1_10": int (1-10)
    }
    
    Returns:
    {
        "success": true,
        "predicted_category": "Good",
        "recommendation": {...}
    }
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = [
            'ca_score_40', 'attendance_rate_percent', 'mock_exam_score_100',
            'study_hours_per_week', 'subject_combination', 'gender',
            'study_resources', 'behavioural_pattern', 'stress_level_1_10'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate ranges
        if not (0 <= int(data['ca_score_40']) <= 40):
            return jsonify({'success': False, 'error': 'CA Score must be between 0 and 40'}), 400
        
        if not (0 <= int(data['attendance_rate_percent']) <= 100):
            return jsonify({'success': False, 'error': 'Attendance Rate must be between 0 and 100'}), 400
        
        if not (0 <= int(data['mock_exam_score_100']) <= 100):
            return jsonify({'success': False, 'error': 'Mock Exam Score must be between 0 and 100'}), 400
        
        if not (1 <= int(data['stress_level_1_10']) <= 10):
            return jsonify({'success': False, 'error': 'Stress Level must be between 1 and 10'}), 400
        
        # Prepare data for prediction
        prediction_data = {
            'ca_score_40': int(data['ca_score_40']),
            'attendance_rate_percent': int(data['attendance_rate_percent']),
            'mock_exam_score_100': int(data['mock_exam_score_100']),
            'study_hours_per_week': int(data['study_hours_per_week']),
            'subject_combination': data['subject_combination'],
            'gender': data['gender'],
            'study_resources': data['study_resources'],
            'behavioural_pattern': data['behavioural_pattern'],
            'stress_level_1_10': int(data['stress_level_1_10'])
        }
        
        # Make prediction
        predicted_category = make_prediction(prediction_data)
        
        # Get recommendation
        recommendation = get_recommendation(predicted_category)
        
        # Save prediction to database
        new_prediction = Prediction(
            user_id=session['user_id'],
            **prediction_data,
            predicted_category=predicted_category
        )
        
        db.session.add(new_prediction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'predicted_category': predicted_category,
            'recommendation': recommendation
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
@login_required
def api_history():
    """API endpoint to get user's prediction history."""
    try:
        predictions = Prediction.query.filter_by(user_id=session['user_id'])\
                                      .order_by(Prediction.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'predictions': [p.to_dict() for p in predictions]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/delete-prediction/<int:prediction_id>', methods=['DELETE'])
@login_required
def delete_prediction(prediction_id):
    """API endpoint to delete a prediction record."""
    try:
        prediction = Prediction.query.filter_by(id=prediction_id, user_id=session['user_id']).first()
        
        if not prediction:
            return jsonify({
                'success': False,
                'error': 'Prediction not found'
            }), 404
        
        db.session.delete(prediction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prediction deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    if request.is_json:
        return jsonify({'success': False, 'error': 'Not found'}), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    if request.is_json:
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    return render_template('500.html'), 500


# ============================================
# CONTEXT PROCESSORS
# ============================================

@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    return {
        'app_name': 'EDU-PREDICT',
        'app_full_name': 'JUPEB Academic Performance Prediction System',
        'current_year': datetime.now().year
    }


# ============================================
# APPLICATION INITIALIZATION
# ============================================

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        print("[✓] Database tables created successfully!")
    
    # Load ML model
    load_model()
    
    # Run the application
    print("\n" + "=" * 60)
    print("EDU-PREDICT Server Starting...")
    print("=" * 60)
    print("Access the application at: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)