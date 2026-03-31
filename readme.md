# 🎙️ Speech-Based Emotion and Mental Health Detection (SDED-T Net)

---

## 📌 Overview

This project presents a deep learning-based system for detecting stress from speech signals using a novel architecture called **SDED-T Net (Safety-Constrained Drift-Guided Dual-Head Transformer Network)**.

The system analyzes speech input in real-time and classifies emotional state as **Normal** or **Abnormal (Stress)** with a confidence score. It is designed for **mental health monitoring and safety-critical applications**.

---

## 🚀 Key Features

- 🎧 Real-time speech-based stress detection  
- 🌍 Multilingual support (English, Hindi, Telugu)  
- 🧠 Transformer-based contextual speech encoding (Wav2Vec2)  
- 🔁 Temporal modeling using Bi-LSTM  
- 📉 Emotional Drift Estimation  
- 🎯 Drift-Guided Attention Mechanism  
- ⚖️ Safety-Constrained Multi-Task Loss (SCMTL)  
- 🌐 Web-based user interface (Flask)  
- 🔐 Secure authentication with SQLite  

---

## 🧠 Proposed Model (SDED-T Net)

### 🔄 Model Pipeline

Speech Input → Preprocessing → Wav2Vec2 Encoder → BiLSTM → Drift Estimation → Drift-Guided Attention → Dual-Head Prediction → Output

### 🔍 Key Contributions

- Captures **temporal emotional variations**
- Models **emotional instability (drift)**
- Reduces **false negatives in stress detection**

---

## 📊 Performance Results

- **Accuracy:** 87.3%  
- **ROC-AUC:** 0.9534  
- **Abnormal Recall:** 88.1%  

These results demonstrate improved reliability and performance for stress detection.

---

## 🏗️ Project Structure

```plaintext
EMOTION_NOVELTY_APP/
│
├── AI Training Code, Dataset, Requirements and Execution Steps/
│   ├── AI Model Training Code/
│   │   ├── Emotion_novelty.ipynb
│   │   └── emotion_novelty.py
│   │
│   ├── sentinel dataset/
│   │   └── Drive link of dataset.txt
│   │
│   └── Requirements and Execution Steps.txt
│
├── models/
│   └── (Download model from Drive)
│
├── static/
│   └── js/
│       └── recorder.js
│
├── templates/
│   ├── about.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── voice.html
│
├── app.py
├── database.db
├── README.md
└── requirements.txt

## ⚙️ System Requirements
1) Python 3.8 or above
2) PyTorch
3) HuggingFace Transformers
4) Flask
5) NumPy, Pandas, Scikit-learn
6) SQLite3
7) FFmpeg
8) Web Browser (Chrome/Edge)


## 🎥 FFmpeg Setup ( Main Step )

FFmpeg is required for audio processing and conversion.

Steps:
1) Download FFmpeg from the official website
https://www.ffmpeg.org/download.html
2) Extract and place it in:
C:\ffmpeg
3) Add to Environment Variables (Path):
C:\ffmpeg\bin
4) Restart terminal

⚠️ Without FFmpeg, audio preprocessing and model inference will fail.

## 📦 Model

Due to GitHub file size limitations, the trained model is hosted externally.

👉 Download Model (Google Drive):
https://drive.google.com/drive/folders/1gDQBIRfdDH6Z4q6SMz9ID4v7gMkqgX9Y?usp=sharing


📌 After downloading:

Place the model file inside:
models/

## 📂 Dataset

Due to GitHub file size limitations, the dataset is hosted externally.

👉 Download Dataset (Google Drive):
https://drive.google.com/drive/folders/1o13k3HCysy6GDcMZXe4tFeg1WMRfOWo0?usp=sharing


📌 After downloading:

Place the dataset inside:
AI Training Code, Dataset, Requirements and Execution Steps/

## ▶️ Installation & Execution

Step 1: Clone Repository
- git clone https://github.com/charan82475/Speech-Based-Emotion-and-Mental-Health-Detection.git
- cd emotion_novelty_app

Step 2: Download Model and Dataset
Download from:
- Model:
https://drive.google.com/drive/folders/1gDQBIRfdDH6Z4q6SMz9ID4v7gMkqgX9Y?usp=sharing

- Dataset:
https://drive.google.com/drive/folders/1o13k3HCysy6GDcMZXe4tFeg1WMRfOWo0?usp=sharing

Step 3: Place Files in Correct Folders
- Place model (.pt) inside:
models/
- Place dataset folder inside:
AI Training Code, Dataset, Requirements and Execution Steps/

Step 4: Install Dependencies
- pip install -r requirements.txt

Step 5: Run Application
- python app.py

Step 6: Open in Browser
- http://127.0.0.1:5000

## 🖥️ Application Workflow
1) User opens the web application
2) Registers or logs in securely
3) Records speech using microphone
4) Audio is converted to 16 kHz WAV format using FFmpeg
5) Preprocessing is applied
6) Model performs inference using SDED-T Net
7) Output is displayed as:
 - Normal
 - Abnormal (Stress)
8) Confidence and drift score are shown

## 📊 Output Interpretation
1) Normal: Stable emotional condition
2) Abnormal: Stress-related emotional condition
3) Confidence Score: Prediction reliability
4) Drift Score: Emotional instability level

## 🔒 Security Features
1) Secure user authentication
2) Password hashing using Werkzeug
3) SQLite database for storage

## 🧪 Dataset Details
The model is trained on a multilingual dataset combining:

1) Hindi Speech Emotion Dataset
2) Telugu Emotion Dataset
3) RAVDESS Dataset
4) Indian Emotion Speech Corpus
5) Kaggle Audio Emotion Datasets

# Dataset Characteristics:
1) ~4454 audio samples
2) Binary classification (Normal vs Abnormal)
3) Balanced dataset
4) 80–20 train-validation split

## Limitations
1) Uses acted emotional datasets
2) Limited real-world validation
3) Performance may vary in noisy environments

## 🔮 Future Work
1) Real-world stress dataset integration
2) Improved cross-lingual generalization
3) Mobile and cloud deployment
4) Clinical validation

## 👨‍💻 Authors
 - Karna Charan Sai Reddy
 - Chintha Indhu Priya
 - Penikalapati Asmitha
 - J Bhargav Reddy

## 🎓 Institution
GITAM School of Computer Science and Engineering
Department of Computer Science and Systems Engineering
Bengaluru Campus

## 📜 License
This project is developed for academic and research purposes only.

## ⭐ Acknowledgement
This project was developed under the guidance of Mr. Kerenalli Sudarshana and with reference to modern deep learning techniques in Speech Emotion Recognition.
