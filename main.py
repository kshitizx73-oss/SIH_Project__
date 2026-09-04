import os
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import engine, get_db, Base
import models_fastapi as models
import schemas
import crud
from seed_fastapi import seed_db

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AyurMitra API — SIH PS 26047 Patient Case-Taking Software",
    description="Full Backend API for Ministry of Ayush / AIIA AyurMitra Patient Case-Taking Software.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed database on startup if empty
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    if db.query(models.Patient).count() == 0:
        seed_db()

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    return {"status": "ok", "app": "AyurMitra Backend", "version": "1.0.0"}


# --- PATIENT ENDPOINTS ---

@app.get("/api/v1/patients", response_model=List[schemas.PatientOut], tags=["Patients"])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_patients(db, skip=skip, limit=limit)

@app.get("/api/v1/patients/{patient_id}", response_model=schemas.PatientOut, tags=["Patients"])
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.get("/api/v1/patients/{patient_id}/summary", response_model=schemas.PatientSummaryOut, tags=["Patients"])
def read_patient_summary(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.post("/api/v1/patients", response_model=schemas.PatientOut, status_code=status.HTTP_201_CREATED, tags=["Patients"])
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db=db, patient=patient)

@app.put("/api/v1/patients/{patient_id}", response_model=schemas.PatientOut, tags=["Patients"])
def update_patient(patient_id: int, patient_update: schemas.PatientUpdate, db: Session = Depends(get_db)):
    db_patient = crud.update_patient(db=db, patient_id=patient_id, patient_update=patient_update)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.delete("/api/v1/patients/{patient_id}", tags=["Patients"])
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    success = crud.delete_patient(db=db, patient_id=patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"success": True, "message": f"Patient {patient_id} permanently deleted"}


# --- MEDICATION ENDPOINTS ---

@app.get("/api/v1/medications", response_model=List[schemas.MedicationOut], tags=["Medications"])
def read_medications(patient_id: Optional[int] = Query(None), status: Optional[str] = Query('all'), db: Session = Depends(get_db)):
    return crud.get_medications(db=db, patient_id=patient_id, status=status)

@app.post("/api/v1/medications", response_model=schemas.MedicationOut, status_code=status.HTTP_201_CREATED, tags=["Medications"])
def create_medication(medication: schemas.MedicationCreate, db: Session = Depends(get_db)):
    # Verify patient exists
    if not crud.get_patient(db, medication.patient_id):
        raise HTTPException(status_code=404, detail="Referenced patient_id does not exist")
    return crud.create_medication(db=db, med=medication)

@app.put("/api/v1/medications/{med_id}", response_model=schemas.MedicationOut, tags=["Medications"])
def update_medication(med_id: int, med_update: schemas.MedicationUpdate, db: Session = Depends(get_db)):
    db_med = crud.update_medication(db=db, med_id=med_id, med_update=med_update)
    if not db_med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return db_med

@app.delete("/api/v1/medications/{med_id}", tags=["Medications"])
def delete_medication(med_id: int, db: Session = Depends(get_db)):
    success = crud.delete_medication(db=db, med_id=med_id)
    if not success:
        raise HTTPException(status_code=404, detail="Medication not found")
    return {"success": True, "message": "Medication record deleted"}


# --- CONSULTATION ENDPOINTS ---

