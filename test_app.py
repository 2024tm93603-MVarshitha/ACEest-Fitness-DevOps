"""
Assignment 2 — Pytest Test Suite
ACEest Fitness & Gym | CSIZG514/SEZG514
"""

import pytest
import json
import os
import sys

# Make sure app module is importable from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["DB_NAME"] = ":memory:"   # Use in-memory SQLite for tests

from app import app as flask_app, init_db, calculate_calories, PROGRAMS


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        with flask_app.app_context():
            init_db()
        yield c


@pytest.fixture
def sample_client_data():
    return {
        "name": "TestUser",
        "age": 28,
        "weight": 70.0,
        "program": "Fat Loss (FL)"
    }


# ─────────────────────────────────────────────────────────────────────────────
# Health & Root
# ─────────────────────────────────────────────────────────────────────────────

class TestHealthAndRoot:

    def test_health_endpoint_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_endpoint_returns_healthy(self, client):
        data = json.loads(client.get("/health").data)
        assert data["status"] == "healthy"

    def test_root_returns_app_info(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert "ACEest Fitness" in data["app"]

    def test_root_contains_programs(self, client):
        data = json.loads(client.get("/").data)
        assert "programs" in data
        assert len(data["programs"]) > 0

    def test_root_returns_version(self, client):
        data = json.loads(client.get("/").data)
        assert "version" in data


# ─────────────────────────────────────────────────────────────────────────────
# Programs
# ─────────────────────────────────────────────────────────────────────────────

class TestPrograms:

    def test_get_programs_returns_list(self, client):
        resp = client.get("/programs")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert "programs" in data

    def test_all_expected_programs_present(self, client):
        data = json.loads(client.get("/programs").data)
        for prog in ["Fat Loss (FL)", "Muscle Gain (MG)", "Beginner (BG)"]:
            assert prog in data["programs"]

    def test_get_single_program_success(self, client):
        resp = client.get("/programs/fat-loss-(fl)")
        assert resp.status_code == 200

    def test_get_nonexistent_program_404(self, client):
        resp = client.get("/programs/nonexistent-program")
        assert resp.status_code == 404

    def test_program_details_have_calorie_factor(self, client):
        resp = client.get("/programs/fat-loss-(fl)")
        data = json.loads(resp.data)
        assert "calorie_factor" in data["details"]


# ─────────────────────────────────────────────────────────────────────────────
# Clients — POST (add)
# ─────────────────────────────────────────────────────────────────────────────

class TestAddClient:

    def test_add_valid_client_returns_201(self, client, sample_client_data):
        resp = client.post("/clients",
                           data=json.dumps(sample_client_data),
                           content_type="application/json")
        assert resp.status_code == 201

    def test_add_client_returns_calories(self, client, sample_client_data):
        resp = client.post("/clients",
                           data=json.dumps(sample_client_data),
                           content_type="application/json")
        data = json.loads(resp.data)
        assert "calories" in data
        assert data["calories"] > 0

    def test_add_client_missing_name_returns_400(self, client):
        resp = client.post("/clients",
                           data=json.dumps({"age": 25, "weight": 60, "program": "Beginner (BG)"}),
                           content_type="application/json")
        assert resp.status_code == 400

    def test_add_client_invalid_program_returns_400(self, client):
        resp = client.post("/clients",
                           data=json.dumps({"name": "X", "weight": 60, "program": "Zumba"}),
                           content_type="application/json")
        assert resp.status_code == 400

    def test_add_client_zero_weight_returns_400(self, client):
        resp = client.post("/clients",
                           data=json.dumps({"name": "X", "weight": 0, "program": "Beginner (BG)"}),
                           content_type="application/json")
        assert resp.status_code == 400

    def test_add_client_negative_weight_returns_400(self, client):
        resp = client.post("/clients",
                           data=json.dumps({"name": "X", "weight": -10, "program": "Beginner (BG)"}),
                           content_type="application/json")
        assert resp.status_code == 400


# ─────────────────────────────────────────────────────────────────────────────
# Clients — GET (list + individual)
# ─────────────────────────────────────────────────────────────────────────────

class TestGetClients:

    def _add(self, client, name="Alice", weight=65.0, program="Muscle Gain (MG)"):
        client.post("/clients",
                    data=json.dumps({"name": name, "age": 30, "weight": weight, "program": program}),
                    content_type="application/json")

    def test_get_clients_returns_list(self, client):
        resp = client.get("/clients")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert "clients" in data

    def test_added_client_appears_in_list(self, client):
        self._add(client)
        data = json.loads(client.get("/clients").data)
        names = [c["name"] for c in data["clients"]]
        assert "Alice" in names


# ─────────────────────────────────────────────────────────────────────────────
# Progress
# ─────────────────────────────────────────────────────────────────────────────

class TestProgress:

    def _add_client(self, client):
        client.post("/clients",
                    data=json.dumps({"name": "Bob", "age": 25, "weight": 80, "program": "Muscle Gain (MG)"}),
                    content_type="application/json")

    def test_log_progress_returns_201(self, client):
        self._add_client(client)
        resp = client.post("/clients/Bob/progress",
                           data=json.dumps({"adherence": 90}),
                           content_type="application/json")
        assert resp.status_code == 201

    def test_log_progress_returns_week(self, client):
        self._add_client(client)
        resp = client.post("/clients/Bob/progress",
                           data=json.dumps({"adherence": 85}),
                           content_type="application/json")
        data = json.loads(resp.data)
        assert "week" in data

    def test_get_progress_returns_history(self, client):
        self._add_client(client)
        client.post("/clients/Bob/progress",
                    data=json.dumps({"adherence": 80}),
                    content_type="application/json")
        resp = client.get("/clients/Bob/progress")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data["progress"]) >= 1


# ─────────────────────────────────────────────────────────────────────────────
# Calorie Calculator
# ─────────────────────────────────────────────────────────────────────────────

class TestCalorieCalculator:

    def test_calories_endpoint_valid(self, client):
        resp = client.get("/calories?weight=70&program=Fat Loss (FL)")
        assert resp.status_code == 200

    def test_calories_calculation_fat_loss(self, client):
        # 70kg * 22 = 1540
        resp = client.get("/calories?weight=70&program=Fat Loss (FL)")
        data = json.loads(resp.data)
        assert data["calories"] == 1540

    def test_calories_calculation_muscle_gain(self, client):
        # 80kg * 35 = 2800
        resp = client.get("/calories?weight=80&program=Muscle Gain (MG)")
        data = json.loads(resp.data)
        assert data["calories"] == 2800

    def test_calories_missing_weight_returns_400(self, client):
        resp = client.get("/calories?program=Beginner (BG)")
        assert resp.status_code == 400

    def test_calories_unknown_program_returns_400(self, client):
        resp = client.get("/calories?weight=70&program=Unknown")
        assert resp.status_code == 400


# ─────────────────────────────────────────────────────────────────────────────
# Unit — calculate_calories helper
# ─────────────────────────────────────────────────────────────────────────────

class TestCalculateCaloriesHelper:

    def test_fat_loss_factor(self):
        assert calculate_calories(70, "Fat Loss (FL)") == 1540

    def test_muscle_gain_factor(self):
        assert calculate_calories(80, "Muscle Gain (MG)") == 2800

    def test_beginner_factor(self):
        assert calculate_calories(60, "Beginner (BG)") == 1560

    def test_unknown_program_uses_default(self):
        # Default factor = 26
        assert calculate_calories(60, "Unknown") == 1560

    def test_zero_weight_returns_zero(self):
        assert calculate_calories(0, "Fat Loss (FL)") == 0
