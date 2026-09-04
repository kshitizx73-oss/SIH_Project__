from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
import models_fastapi as models
import schemas

# --- Patient CRUD ---
def get_patient(db: Session, patient_id: int) -> Optional[models.Patient]:
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[models.Patient]:
    return db.query(models.Patient).offset(skip).limit(limit).all()

def create_patient(db: Session, patient: schemas.PatientCreate) -> models.Patient:
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def update_patient(db: Session, patient_id: int, patient_update: schemas.PatientUpdate) -> Optional[models.Patient]:
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    
    update_data = patient_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int) -> bool:
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return False
    db.delete(db_patient)
    db.commit()
    return True


# --- Medication CRUD ---
def get_medication(db: Session, med_id: int) -> Optional[models.Medication]:
    return db.query(models.Medication).filter(models.Medication.id == med_id).first()

def get_medications(db: Session, patient_id: Optional[int] = None, status: Optional[str] = None) -> List[models.Medication]:
    query = db.query(models.Medication)
    if patient_id:
        query = query.filter(models.Medication.patient_id == patient_id)
    if status and status != 'all':
        query = query.filter(models.Medication.status == status)
    return query.all()

def create_medication(db: Session, med: schemas.MedicationCreate) -> models.Medication:
    db_med = models.Medication(**med.model_dump())
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return db_med

def update_medication(db: Session, med_id: int, med_update: schemas.MedicationUpdate) -> Optional[models.Medication]:
    db_med = get_medication(db, med_id)
    if not db_med:
        return None
    update_data = med_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_med, key, value)
    db.commit()
    db.refresh(db_med)
    return db_med

def delete_medication(db: Session, med_id: int) -> bool:
    db_med = get_medication(db, med_id)
    if not db_med:
        return False
    db.delete(db_med)
    db.commit()
    return True


# --- Consultation CRUD ---
def get_consultation(db: Session, doc_id: int) -> Optional[models.Consultation]:
    return db.query(models.Consultation).filter(models.Consultation.id == doc_id).first()

def get_consultations(db: Session, patient_id: Optional[int] = None) -> List[models.Consultation]:
    query = db.query(models.Consultation)
    if patient_id:
        query = query.filter(models.Consultation.patient_id == patient_id)
    return query.order_by(models.Consultation.visit_date.desc()).all()

def create_consultation(db: Session, consultation: schemas.ConsultationCreate) -> models.Consultation:
    db_doc = models.Consultation(**consultation.model_dump())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def update_consultation(db: Session, doc_id: int, doc_update: schemas.ConsultationUpdate) -> Optional[models.Consultation]:
    db_doc = get_consultation(db, doc_id)
    if not db_doc:
        return None
    update_data = doc_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_doc, key, value)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def delete_consultation(db: Session, doc_id: int) -> bool:
    db_doc = get_consultation(db, doc_id)
    if not db_doc:
        return False
    db.delete(db_doc)
    db.commit()
    return True


# --- Family History CRUD ---
def get_family_history(db: Session, fam_id: int) -> Optional[models.FamilyHistory]:
    return db.query(models.FamilyHistory).filter(models.FamilyHistory.id == fam_id).first()

def get_family_histories(db: Session, patient_id: Optional[int] = None) -> List[models.FamilyHistory]:
    query = db.query(models.FamilyHistory)
    if patient_id:
        query = query.filter(models.FamilyHistory.patient_id == patient_id)
    return query.all()

def create_family_history(db: Session, fam: schemas.FamilyHistoryCreate) -> models.FamilyHistory:
    db_fam = models.FamilyHistory(**fam.model_dump())
    db.add(db_fam)
    db.commit()
    db.refresh(db_fam)
    return db_fam

def update_family_history(db: Session, fam_id: int, fam_update: schemas.FamilyHistoryUpdate) -> Optional[models.FamilyHistory]:
    db_fam = get_family_history(db, fam_id)
    if not db_fam:
        return None
    update_data = fam_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_fam, key, value)
    db.commit()
    db.refresh(db_fam)
    return db_fam

def delete_family_history(db: Session, fam_id: int) -> bool:
    db_fam = get_family_history(db, fam_id)
    if not db_fam:
        return False
    db.delete(db_fam)
    db.commit()
    return True


# --- Report CRUD ---
def get_report(db: Session, report_id: int) -> Optional[models.Report]:
    return db.query(models.Report).filter(models.Report.id == report_id).first()

def get_reports(db: Session, patient_id: Optional[int] = None, category: Optional[str] = None) -> List[models.Report]:
    query = db.query(models.Report)
    if patient_id:
        query = query.filter(models.Report.patient_id == patient_id)
    if category and category != 'all':
        query = query.filter(models.Report.category == category)
    return query.order_by(models.Report.report_date.desc()).all()

def create_report(db: Session, report: schemas.ReportCreate) -> models.Report:
    db_rep = models.Report(**report.model_dump())
    db.add(db_rep)
    db.commit()
    db.refresh(db_rep)
    return db_rep

