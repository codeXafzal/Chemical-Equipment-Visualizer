# Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop App)

## 📌 Project Overview

The **Chemical Equipment Parameter Visualizer** is a hybrid application designed to run as both a **Web Application** and a **Desktop Application**, powered by a single Django backend API. The system allows users to upload CSV files containing chemical equipment data, perform analytics, and visualize insights through charts and tables.

Both the **React (Web)** and **PyQt5 (Desktop)** frontends consume the same Django REST API, demonstrating clean architecture, reusability, and real-world full‑stack integration.

---

## 🧱 System Architecture

```
React (Web)        PyQt5 (Desktop)
     |                    |
     |------ REST API ----|
              |
        Django + DRF
              |
           SQLite DB
```

---

## 🛠 Tech Stack

### Backend

* Python
* Django
* Django REST Framework (DRF)
* Pandas
* SQLite

### Frontend (Web)

* React.js
* Chart.js
* Axios

### Frontend (Desktop)

* PyQt5
* Matplotlib
* Requests

### Other

* Git & GitHub

---

## ✨ Key Features

* CSV file upload (Web & Desktop)
* Data analysis using Pandas
* Summary statistics (total count, averages)
* Equipment type distribution
* Interactive charts
* Tabular data view
* History management (last 5 datasets only)
* PDF report generation
* Basic authentication

---

## 📂 Project Structure

```
chemical-equipment-visualizer/
│
├── backend/
│   ├── manage.py
│   ├── backend/
│   ├── equipment/
│   └── venv/
│
├── web/
│   └── react-app/
│
├── desktop/
│   └── pyqt_app/
│
├── sample_equipment_data.csv
├── README.md
└── .gitignore
```

---

## 🚀 Setup Instructions

### 1️⃣ Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend runs at:

```
http://127.0.0.1:8000/
```

---

### 2️⃣ Web Frontend Setup

```bash
cd web/react-app
npm install
npm start
```

Web app runs at:

```
http://localhost:3000/
```

---

### 3️⃣ Desktop Application Setup

```bash
cd desktop/pyqt_app
python main.py
```

---

## 🔌 API Endpoints

| Method | Endpoint      | Description              |
| ------ | ------------- | ------------------------ |
| POST   | /api/upload/  | Upload CSV file          |
| GET    | /api/history/ | Last 5 dataset summaries |

---

## 🔐 Authentication

* Django session-based authentication
* APIs protected using `IsAuthenticated`
* Login via Django Admin

---

## 📊 Sample Data

A sample CSV file `sample_equipment_data.csv` is provided for testing and demo purposes.

---

## 📸 Screenshots

(Add screenshots of Web UI, Desktop UI, and charts here)

---

## 🎥 Demo Video

A short demo video (2–3 minutes) is provided separately as per submission guidelines.

---

## 📄 License

This project is created for **internship screening and educational purposes**.
