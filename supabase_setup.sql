-- ================================================================
-- Complete Supabase PostgreSQL Schema & RLS Setup Script for MediHist
-- Paste this script directly into Supabase SQL Editor -> New Query -> Run
-- Project URL: https://ynqyshgctoeektnlseet.supabase.co
-- ================================================================

-- 1. Patients Table
CREATE TABLE IF NOT EXISTS public.patients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50) DEFAULT '',
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    dob VARCHAR(20) NOT NULL,
    blood_group VARCHAR(10) DEFAULT 'Unknown',
    phone VARCHAR(20),
    email VARCHAR(100),
    height_cm DOUBLE PRECISION DEFAULT 170.0,
    weight_kg DOUBLE PRECISION DEFAULT 70.0,
    allergies TEXT DEFAULT 'None reported',
    chronic_conditions TEXT DEFAULT 'None recorded',
    insurance_provider VARCHAR(100),
    insurance_policy_number VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Medications Table
CREATE TABLE IF NOT EXISTS public.medications (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES public.patients(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    frequency VARCHAR(50) NOT NULL,
    route VARCHAR(50) DEFAULT 'Oral',
    prescribing_doctor VARCHAR(100),
    indication VARCHAR(200),
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Consultations (Doctor Visits) Table
CREATE TABLE IF NOT EXISTS public.consultations (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES public.patients(id) ON DELETE CASCADE,
    doctor_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    hospital VARCHAR(150),
    visit_date VARCHAR(20) NOT NULL,
    reason VARCHAR(200),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Family History Table
CREATE TABLE IF NOT EXISTS public.family_histories (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES public.patients(id) ON DELETE CASCADE,
    relation VARCHAR(50) NOT NULL,
    condition VARCHAR(100) NOT NULL,
    age_at_onset VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Living',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Reports Table
CREATE TABLE IF NOT EXISTS public.reports (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES public.patients(id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(50) DEFAULT 'Lab Test',
    report_date VARCHAR(20) NOT NULL,
    findings TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create Indexes for fast foreign key lookups
CREATE INDEX IF NOT EXISTS idx_medications_patient_id ON public.medications(patient_id);
CREATE INDEX IF NOT EXISTS idx_consultations_patient_id ON public.consultations(patient_id);
CREATE INDEX IF NOT EXISTS idx_family_histories_patient_id ON public.family_histories(patient_id);
CREATE INDEX IF NOT EXISTS idx_reports_patient_id ON public.reports(patient_id);

-- Enable Row Level Security (RLS) and grant full access to anonymous/authenticated users with publishable key
ALTER TABLE public.patients ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow public read and write access on patients" ON public.patients;
CREATE POLICY "Allow public read and write access on patients" ON public.patients FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE public.medications ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow public read and write access on medications" ON public.medications;
CREATE POLICY "Allow public read and write access on medications" ON public.medications FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE public.consultations ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow public read and write access on consultations" ON public.consultations;
CREATE POLICY "Allow public read and write access on consultations" ON public.consultations FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE public.family_histories ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow public read and write access on family_histories" ON public.family_histories;
CREATE POLICY "Allow public read and write access on family_histories" ON public.family_histories FOR ALL USING (true) WITH CHECK (true);

ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow public read and write access on reports" ON public.reports;
CREATE POLICY "Allow public read and write access on reports" ON public.reports FOR ALL USING (true) WITH CHECK (true);

-- Insert Sample Patient Seed Data
INSERT INTO public.patients (id, first_name, middle_name, last_name, gender, dob, blood_group, phone, email, height_cm, weight_kg, allergies, chronic_conditions, insurance_provider, insurance_policy_number)
VALUES 
(1, 'Arthur', 'Pendelton', 'Smith', 'Male', '1968-04-12', 'A+', '+1 (555) 234-5678', 'arthur.smith@example.com', 178.0, 84.5, 'Penicillin (Severe Rash), Sulfa Drugs (Hives)', 'Type 2 Diabetes Mellitus, Essential Hypertension, Hyperlipidemia', 'BlueCross BlueShield', 'BCBS-98721405'),
(2, 'Clara', 'Evelyn', 'Montgomery', 'Female', '1992-09-18', 'O-', '+1 (555) 876-5432', 'clara.m@example.com', 165.0, 61.0, 'Latex (Contact Dermatitis), Shellfish', 'Moderate Persistent Asthma, Primary Hypothyroidism', 'Aetna Health Care', 'AET-44109822')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.medications (id, patient_id, name, dosage, frequency, route, prescribing_doctor, indication, status)
VALUES 
(1, 1, 'Metformin', '1000 mg', 'Twice daily with meals', 'Oral', 'Dr. Marcus Vance', 'Type 2 Diabetes Mellitus', 'Active'),
(2, 1, 'Lisinopril', '20 mg', 'Once daily (Morning)', 'Oral', 'Dr. Sarah Jenkins', 'Essential Hypertension', 'Active'),
(3, 1, 'Atorvastatin', '40 mg', 'Once daily (Bedtime)', 'Oral', 'Dr. Sarah Jenkins', 'Hyperlipidemia', 'Active'),
(4, 2, 'Levothyroxine', '75 mcg', 'Once daily (30 min before breakfast)', 'Oral', 'Dr. Elena Rostova', 'Primary Hypothyroidism', 'Active')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.consultations (id, patient_id, doctor_name, specialization, hospital, visit_date, reason, notes)
VALUES 
(1, 1, 'Dr. Sarah Jenkins', 'Cardiology', 'Metro Heart Center', '2026-06-15', 'Routine 6-month BP check', 'BP 126/80 mmHg. ECG normal sinus rhythm. Continue Lisinopril.'),
(2, 1, 'Dr. Marcus Vance', 'Endocrinology', 'St. Jude Medical Complex', '2026-05-10', 'HbA1c Followup', 'HbA1c improved to 6.8%. Diet adherence good.')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.family_histories (id, patient_id, relation, condition, age_at_onset, status)
VALUES 
(1, 1, 'Father', 'Coronary Artery Disease', '55', 'Deceased'),
(2, 1, 'Mother', 'Type 2 Diabetes Mellitus', '60', 'Living')
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.reports (id, patient_id, title, category, report_date, findings)
VALUES 
(1, 1, 'Comprehensive Metabolic Panel & HbA1c', 'Lab Test', '2026-05-08', 'HbA1c: 6.8%, Fasting Glucose: 118 mg/dL, eGFR: 88 mL/min.'),
(2, 1, '12-Lead Resting Electrocardiogram (ECG)', 'Imaging', '2026-06-15', 'Normal sinus rhythm with rate 68 bpm. No ST-T wave changes.')
ON CONFLICT (id) DO NOTHING;

-- Synchronize sequences for primary key auto-incrementing
SELECT setval('public.patients_id_seq', COALESCE((SELECT MAX(id) FROM public.patients), 1));
SELECT setval('public.medications_id_seq', COALESCE((SELECT MAX(id) FROM public.medications), 1));
SELECT setval('public.consultations_id_seq', COALESCE((SELECT MAX(id) FROM public.consultations), 1));
SELECT setval('public.family_histories_id_seq', COALESCE((SELECT MAX(id) FROM public.family_histories), 1));
SELECT setval('public.reports_id_seq', COALESCE((SELECT MAX(id) FROM public.reports), 1));
