from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import soundfile as sf
from pydub import AudioSegment
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model

app = Flask(__name__)
app.secret_key = "charan-super-secret-key-2026-change-me"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "database.db")

# ──── DATABASE ────
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ──── MODEL CLASS ────
class EmotionNoveltyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.wav2vec = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base")
        
        self.bilstm = nn.LSTM(
            input_size=self.wav2vec.config.hidden_size,
            hidden_size=256,
            num_layers=2,
            bidirectional=True,
            batch_first=True
        )
        
        self.attention = nn.Sequential(
            nn.Linear(512, 128),
            nn.Tanh(),
            nn.Linear(128, 1)
        )
        
        self.shared = nn.Sequential(
            nn.Linear(512, 256)
        )
        
        self.emotion_head = nn.Linear(256, 2)
        self.drift_head = nn.Linear(256, 1)  # NOW USED
        self.confidence_head = nn.Sequential(
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        features = self.wav2vec(x).last_hidden_state
        
        lstm_out, _ = self.bilstm(features)
        
        attn_scores = self.attention(lstm_out)
        attn_weights = F.softmax(attn_scores, dim=1)
        context = torch.sum(lstm_out * attn_weights, dim=1)
        
        shared = F.relu(self.shared(context))
        
        emotion_logits = self.emotion_head(shared)
        drift = self.drift_head(shared)  # ✅ NEW
        
        return emotion_logits, drift


# ──── LOAD MODEL ────
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = os.path.join(BASE_DIR, "models", "SDED_T_Final_Model.pt")

model = EmotionNoveltyModel()
state_dict = torch.load(MODEL_PATH, map_location=device, weights_only=True)
model.load_state_dict(state_dict)
model.to(device)
model.eval()

print("Model loaded successfully on", device)

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-base")


# ──── PREDICTION FUNCTION ────
def predict_normal_abnormal(audio_path):
    audio, sr = sf.read(audio_path)

    if sr != 16000:
        sound = AudioSegment.from_file(audio_path)
        sound = sound.set_channels(1).set_frame_rate(16000)
        sound.export(audio_path, format="wav")
        audio, sr = sf.read(audio_path)

    inputs = feature_extractor(
        audio,
        sampling_rate=sr,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=16000 * 8
    ).input_values.to(device)

    with torch.no_grad():
        logits, drift = model(inputs)  # ✅ UPDATED

        probs = torch.softmax(logits, dim=-1)[0].cpu().numpy()
        
        idx = probs.argmax()
        emotion = "Abnormal" if idx == 1 else "Normal"
        confidence = probs[idx] * 100

        # ✅ DRIFT SCORE
        drift_score = torch.sigmoid(drift)[0].item()  # normalize (0–1)

        print(f"Probabilities: {probs}")
        print(f"Drift Score: {drift_score}")

    return emotion, round(confidence, 2), round(drift_score, 4)


# ──── ROUTES ────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Login successful!", "success")
            return redirect(url_for("voice"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = generate_password_hash(request.form["password"])

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO users (name,email,phone,password) VALUES (?,?,?,?)",
                (name, email, phone, password)
            )
            conn.commit()
            conn.close()

            flash("Registration successful", "success")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Email already exists", "danger")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("index"))


@app.route("/voice", methods=["GET", "POST"])
def voice():
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        if "audio" not in request.files:
            return jsonify({"error": "No audio"}), 400

        audio_file = request.files["audio"]

        webm_path = os.path.join(BASE_DIR, "temp.webm")
        wav_path = os.path.join(BASE_DIR, "temp.wav")

        audio_file.save(webm_path)

        sound = AudioSegment.from_file(webm_path)
        sound = sound.set_channels(1).set_frame_rate(16000)
        sound.export(wav_path, format="wav")

        emotion, conf, drift = predict_normal_abnormal(wav_path)

        try:
            os.remove(webm_path)
            os.remove(wav_path)
        except:
            pass

        return jsonify({
            "emotion": emotion,
            "confidence": conf,
            "drift": drift
        })

    return render_template("voice.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)