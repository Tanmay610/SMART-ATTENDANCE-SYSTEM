# Smart Attendance System Using Face Recognition
**Author:** Tanmay Khosla  
**Project:** Automated Smart Attendance System with Deep Learning & Computer Vision  

---

## Overview
This automated attendance system eliminates manual roll calls and paper logs using deep learning face embeddings and computer vision. The system provides real-time facial recognition with deep feature extraction (FaceNet embeddings), a multi-layer neural network classifier, local caching, and MongoDB cloud/local database synchronization.

Features automated student enrollment, multi-threading training workflows, subject-based attendance tracking (e.g. Hindi, English lectures), and CSV export.

---

## Architecture & Pipeline

1. **Student Enrollment & Face Dataset Generation**:
   - Captures facial crops in real time using OpenCV's Haar Cascade classifier.
   - Saves cropped training samples locally under `people/` directory.
   - Automatically registers the student into MongoDB with initial attendance counts and syncs to `Students_Enrollment.csv`.

2. **Deep Feature Extraction & Model Training**:
   - Normalizes faces to 160×160 and extracts 128-dimensional biometric embeddings via pre-trained FaceNet.
   - Trains a multi-layer neural network classifier with Softmax activation.
   - Saves the trained model weights directly to `Model/Face_recognition.h5`.

3. **Real-Time Facial Recognition Attendance**:
   - Real-time video stream captures student faces.
   - Computes live embeddings and feeds them into the trained classifier.
   - Verifies identity thresholds and logs marked attendance to MongoDB and subject CSV files.

4. **Desktop User Interface (Tkinter)**:
   - High-contrast graphical user interface built with Tkinter, ttk, and tkmacosx.
   - Live attendance viewer with table Treeview display and subject selection.

---

## Prerequisites & Installation

Create and activate the virtual environment:
```bash
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -r Requirements/CPU_Req.txt
uv pip install tkmacosx
```

Make sure MongoDB service is active:
```bash
brew services start mongodb-community
```

---

## How to Run

Launch the application:
```bash
.venv/bin/python UI.py
```

### Steps:
1. **Enroll New Student**:
   - On the right panel (**For New Enrollment**), enter the **Roll Number** and **Student's Name**.
   - Click **Take Images** to capture face samples.
2. **Train Model**:
   - Click **Train The Model** to compile the neural network with the new student embeddings.
3. **Take Attendance**:
   - Select the lecture/subject (Hindi or English).
   - Click **Take Attendance** to start the recognition camera stream.
   - Press `q` to complete attendance.
4. **View Records**:
   - Click **Show Attendance** to load the updated student attendance table.

---
*Developed by Tanmay Khosla.*
