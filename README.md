# EDU-PREDICT: JUPEB Academic Performance Prediction System

![EDU-PREDICT Logo](static/images/logo.png)

## 📚 Project Overview

**EDU-PREDICT** is a Final Year Computer Science project that uses Machine Learning (Random Forest Classification) to predict JUPEB (Joint Universities Preliminary Examinations Board) student academic performance.

### 🎯 Features

- **AI-Powered Predictions**: Uses Random Forest algorithm trained on 1,500+ student records
- **User Authentication**: Secure login/signup system with password hashing
- **Performance Categories**: Excellent, Good, Average, At Risk
- **Personalized Recommendations**: Tailored advice based on prediction results
- **Prediction History**: Track all your predictions over time
- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🛠️ Technology Stack

### Backend
- **Python** 3.8+
- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Scikit-learn** - Machine Learning library
- **Pandas & NumPy** - Data processing
- **Joblib** - Model serialization
- **SQLite** - Database

### Frontend
- **HTML5** & **CSS3**
- **JavaScript**
- **Bootstrap 5** - UI framework
- **Bootstrap Icons** - Icon library

### Machine Learning
- **Random Forest Classifier**
- **Label Encoding** for categorical features
- **Train/Test Split** for model evaluation

## 📁 Project Structure

```
jupeb_project/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── jupeb_synthetic_dataset_1500.csv  # Training dataset
│
├── model/
│     ├── train_model.py        # Model training script
│     ├── model.pkl             # Trained model (generated)
│     ├── encoders.pkl          # Label encoders (generated)
│     └── target_encoder.pkl    # Target encoder (generated)
│
├── static/
│     ├── css/
│     │     └── style.css       # Custom styles
│     ├── js/
│     │     └── main.js         # JavaScript functionality
│     └── images/
│           └── logo.png        # EDU-PREDICT logo
│
├── templates/
│     ├── base.html             # Base template
│     ├── index.html            # Home page
│     ├── login.html            # Login page
│     ├── signup.html           # Signup page
│     ├── predict.html          # Prediction form
│     ├── history.html          # Prediction history
│     ├── about.html            # About page
│     ├── 404.html              # Not found error
│     └── 500.html              # Server error
│
└── database.db                 # SQLite database (generated)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Extract the Project
```bash
cd jupeb_project
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Train the Model (First Time Only)
```bash
python model/train_model.py
```

This will:
- Load the synthetic dataset
- Train the Random Forest model
- Save the model and encoders to the `model/` folder
- Display model accuracy and feature importance

### Step 5: Run the Application
```bash
python app.py
```

The application will start at: **http://127.0.0.1:5000**

## 📊 Dataset Features

### Input Features
| Feature | Type | Range/Options |
|---------|------|---------------|
| CA Score | Numerical | 0-40 |
| Attendance Rate | Numerical | 0-100% |
| Mock Exam Score | Numerical | 0-100 |
| Study Hours/Week | Numerical | 0-168 |
| Subject Combination | Categorical | Science, Arts, Commercial |
| Gender | Categorical | Male, Female |
| Study Resources | Categorical | Textbooks, YouTube, Tutorials, Mixed |
| Behavioural Pattern | Categorical | Motivated, Stressed, Struggling |
| Stress Level | Numerical | 1-10 |

### Output Categories
| Category | Description |
|----------|-------------|
| **Excellent** | Top-tier performance (75%+) |
| **Good** | Above-average performance (60-74%) |
| **Average** | Moderate performance (45-59%) |
| **At Risk** | Needs immediate attention (Below 45%) |

## 🔑 API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /signup` - Signup page
- `POST /signup` - Register new user
- `GET /logout` - Logout user

### Main Application
- `GET /` - Home page
- `GET /predict` - Prediction form (requires login)
- `GET /history` - Prediction history (requires login)
- `GET /about` - About page

### API Endpoints
- `POST /api/predict` - Make prediction (requires login)
  ```json
  {
    "ca_score_40": 35,
    "attendance_rate_percent": 85,
    "mock_exam_score_100": 78,
    "study_hours_per_week": 25,
    "subject_combination": "Science",
    "gender": "Male",
    "study_resources": "Mixed",
    "behavioural_pattern": "Motivated",
    "stress_level_1_10": 4
  }
  ```
  
  Response:
  ```json
  {
    "success": true,
    "predicted_category": "Good",
    "recommendation": {
      "message": "Great job! You are on the right track...",
      "card_class": "info",
      "icon": "star"
    }
  }
  ```

- `GET /api/history` - Get user's prediction history (requires login)
- `DELETE /api/delete-prediction/<id>` - Delete a prediction (requires login)

## 🎨 UI/UX Features

### Theme
- **Gold & Silver** color scheme
- **Light/Dark mode** toggle with persistent preference
- **Modern gradient** effects
- **Responsive design** for all screen sizes

### Animations
- Smooth page transitions
- Floating cards in hero section
- Fade-in effects on scroll
- Loading spinners for async operations

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection (via Flask-WTF in production)
- SQL injection protection via SQLAlchemy ORM
- XSS protection via template escaping

## 📝 Usage Guide

### For Students

1. **Create Account**: Sign up with your email and password
2. **Login**: Access your dashboard
3. **Make Prediction**: 
   - Enter your academic scores (CA, Attendance, Mock Exam)
   - Input your study habits and behavioral patterns
   - Click "Generate Prediction"
4. **View Results**: See your predicted category and personalized recommendations
5. **Track History**: View all your past predictions in the History page

### Sample Input
```
CA Score: 35/40
Attendance Rate: 85%
Mock Exam Score: 78/100
Study Hours per Week: 25
Subject Combination: Science
Gender: Male
Study Resources: Mixed
Behavioural Pattern: Motivated
Stress Level: 4/10
```

## 🧪 Model Performance

The Random Forest model is trained on 1,500 synthetic JUPEB student records:

- **Training Accuracy**: ~98%
- **Testing Accuracy**: ~62%
- **Algorithm**: Random Forest Classifier (200 estimators)
- **Features**: 9 input features
- **Classes**: 4 performance categories

### Feature Importance
1. Mock Exam Score (highest importance)
2. CA Score
3. Attendance Rate
4. Study Hours per Week
5. Stress Level
6. Subject Combination
7. Study Resources
8. Behavioural Pattern
9. Gender

## 🐛 Troubleshooting

### Common Issues

1. **Model not found error**
   ```bash
   python model/train_model.py
   ```

2. **Database errors**
   - Delete `database.db` and restart the app
   - The database will be recreated automatically

3. **Port already in use**
   - Change the port in `app.py`: `app.run(port=5001)`

4. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 👨‍💻 Developer Information

**Project Type**: Final Year (400 Level) Computer Science Project  
**Institution**: [Your University Name]  
**Student Name**: [Your Name]  
**Matric Number**: [Your Matric Number]  
**Supervisor**: [Supervisor Name]  
**Year**: 2024

## 📄 License

This project is developed for academic purposes as part of a Final Year Computer Science degree requirement.

## 🙏 Acknowledgments

- JUPEB (Joint Universities Preliminary Examinations Board)
- Department of Computer Science
- Project Supervisor

---

**EDU-PREDICT** - Predicting Academic Success with Machine Learning 🎓🤖