import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ============================
# 1️⃣ TEST :parse
# ============================


def test_parse_transactions_valid():
    payload = [
        {"date": "2024-01-01 12:07:00", "amount": 150},
        {"date": "2024-01-02 13:15:00", "amount": 275},
    ]

    response = client.post("/api/blackrock/challenge/v1/transactions:parse", json=payload)
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["ceiling"] >= payload[0]["amount"]
    assert data[1]["remanent"] == data[1]["ceiling"] - payload[1]["amount"]


def test_parse_transactions_empty():
    response = client.post("/api/blackrock/challenge/v1/transactions:parse", json=[])
    assert response.status_code == 200
    assert response.json() == []


def test_parse_transactions_invalid_payload():
    payload = [{"date": "2024-01-01 12:09:55"}]  # missing amount
    response = client.post("/api/blackrock/challenge/v1/transactions:parse", json=payload)
    assert response.status_code == 422


# ============================
# 2️⃣ TEST :validate
# ============================


def test_validate_transactions_valid():
    payload = {
        "wage": 50000,
        "transaction": [
            {"date": "2026-02-21 06:04:11", "amount": 2000, "ceiling": 300, "remanent": 50},
            {"date": "2026-02-21 06:04:11", "amount": 3500, "ceiling": 400, "remanent": 70}
        ],
    }

    response = client.post("/api/blackrock/challenge/v1/transactions:validate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert len(data["valid"]) == 2
    assert len(data["invalid"]) == 0


def test_validate_transactions_negative_amount():
    payload = {"wage": 3000, "transaction": [{"date": "2024-01-01 12:07:00", "amount": 2000, "ceiling": 300, "remanent": 50}, {"date": "2024-01-02 13:15:00", "amount": -150, "ceiling": 200, "remanent": 30}]}

    response = client.post("/api/blackrock/challenge/v1/transactions:validate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert len(data["invalid"]) == 1
    assert data["invalid"][0]["message"] == "negative amounts are not allowed"


def test_validate_transactions_duplicate():
    payload = {
        "wage": 3000,
        "transaction": [
            {"date": "2024-01-01 12:07:00", "amount": 1010, "ceiling": 1100, "remanent": 90},
            {"date": "2024-01-01 12:07:00", "amount": 1010, "ceiling": 1100, "remanent": 90},
        ]
    }

    response = client.post("/api/blackrock/challenge/v1/transactions:validate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert len(data["valid"]) == 1
    assert len(data["invalid"]) == 1
    assert data["invalid"][0]["message"] == "Duplicate transactions"


def test_validate_transactions_mixed():
    payload = {
        "wage": 3000,
        "transaction": [
            {"date": "2024-01-01 12:07:00", "amount": 1010, "ceiling": 1100, "remanent": 90},
            {"date": "2024-01-01 12:07:00", "amount": 1010, "ceiling": 1100, "remanent": 90},
            {"date": "2024-01-02 13:15:00", "amount": -50, "ceiling": 0, "remanent": 0},
        ]
    }

    response = client.post("/api/blackrock/challenge/v1/transactions:validate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert len(data["valid"]) == 1
    assert len(data["invalid"]) == 2


# ============================
# 3️⃣ TEST :filter
# ============================


def test_filter_transactions_basic():
    payload = {
        "transaction": [
            {"date": "2024-01-01 12:07:00", "amount": 150},
            {"date": "2024-01-02 13:15:00", "amount": 275},
        ],
        "q": [],
        "p": [],
        "k": [],
        "wage": 0,
    }

    response = client.post("/api/blackrock/challenge/v1/transactions:filter", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "valid" in data
    assert "invalid" in data


def test_filter_transactions_negative_and_duplicate():
    payload = {
        "transaction": [
            {"date": "2024-01-01 12:07:00", "amount": 150},
            {"date": "2024-01-01 12:07:00", "amount": 150},
            {"date": "2024-01-02 13:15:00", "amount": -10},
        ],
        "q": [
            {"fixed": 0, "start": "2026-07-01 00:00:00", "end": "2026-07-31 23:59:59"}
        ],
        "p": [
            {"extra": 25, "start": "2026-10-01 08:00:00", "end": "2026-12-31 19:59:59"}
        ],
        "k": [{"start": "2026-01-01 00:00:00", "end": "2026-12-31 23:59:59"}],
        "wage": 50000
    }

    response = client.post("/api/blackrock/challenge/v1/transactions:filter", json=payload)
    assert response.status_code == 200

    data = response.json()

    assert len(data["invalid"]) == 2
    assert any(i["message"] == "Duplicate transactions" for i in data["invalid"])
    assert any(
        i["message"] == "negative amounts are not allowed" for i in data["invalid"]
    )


def test_filter_transactions_k_period():
    payload = {
        "wage": 50000,
        "q": [
            {"fixed": 0, "start": "2026-07-01 00:00:00", "end": "2026-07-31 23:59:59"}
        ],
        "p": [
            {"extra": 25, "start": "2026-10-01 08:00:00", "end": "2026-12-31 19:59:59"}
        ],
        "k": [{"start": "2026-01-01 00:00:00", "end": "2026-12-31 23:59:59"}],
        "transaction": [
            {"date": "2026-02-28 15:49:20", "amount": 375},
            {"date": "2026-07-15 10:30:00", "amount": 620},
            {"date": "2026-10-12 20:15:30", "amount": 250},
            {"date": "2026-10-12 20:15:30", "amount": 250},
            {"date": "2026-12-17 08:09:45", "amount": -480},
        ],
    }

    response = client.post("/api/blackrock/challenge/v1/transactions:filter", json=payload)
    assert response.status_code == 200

    data = response.json()

    if data["valid"]:
        assert data["valid"][0]["inKPeriod"] is True


def test_filter_transactions_empty():
    payload = {"transaction": [], "q": [], "p": [], "k": [], "wage": 0}

    response = client.post("/api/blackrock/challenge/v1/transactions:filter", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["valid"] == []
    assert data["invalid"] == []
