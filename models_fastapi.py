from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True, default="")
    last_name = Column(String(50), nullable=False)
    gender = Column(String(20), nullable=False)
    dob = Column(String(20), nullable=False)  # YYYY-MM-DD
    blood_group = Column(String(10), default="Unknown")
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    allergies = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    insurance_provider = Column(String(100), nullable=True)
    insurance_policy_number = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships with ON DELETE CASCADE
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    consultations = relationship("Consultation", back_populates="patient", cascade="all, delete-orphan")
    family_histories = relationship("FamilyHistory", back_populates="patient", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="patient", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        if self.middle_name and self.middle_name.strip():
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    @property
    def patient_code(self) -> str:
        letters = ""
        if self.first_name:
            letters += self.first_name[0].upper()
        if self.middle_name and self.middle_name.strip():
            letters += self.middle_name.strip()[0].upper()
        if self.last_name:
            letters += self.last_name[0].upper()
        
        numbers = ""
        if self.dob:
            parts = str(self.dob).split("-")
            if len(parts) == 3:
                year = parts[0]
                day = parts[2]
                numbers = f"{day}{year[-2:]}"
        return f"{letters}{numbers}"

    @property
    def age(self) -> int:
        if not self.dob:
            return 0
        try:
            dob_dt = datetime.strptime(str(self.dob), "%Y-%m-%d")
            today = datetime.today()
            return today.year - dob_dt.year - ((today.month, today.day) < (dob_dt.month, dob_dt.day))
        except Exception:
            return 0


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    route = Column(String(50), default="Oral")
    prescribing_doctor = Column(String(100), nullable=True)
    indication = Column(String(200), nullable=True)
    status = Column(String(20), default="Active")  # Active, Discontinued, As Needed
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="medications")


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    hospital = Column(String(150), nullable=True)
    visit_date = Column(String(20), nullable=False)
    reason = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="consultations")


class FamilyHistory(Base):
    __tablename__ = "family_histories"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    relation = Column(String(50), nullable=False)
    condition = Column(String(100), nullable=False)
    age_at_onset = Column(String(20), nullable=True)
    status = Column(String(20), default="Living")  # Living, Deceased
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="family_histories")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(150), nullable=False)
    category = Column(String(50), default="Lab Test")
    report_date = Column(String(20), nullable=False)
    findings = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="reports")
