import os
import sys
from datetime import date, timedelta

import pytest


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fancyhotel"))
sys.path.insert(0, ROOT)


def _load_app():
    try:
        import serve

        return serve.app
    except Exception as exc:
        pytest.skip("MySQL-backed app is not available: {}".format(exc))


@pytest.fixture()
def client():
    app = _load_app()
    app.config["TESTING"] = True
    return app.test_client()


def login(client, username, password="password"):
    response = client.post("/api/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.get_json()


def test_customer_login_and_saved_cards_are_masked(client):
    payload = login(client, "C0001")
    assert payload["role"] == "customer"

    response = client.get("/api/payment", query_string={"username": "C0001"})
    assert response.status_code == 200
    cards = response.get_json()
    assert cards
    assert "cvv" not in cards[0]
    assert cards[0]["masked_number"].startswith("************")
    assert "card_number" not in cards[0]


def test_search_uses_date_overlap_to_hide_booked_room(client):
    checkin = (date.today() + timedelta(days=8)).strftime("%Y-%m-%d")
    checkout = (date.today() + timedelta(days=9)).strftime("%Y-%m-%d")

    response = client.get(
        "/api/searchRoom",
        query_string={"location": "Atlanta", "checkIn": checkin, "checkOut": checkout},
    )

    assert response.status_code == 200
    room_numbers = {room["room_number"] for room in response.get_json()["response"]}
    assert 104 not in room_numbers


def test_manager_can_get_demand_forecast(client):
    payload = login(client, "M0001")
    assert payload["role"] == "manager"

    response = client.get("/api/reports/demandForecast")
    assert response.status_code == 200
    data = response.get_json()
    assert data["forecast"]
    assert {"location", "month", "predicted_occupancy", "price_suggestion"}.issubset(data["forecast"][0])


def test_customer_cannot_access_demand_forecast(client):
    login(client, "C0001")
    response = client.get("/api/reports/demandForecast")
    assert response.status_code == 403
