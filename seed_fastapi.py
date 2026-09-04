from database import SessionLocal, engine, Base
import models_fastapi as models

def seed_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if empty
        if db.query(models.Patient).count() > 0:
            print("Database already seeded.")
            return

        print("Seeding AyurMitra SIH database with sample records...")

        # 1. Patient 1: Arthur Pendelton
        p1 = models.Patient(
            first_name="Arthur",
            middle_name="Pendelton",
            last_name="Smith",
            gender="Male",
            dob="1968-04-12",
            blood_group="A+",
            phone="+1 (555) 234-5678",
            email="arthur.pendelton@example.com",
            height_cm=178.0,
            weight_kg=84.5,
            allergies="Penicillin (Severe Rash), Sulfa Drugs (Hives)",
            chronic_conditions="Type 2 Diabetes Mellitus, Essential Hypertension, Hyperlipidemia",
            insurance_provider="BlueCross BlueShield",
            insurance_policy_number="BCBS-98721405"
        )
        db.add(p1)
        db.commit()
        db.refresh(p1)

        # Patient 1 Medications
        meds1 = [
            models.Medication(
                patient_id=p1.id, name="Metformin", dosage="1000 mg", frequency="Twice daily with meals",
                route="Oral", prescribing_doctor="Dr. Marcus Vance", indication="Type 2 Diabetes Mellitus", status="Active"
            ),
            models.Medication(
                patient_id=p1.id, name="Lisinopril", dosage="20 mg", frequency="Once daily (Morning)",
                route="Oral", prescribing_doctor="Dr. Sarah Jenkins", indication="Essential Hypertension", status="Active"
            ),
            models.Medication(
                patient_id=p1.id, name="Atorvastatin", dosage="40 mg", frequency="Once daily (Bedtime)",
                route="Oral", prescribing_doctor="Dr. Sarah Jenkins", indication="Hyperlipidemia", status="Active"
            ),
            models.Medication(
                patient_id=p1.id, name="Aspirin Low Dose", dosage="81 mg", frequency="Once daily",
                route="Oral", prescribing_doctor="Dr. Sarah Jenkins", indication="Cardiovascular Primary Prevention", status="Active"
            )
        ]

        # Patient 1 Consultations
        docs1 = [
            models.Consultation(
                patient_id=p1.id, doctor_name="Dr. Sarah Jenkins", specialization="Cardiology", hospital="Metro Heart Center",
                visit_date="2026-06-15", reason="Routine 6-month BP check", notes="BP 126/80 mmHg. ECG normal sinus rhythm. Continue Lisinopril."
            ),
            models.Consultation(
                patient_id=p1.id, doctor_name="Dr. Marcus Vance", specialization="Endocrinology", hospital="St. Jude Complex",
                visit_date="2026-05-10", reason="HbA1c Followup", notes="HbA1c improved to 6.8%. Diet adherence good."
            )
        ]

        # Patient 1 Family History
        fams1 = [
            models.FamilyHistory(
                patient_id=p1.id, relation="Father", condition="Coronary Artery Disease", age_at_onset="55", status="Deceased"
            ),
            models.FamilyHistory(
                patient_id=p1.id, relation="Mother", condition="Type 2 Diabetes Mellitus", age_at_onset="60", status="Living"
            )
        ]

        # Patient 1 Reports
        reps1 = [
            models.Report(
                patient_id=p1.id, title="Comprehensive Metabolic Panel & HbA1c", category="Lab Test", report_date="2026-05-08",
                findings="HbA1c: 6.8%, Fasting Glucose: 118 mg/dL, eGFR: 88 mL/min."
            ),
            models.Report(
                patient_id=p1.id, title="12-Lead Resting Electrocardiogram (ECG)", category="Imaging", report_date="2026-06-15",
                findings="Normal sinus rhythm with rate 68 bpm. No ST-T wave changes."
            )
        ]

        # 2. Patient 2: Clara Montgomery
        p2 = models.Patient(
            first_name="Clara",
            last_name="Montgomery",
            gender="Female",
            dob="1992-09-18",
            blood_group="O-",
            phone="+1 (555) 876-5432",
            email="clara.m@example.com",
            height_cm=165.0,
            weight_kg=61.0,
            allergies="Latex, Shellfish",
            chronic_conditions="Moderate Persistent Asthma, Hypothyroidism",
            insurance_provider="Aetna Health Care",
            insurance_policy_number="AET-441092"
        )
        db.add(p2)
        db.commit()
        db.refresh(p2)

        meds2 = [
            models.Medication(
                patient_id=p2.id, name="Levothyroxine", dosage="75 mcg", frequency="Once daily",
                route="Oral", prescribing_doctor="Dr. Elena Rostova", indication="Hypothyroidism", status="Active"
            ),
            models.Medication(
                patient_id=p2.id, name="Advair Diskus", dosage="250/50 mcg", frequency="Twice daily",
                route="Inhaler", prescribing_doctor="Dr. Vikram Patel", indication="Asthma Maintenance", status="Active"
            ),
            models.Medication(
                patient_id=p2.id, name="Albuterol Sulfate Inhaler", dosage="90 mcg", frequency="2 puffs every 4-6 hours PRN",
                route="Inhaler", prescribing_doctor="Dr. Vikram Patel", indication="Acute Bronchospasm Rescue", status="As Needed"
            )
        ]

        docs2 = [
            models.Consultation(
                patient_id=p2.id, doctor_name="Dr. Vikram Patel", specialization="Pulmonology", hospital="Respiratory Care Center",
                visit_date="2026-07-12", reason="Asthma Control Check", notes="Spirometry pre-FEV1 82%, post-albuterol 94%. Good response."
            ),
            models.Consultation(
                patient_id=p2.id, doctor_name="Dr. Elena Rostova", specialization="Endocrinology", hospital="City Health Endocrinology",
                visit_date="2026-04-03", reason="Thyroid Function Followup", notes="TSH 2.1 mIU/L, Free T4 1.2 ng/dL. Patient feeling well."
            )
        ]

        fams2 = [
            models.FamilyHistory(
                patient_id=p2.id, relation="Mother", condition="Hashimoto's Thyroiditis", age_at_onset="40", status="Living"
            )
        ]

        reps2 = [
            models.Report(
                patient_id=p2.id, title="Pulmonary Function Test (Spirometry)", category="Imaging", report_date="2026-07-12",
                findings="FEV1: 2.85L (82% predicted). Significant bronchodilator response (+12%)."
            ),
            models.Report(
                patient_id=p2.id, title="Serum TSH & Free T4 Panel", category="Lab Test", report_date="2026-04-01",
                findings="TSH: 2.10 mIU/L. Free T4: 1.24 ng/dL. Thyroid function normal on therapy."
            )
        ]

        for item in meds1 + docs1 + fams1 + reps1 + meds2 + docs2 + fams2 + reps2:
            db.add(item)

        db.commit()
        print("AyurMitra SIH database seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
