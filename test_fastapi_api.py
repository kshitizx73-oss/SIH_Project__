import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_fastapi.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_patients_crud():
    # 1. Create Patient
    payload = {
        "first_name": "Arthur",
        "middle_name": "Pendelton",
        "last_name": "Smith",
        "gender": "Male",
        "dob": "1968-04-12",
        "blood_group": "A+",
        "phone": "+1 (555) 234-5678"
    }
    create_res = client.post("/api/v1/patients", json=payload)
    assert create_res.status_code == 201
    pat_data = create_res.json()
    assert pat_data["patient_code"] == "APS1268"
    assert pat_data["age"] > 50
    pat_id = pat_data["id"]

    # 2. Get Patients List
    list_res = client.get("/api/v1/patients")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # 3. Get Patient Detail
    get_res = client.get(f"/api/v1/patients/{pat_id}")
    assert get_res.status_code == 200
    assert get_res.json()["full_name"] == "Arthur Pendelton Smith"

    # 4. Update Patient
    up_res = client.put(f"/api/v1/patients/{pat_id}", json={"allergies": "Penicillin"})
    assert up_res.status_code == 200
    assert up_res.json()["allergies"] == "Penicillin"

    # 5. Delete Patient
    del_res = client.delete(f"/api/v1/patients/{pat_id}")
    assert del_res.status_code == 200
    assert client.get(f"/api/v1/patients/{pat_id}").status_code == 404

def test_medications_crud():
    p_res = client.post("/api/v1/patients", json={
        "first_name": "Clara", "last_name": "Montgomery", "gender": "Female", "dob": "1992-09-18"
    })
    pat_id = p_res.json()["id"]

    # Create Medication
    m_res = client.post("/api/v1/medications", json={
        "patient_id": pat_id, "name": "Metformin", "dosage": "500 mg", "frequency": "Twice daily"
    })
    assert m_res.status_code == 201
    med_id = m_res.json()["id"]

    # Get Medications List
    list_res = client.get(f"/api/v1/medications?patient_id={pat_id}")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # Delete Medication
    del_res = client.delete(f"/api/v1/medications/{med_id}")
    assert del_res.status_code == 200

def test_full_summary_and_search():
    p_res = client.post("/api/v1/patients", json={
        "first_name": "Arthur", "last_name": "Pendelton", "gender": "Male", "dob": "1968-04-12"
    })
    pat_id = p_res.json()["id"]
    pat_code = p_res.json()["patient_code"]

    client.post("/api/v1/medications", json={
        "patient_id": pat_id, "name": "Lisinopril", "dosage": "20 mg", "frequency": "Daily"
    })

    # Summary
    sum_res = client.get(f"/api/v1/patients/{pat_id}/summary")
    assert sum_res.status_code == 200
    sum_data = sum_res.json()
    assert len(sum_data["medications"]) == 1

    # Search
    s_res = client.get(f"/api/v1/search?q={pat_code}")
    assert s_res.status_code == 200
    assert len(s_res.json()) >= 1
    assert s_res.json()[0]["type"] == "patient"
