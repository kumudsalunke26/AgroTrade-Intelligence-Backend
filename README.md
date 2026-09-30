# 🌾 AgroTrade Intelligence — Backend

This repository contains the **machine learning and REST API backend** for AgroTrade Intelligence, an agricultural market intelligence platform designed to provide crop price predictions and support data-driven agricultural analysis.

The backend uses **Python, Flask, and CatBoostRegressor** to process agricultural inputs and generate machine learning predictions that are consumed by the React frontend.

## 🌐 Live Deployment

**Backend API:**
https://agrotrade-intelligence-backend.onrender.com

**Frontend Application:**
https://agrotrade-frontend.vercel.app/

---

## 📌 Project Overview

AgroTrade Intelligence combines machine learning with a web-based interface to provide agricultural market insights.

The backend serves as the computational layer of the platform.

It is responsible for:

* Agricultural data preprocessing
* Feature engineering
* Machine learning model development
* Model evaluation
* Model serialization
* API request handling
* Crop price prediction
* Returning prediction results to the frontend

---

## 🧠 Machine Learning

### Model Used

**CatBoostRegressor**

CatBoostRegressor is a gradient boosting regression algorithm used to learn relationships between agricultural input features and crop prices.

It was selected as the primary regression model for the crop price prediction component.

---

## 📊 Dataset

The project uses a cleaned agricultural dataset containing **6,300+ records**.

The data preparation workflow includes:

* Data cleaning
* Handling unsuitable records
* Outlier removal
* Feature engineering
* Model-ready feature preparation

---

## 📈 Model Performance

The model was evaluated using training and testing data.

| Evaluation       |                Result |
| ---------------- | --------------------: |
| Dataset Size     |    **6,300+ records** |
| Model            | **CatBoostRegressor** |
| Training R²      |              **0.91** |
| Testing R²       |              **0.87** |
| Cross-Validation |            **5-Fold** |

The testing R² of **0.87** represents the model's performance on the held-out testing data.

---

## 🔬 Machine Learning Pipeline

```text
                    Agricultural Dataset
                            │
                            ▼
                    Data Cleaning
                            │
                            ▼
                    Outlier Removal
                            │
                            ▼
                    Feature Engineering
                            │
                            ▼
                     Data Preparation
                            │
                            ▼
                  5-Fold Cross-Validation
                            │
                            ▼
                    CatBoostRegressor
                            │
                            ▼
                    Model Evaluation
                            │
                            ▼
                    Trained ML Model
                            │
                            ▼
                  Model Serialization
                            │
                            ▼
                       Flask API
```

---

## 🏗️ Backend Architecture

```text
                    React Frontend
                          │
                          │ HTTP Request
                          ▼
                  ┌─────────────────┐
                  │    Flask API    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Input Processing│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ CatBoost Model  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Crop Prediction │
                  └────────┬────────┘
                           │
                           ▼
                    JSON Response
                           │
                           ▼
                    React Frontend
```

---

## 🛠️ Technology Stack

| Technology           | Purpose                     |
| -------------------- | --------------------------- |
| **Python**           | Backend and ML development  |
| **Flask**            | REST API                    |
| **CatBoost**         | Machine learning regression |
| **Pandas**           | Data manipulation           |
| **NumPy**            | Numerical computation       |
| **Scikit-learn**     | Validation and evaluation   |
| **Jupyter Notebook** | Model development           |
| **Pickle**           | Model serialization         |
| **Render**           | Backend deployment          |

---

## 📂 Project Structure

```text
AgroTrade-Intelligence-Backend/
│
├── app.py
├── clean_agri_dataset.csv
├── clean_agri_model_new.pkl
├── newagri.ipynb
├── requirements.txt
├── runtime.txt
├── catboost_info/
│
├── .gitignore
└── README.md
```

### Important Files

| File                       | Description                           |
| -------------------------- | ------------------------------------- |
| `app.py`                   | Flask API application                 |
| `clean_agri_dataset.csv`   | Cleaned agricultural dataset          |
| `clean_agri_model_new.pkl` | Serialized trained CatBoost model     |
| `newagri.ipynb`            | Machine learning development notebook |
| `requirements.txt`         | Python dependencies                   |
| `runtime.txt`              | Deployment runtime configuration      |

---

## ⚙️ Getting Started

### Prerequisites

Make sure the following are installed:

* Python 3.x
* pip
* Git

### 1. Clone the repository

```bash
git clone https://github.com/kumudsalunke26/AgroTrade-Intelligence-Backend.git
```

### 2. Navigate to the project directory

```bash
cd AgroTrade-Intelligence-Backend
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Flask application

```bash
python app.py
```

The Flask API will start on the configured local host and port.

---

## 🔄 API Prediction Workflow

```text
User
 │
 ▼
React Frontend
 │
 │ Prediction Request
 ▼
Flask REST API
 │
 ▼
Input Validation / Processing
 │
 ▼
CatBoostRegressor
 │
 ▼
Crop Price Prediction
 │
 ▼
JSON Response
 │
 ▼
React Dashboard
```

---

## 💾 Model Serialization

After model training, the trained model is serialized and stored as:

```text
clean_agri_model_new.pkl
```

The Flask application loads this model during inference and uses it to generate predictions without retraining the model for every API request.

---

## ☁️ Deployment

The backend is deployed using **Render**.

### Production Backend

https://agrotrade-intelligence-backend.onrender.com

The deployed Flask application acts as the API layer consumed by the React frontend.

### Production Architecture

```text
                    Vercel
                      │
                      │ HTTPS / API Requests
                      ▼
                    Render
                      │
                      ▼
                 Flask API
                      │
                      ▼
              CatBoost Model
                      │
                      ▼
                 Prediction
```

---

## 🔗 Related Frontend

The frontend application is maintained separately:

**Frontend Repository:**
https://github.com/kumudsalunke26/AgroTrade-Intelligence-Frontend

**Frontend Deployment:**
https://agrotrade-frontend.vercel.app/

---

## 🎯 Project Objectives

* Develop a machine learning-based crop price prediction system
* Build a REST API for machine learning inference
* Integrate a trained regression model into a production backend
* Connect the ML backend with a React frontend
* Provide agricultural market intelligence
* Deploy a complete machine learning API to the cloud

---

## 🔮 Future Enhancements

* Real-time market data integration
* Automated model retraining
* Model performance monitoring
* Additional agricultural datasets
* Advanced price forecasting
* Explainable AI for predictions
* API authentication
* Prediction history
* Cloud-based model monitoring
* Automated ML pipelines

---

## 👩‍💻 Author

**Kumud Salunke**

GitHub:
https://github.com/kumudsalunke26
