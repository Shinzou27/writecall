# WriteCall

A system to record audio and obtain transcriptions using Whisper.

---

## 📋 Installation Guide

### 1️⃣ Install FFMPEG  
FFMPEG is required to use Whisper. It’s recommended to use **Chocolatey** for installation:  
```bash
choco install ffmpeg
```

---

### 2️⃣ Install Required Modules  
Install the necessary Python modules by running:  
```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the API  
Start the API with the following command:  
```bash
uvicorn api.main:app --reload
```

---

### 4️⃣ Run the Application  
The application is a simple call recorder:  

1. **Name the Call**: Start by choosing a name for the call.  
2. **Recording Process**: During the recording, every 30 seconds, an audio segment will be saved on the server. The transcription will be linked to the saved audio.  

Run the application with:  
```bash
python .\app\app.py
```

---
