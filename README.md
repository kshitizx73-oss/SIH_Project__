# MediHist - Patient Medical History Portal (Supabase & FastAPI)

**MediHist** is a full-stack patient medical record management web application built with **FastAPI**, **SQLAlchemy**, and **Supabase (PostgreSQL)**. It provides complete medical history tracking including patient demographics, general vitals (height, weight, BMI indicator, blood group), active medications, doctor consultations, family medical risks, diagnostic reports, and printable clinical chart summaries.

---

## 🚀 Features

- **Full Patient Lifecycle**: Intake wizard, patient chart selection, vitals management, and printable clinical summaries.
- **Supabase PostgreSQL Integration**: Direct connection with Supabase REST API & PostgreSQL database engine with Row Level Security (RLS).
- **Vibrant Pastel Light & Dark Themes**: Modern toggleable dark/light UI with pastel accent indicators.
- **Unified Global Search**: Search by patient name, code ID, medication, disease diagnosis, or doctor name.
- **FastAPI REST API**: OpenAPI interactive documentation available at `/docs` and ReDoc at `/redoc`.
- **Automated Test Suite**: Pytest automated test coverage for all endpoints.

---

## 🛠️ Project Structure

```text
├── index.html            # Single-page web application frontend with Supabase JS SDK
├── main.py               # FastAPI application entrypoint & static file serving
├── database.py           # SQLAlchemy database configuration for Supabase PostgreSQL & SQLite
├── models_fastapi.py     # SQLAlchemy ORM database models (Patient, Medication, Consultation, FamilyHistory, Report)
├── schemas.py            # Pydantic V2 request validation and serialization schemas
├── crud.py               # Database helper functions & unified search logic
├── seed_fastapi.py       # Database seeder script
├── supabase_setup.sql    # Complete SQL schema, RLS policies, and seed script for Supabase
├── test_fastapi_api.py   # Automated pytest unit test suite
├── requirements.txt      # Python package dependencies
├── .env.example          # Environment variables template
└── .gitignore            # Git ignore configuration
```

---

## ⚡ Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/medihist-supabase-portal.git
cd medihist-supabase-portal
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Update `.env` with your Supabase credentials:
```env
SUPABASE_URL=https://ynqyshgctoeektnlseet.supabase.co
SUPABASE_KEY=sb_publishable_kwXYWN9hoRts6HAoSS96rg_dvkopI1W
```

### 4. Run the FastAPI Server
```bash
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🗄️ Supabase Setup Instructions

1. Log into your **[Supabase Dashboard](https://supabase.com/dashboard)**.
2. Go to **SQL Editor** $\rightarrow$ **New Query**.
3. Copy and paste the contents of `supabase_setup.sql`.
4. Click **Run** to create all tables (`patients`, `medications`, `consultations`, `family_histories`, `reports`), set up Row Level Security (RLS) policies, and seed sample records.

---

## 🧪 Running Automated Tests

Run the test suite using pytest:
```bash
pytest test_fastapi_api.py
```