def update_report(db: Session, report_id: int, rep_update: schemas.ReportUpdate) -> Optional[models.Report]:
    db_rep = get_report(db, report_id)
    if not db_rep:
        return None
    update_data = rep_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_rep, key, value)
    db.commit()
    db.refresh(db_rep)
    return db_rep

def delete_report(db: Session, report_id: int) -> bool:
    db_rep = get_report(db, report_id)
    if not db_rep:
        return False
    db.delete(db_rep)
    db.commit()
    return True


# --- Search Functionality ---
def search_all(db: Session, query_str: str) -> List[schemas.SearchResultItem]:
    if not query_str:
        return []

    q_pattern = f"%{query_str}%"
    results = []

    # 1. Search Patients
    patients = db.query(models.Patient).filter(
        or_(
            models.Patient.first_name.ilike(q_pattern),
            models.Patient.middle_name.ilike(q_pattern),
            models.Patient.last_name.ilike(q_pattern),
            models.Patient.allergies.ilike(q_pattern),
            models.Patient.chronic_conditions.ilike(q_pattern),
            models.Patient.phone.ilike(q_pattern),
            models.Patient.email.ilike(q_pattern)
        )
    ).all()

    # Also match patient code
    all_pats = db.query(models.Patient).all()
    matched_ids = {p.id for p in patients}
    for p in all_pats:
        if query_str.upper() in p.patient_code.upper():
            if p.id not in matched_ids:
                patients.append(p)
                matched_ids.add(p.id)

    for p in patients:
        results.append(schemas.SearchResultItem(
            type="patient",
            title=f"{p.full_name} ({p.patient_code})",
            subtitle=f"{p.gender}, {p.dob} | Blood: {p.blood_group} | Allergies: {p.allergies or 'None'}",
            patient_id=p.id,
            action_tab="dashboard"
        ))

    # 2. Search Medications
    meds = db.query(models.Medication).filter(
        or_(
            models.Medication.name.ilike(q_pattern),
            models.Medication.indication.ilike(q_pattern),
            models.Medication.prescribing_doctor.ilike(q_pattern)
        )
    ).all()
    for m in meds:
        pat = get_patient(db, m.patient_id)
        pat_str = f"Patient: {pat.full_name} ({pat.patient_code})" if pat else ""
        results.append(schemas.SearchResultItem(
            type="medication",
            title=f"{m.name} ({m.dosage})",
            subtitle=f"{pat_str} | Status: {m.status} | Doctor: {m.prescribing_doctor or 'N/A'}",
            patient_id=m.patient_id,
            action_tab="medications"
        ))

    # 3. Search Consultations
    docs = db.query(models.Consultation).filter(
        or_(
            models.Consultation.doctor_name.ilike(q_pattern),
            models.Consultation.specialization.ilike(q_pattern),
            models.Consultation.reason.ilike(q_pattern),
            models.Consultation.notes.ilike(q_pattern)
        )
    ).all()
    for d in docs:
        pat = get_patient(db, d.patient_id)
        pat_str = f"Patient: {pat.full_name} ({pat.patient_code})" if pat else ""
        results.append(schemas.SearchResultItem(
            type="consultation",
            title=f"{d.doctor_name} ({d.specialization})",
            subtitle=f"{pat_str} | Date: {d.visit_date} | Reason: {d.reason or 'N/A'}",
            patient_id=d.patient_id,
            action_tab="doctors"
        ))

    # 4. Search Family History
    fams = db.query(models.FamilyHistory).filter(
        or_(
            models.FamilyHistory.relation.ilike(q_pattern),
            models.FamilyHistory.condition.ilike(q_pattern)
        )
    ).all()
    for f in fams:
        pat = get_patient(db, f.patient_id)
        pat_str = f"Patient: {pat.full_name} ({pat.patient_code})" if pat else ""
        results.append(schemas.SearchResultItem(
            type="family_history",
            title=f"{f.relation} - {f.condition}",
            subtitle=f"{pat_str} | Status: {f.status} (Onset: {f.age_at_onset or 'N/A'})",
            patient_id=f.patient_id,
            action_tab="family"
        ))

    # 5. Search Reports
    reps = db.query(models.Report).filter(
        or_(
            models.Report.title.ilike(q_pattern),
            models.Report.category.ilike(q_pattern),
            models.Report.findings.ilike(q_pattern)
        )
    ).all()
    for r in reps:
        pat = get_patient(db, r.patient_id)
        pat_str = f"Patient: {pat.full_name} ({pat.patient_code})" if pat else ""
        results.append(schemas.SearchResultItem(
            type="report",
            title=f"{r.title} [{r.category}]",
            subtitle=f"{pat_str} | Date: {r.report_date}",
            patient_id=r.patient_id,
            action_tab="reports"
        ))

    return results
