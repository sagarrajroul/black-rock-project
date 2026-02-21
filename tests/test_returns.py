from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def sample_payload():
    return {
        "q": [],
        "p": [],
        "k": [],
        "wage": 0,
        "transaction": [
            {"date": "2026-02-21 06:04:11", "amount": 150},
            {"date": "2026-02-22 06:04:11", "amount": -50},
            {"date": "2026-02-23 06:04:11", "amount": 275}
        ],
        "age": 30,
        "inflation": 5
    }



def test_calculate_nps_basic():
    response = client.post(
        "/api/blackrock/challenge/v1/returns:nps",
        json=sample_payload()
    )

    assert response.status_code == 200

    data = response.json()

    # Negative amount ignored → 150 + 275
    assert data["totalTransactionAmount"] == 425

    # Ceiling: 200 + 300
    assert data["totalCeilingAmount"] == 500

    assert "savingsByDates" in data



def test_calculate_index_basic():
    response = client.post(
        "/api/blackrock/challenge/v1/returns:index",
        json=sample_payload()
    )

    assert response.status_code == 200

    data = response.json()

    assert data["totalTransactionAmount"] == 425
    assert data["totalCeilingAmount"] == 500
    assert "savingsByDates" in data



def test_empty_transactions():
    payload = sample_payload()
    payload["transaction"] = []

    response = client.post(
        "/api/blackrock/challenge/v1/returns:nps",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["totalTransactionAmount"] == 0
    assert data["totalCeilingAmount"] == 0


def test_all_negative_transactions():
    payload = sample_payload()
    payload["transaction"] = [
        {"date": "2026-02-21 06:04:11", "amount": -100}
    ]

    response = client.post(
        "/api/blackrock/challenge/v1/returns:nps",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["totalTransactionAmount"] == 0
    assert data["totalCeilingAmount"] == 0