@app.get("/api/v1/consultations", response_model=List[schemas.ConsultationOut], tags=["Consultations"])
def read_consultations(patient_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    return crud.get_consultations(db=db, patient_id=patient_id)

@app.post("/api/v1/consultations", response_model=schemas.ConsultationOut, status_code=status.HTTP_201_CREATED, tags=["Consultations"])
def create_consultation(consultation: schemas.ConsultationCreate, db: Session = Depends(get_db)):
    if not crud.get_patient(db, consultation.patient_id):
        raise HTTPException(status_code=404, detail="Referenced patient_id does not exist")
    return crud.create_consultation(db=db, consultation=consultation)

@app.put("/api/v1/consultations/{doc_id}", response_model=schemas.ConsultationOut, tags=["Consultations"])
def update_consultation(doc_id: int, doc_update: schemas.ConsultationUpdate, db: Session = Depends(get_db)):
    db_doc = crud.update_consultation(db=db, doc_id=doc_id, doc_update=doc_update)
    if not db_doc:
        raise HTTPException(status_code=404, detail="Consultation record not found")
    return db_doc

@app.delete("/api/v1/consultations/{doc_id}", tags=["Consultations"])
def delete_consultation(doc_id: int, db: Session = Depends(get_db)):
    success = crud.delete_consultation(db=db, doc_id=doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Consultation record not found")
    return {"success": True, "message": "Consultation record deleted"}


# --- FAMILY HISTORY ENDPOINTS ---

@app.get("/api/v1/family-history", response_model=List[schemas.FamilyHistoryOut], tags=["Family History"])
def read_family_histories(patient_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    return crud.get_family_histories(db=db, patient_id=patient_id)

@app.post("/api/v1/family-history", response_model=schemas.FamilyHistoryOut, status_code=status.HTTP_201_CREATED, tags=["Family History"])
def create_family_history(family_history: schemas.FamilyHistoryCreate, db: Session = Depends(get_db)):
    if not crud.get_patient(db, family_history.patient_id):
        raise HTTPException(status_code=404, detail="Referenced patient_id does not exist")
    return crud.create_family_history(db=db, fam=family_history)

@app.put("/api/v1/family-history/{fam_id}", response_model=schemas.FamilyHistoryOut, tags=["Family History"])
def update_family_history(fam_id: int, fam_update: schemas.FamilyHistoryUpdate, db: Session = Depends(get_db)):
    db_fam = crud.update_family_history(db=db, fam_id=fam_id, fam_update=fam_update)
    if not db_fam:
        raise HTTPException(status_code=404, detail="Family history record not found")
    return db_fam

@app.delete("/api/v1/family-history/{fam_id}", tags=["Family History"])
def delete_family_history(fam_id: int, db: Session = Depends(get_db)):
    success = crud.delete_family_history(db=db, fam_id=fam_id)
    if not success:
        raise HTTPException(status_code=404, detail="Family history record not found")
    return {"success": True, "message": "Family history record deleted"}


# --- REPORT ENDPOINTS ---

@app.get("/api/v1/reports", response_model=List[schemas.ReportOut], tags=["Reports"])
def read_reports(patient_id: Optional[int] = Query(None), category: Optional[str] = Query('all'), db: Session = Depends(get_db)):
    return crud.get_reports(db=db, patient_id=patient_id, category=category)

@app.post("/api/v1/reports", response_model=schemas.ReportOut, status_code=status.HTTP_201_CREATED, tags=["Reports"])
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    if not crud.get_patient(db, report.patient_id):
        raise HTTPException(status_code=404, detail="Referenced patient_id does not exist")
    return crud.create_report(db=db, report=report)

@app.put("/api/v1/reports/{report_id}", response_model=schemas.ReportOut, tags=["Reports"])
def update_report(report_id: int, report_update: schemas.ReportUpdate, db: Session = Depends(get_db)):
    db_rep = crud.update_report(db=db, report_id=report_id, rep_update=report_update)
    if not db_rep:
        raise HTTPException(status_code=404, detail="Report record not found")
    return db_rep

@app.delete("/api/v1/reports/{report_id}", tags=["Reports"])
def delete_report(report_id: int, db: Session = Depends(get_db)):
    success = crud.delete_report(db=db, report_id=report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report record not found")
    return {"success": True, "message": "Report record deleted"}


# --- FULL INTAKE ENDPOINT ---

@app.post("/api/v1/intake", response_model=schemas.PatientOut, status_code=status.HTTP_201_CREATED, tags=["Intake"])
def create_full_intake(intake: schemas.FullIntakeCreate, db: Session = Depends(get_db)):
    patient_data = schemas.PatientCreate(
        first_name=intake.first_name,
        middle_name=intake.middle_name,
        last_name=intake.last_name,
        gender=intake.gender,
        dob=intake.dob,
        blood_group=intake.blood_group,
        phone=intake.phone,
        email=intake.email,
        height_cm=intake.height_cm,
        weight_kg=intake.weight_kg,
        allergies=intake.allergies,
        chronic_conditions=intake.chronic_conditions,
        insurance_provider=intake.insurance_provider,
        insurance_policy_number=intake.insurance_policy_number
    )
    db_patient = crud.create_patient(db=db, patient=patient_data)

    if intake.med_name:
        crud.create_medication(db=db, med=schemas.MedicationCreate(
            patient_id=db_patient.id,
            name=intake.med_name,
            dosage=intake.med_dosage or "N/A",
            frequency=intake.med_frequency or "Daily",
            route=intake.med_route or "Oral",
            prescribing_doctor=intake.med_prescriber,
            indication=intake.med_indication
        ))

    if intake.doc_name:
        crud.create_consultation(db=db, consultation=schemas.ConsultationCreate(
            patient_id=db_patient.id,
            doctor_name=intake.doc_name,
            specialization=intake.doc_specialty or "General Medicine",
            hospital=intake.doc_hospital,
            visit_date=intake.doc_visit_date or db_patient.dob,
            reason=intake.doc_reason,
            notes=intake.doc_notes
        ))

    if intake.fam_relation and intake.fam_condition:
        crud.create_family_history(db=db, fam=schemas.FamilyHistoryCreate(
            patient_id=db_patient.id,
            relation=intake.fam_relation,
            condition=intake.fam_condition,
            age_at_onset=intake.fam_age,
            status=intake.fam_status or "Living"
        ))

    return db_patient


# --- UNIFIED SEARCH ENDPOINT ---

@app.get("/api/v1/search", response_model=List[schemas.SearchResultItem], tags=["Search"])
def search(q: str = Query("", min_length=1), db: Session = Depends(get_db)):
    return crud.search_all(db=db, query_str=q.strip())


# --- SERVE FRONTEND SPA AT ROOT ---
@app.get("/", include_in_schema=False)
def serve_frontend():
    index_file = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "AyurMitra Backend Active. Access API docs at /docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
