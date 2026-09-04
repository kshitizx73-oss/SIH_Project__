from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# --- Medication Schemas ---
class MedicationBase(BaseModel):
    name: str
    dosage: str
    frequency: str
    route: Optional[str] = "Oral"
    prescribing_doctor: Optional[str] = None
    indication: Optional[str] = None
    status: Optional[str] = "Active"

class MedicationCreate(MedicationBase):
    patient_id: int

class MedicationUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None
    prescribing_doctor: Optional[str] = None
    indication: Optional[str] = None
    status: Optional[str] = None

class MedicationOut(MedicationBase):
    id: int
    patient_id: int
    model_config = ConfigDict(from_attributes=True)


# --- Consultation Schemas ---
class ConsultationBase(BaseModel):
    doctor_name: str
    specialization: str
    hospital: Optional[str] = None
    visit_date: str
    reason: Optional[str] = None
    notes: Optional[str] = None

class ConsultationCreate(ConsultationBase):
    patient_id: int

class ConsultationUpdate(BaseModel):
    doctor_name: Optional[str] = None
    specialization: Optional[str] = None
    hospital: Optional[str] = None
    visit_date: Optional[str] = None
    reason: Optional[str] = None
    notes: Optional[str] = None

class ConsultationOut(ConsultationBase):
    id: int
    patient_id: int
    model_config = ConfigDict(from_attributes=True)


# --- Family History Schemas ---
class FamilyHistoryBase(BaseModel):
    relation: str
    condition: str
    age_at_onset: Optional[str] = None
    status: Optional[str] = "Living"

class FamilyHistoryCreate(FamilyHistoryBase):
    patient_id: int

class FamilyHistoryUpdate(BaseModel):
    relation: Optional[str] = None
    condition: Optional[str] = None
    age_at_onset: Optional[str] = None
    status: Optional[str] = None

class FamilyHistoryOut(FamilyHistoryBase):
    id: int
    patient_id: int
    model_config = ConfigDict(from_attributes=True)


# --- Report Schemas ---
class ReportBase(BaseModel):
    title: str
    category: Optional[str] = "Lab Test"
    report_date: str
    findings: Optional[str] = None

class ReportCreate(ReportBase):
    patient_id: int

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    report_date: Optional[str] = None
    findings: Optional[str] = None

class ReportOut(ReportBase):
    id: int
    patient_id: int
    model_config = ConfigDict(from_attributes=True)


# --- Patient Schemas ---
class PatientBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = ""
    last_name: str
    gender: str
    dob: str
    blood_group: Optional[str] = "Unknown"
    phone: Optional[str] = None
    email: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None

class PatientOut(PatientBase):
    id: int
    age: int
    full_name: str
    patient_code: str
    model_config = ConfigDict(from_attributes=True)


# --- Full Patient Summary Schema ---
class PatientSummaryOut(PatientOut):
    medications: List[MedicationOut] = []
    consultations: List[ConsultationOut] = []
    family_histories: List[FamilyHistoryOut] = []
    reports: List[ReportOut] = []


# --- Full Intake Request Schema ---
class FullIntakeCreate(PatientBase):
    med_name: Optional[str] = None
    med_dosage: Optional[str] = None
    med_frequency: Optional[str] = None
    med_route: Optional[str] = "Oral"
    med_prescriber: Optional[str] = None
    med_indication: Optional[str] = None

    doc_name: Optional[str] = None
    doc_specialty: Optional[str] = None
    doc_hospital: Optional[str] = None
    doc_visit_date: Optional[str] = None
    doc_reason: Optional[str] = None
    doc_notes: Optional[str] = None

    fam_relation: Optional[str] = None
    fam_condition: Optional[str] = None
    fam_age: Optional[str] = None
    fam_status: Optional[str] = "Living"


# --- Search Result Item Schema ---
class SearchResultItem(BaseModel):
    type: str  # patient, medication, consultation, family_history, report
    title: str
    subtitle: str
    patient_id: int
    action_tab: str
    model_config = ConfigDict(from_attributes=True)
