import pytest, json, os, sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))
import app as app_module
from app import calculate_calories, PROGRAMS

@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    app_module.DB_NAME = "test_aceest.db"
    with app_module.app.test_client() as c:
        app_module.init_db()
        yield c
    if os.path.exists("test_aceest.db"):
        os.remove("test_aceest.db")

@pytest.fixture
def sample():
    return {"name":"Arjun","age":25,
            "weight":75.0,"program":"Muscle Gain (MG)"}

# ── Health & Home ──────────────────────────────────────────
class TestHealth:
    def test_health_200(self, client):
        assert client.get("/health").status_code == 200

    def test_health_status(self, client):
        data = json.loads(client.get("/health").data)
        assert data["status"] == "healthy"

    def test_index_200(self, client):
        assert client.get("/").status_code == 200

    def test_index_app_name(self, client):
        data = json.loads(client.get("/").data)
        assert "ACEest" in data["app"]

# ── Programs ───────────────────────────────────────────────
class TestPrograms:
    def test_get_programs_200(self, client):
        assert client.get("/programs").status_code == 200

    def test_three_programs(self, client):
        data = json.loads(client.get("/programs").data)
        assert len(data["programs"]) == 3

    def test_fat_loss_exists(self, client):
        data = json.loads(client.get("/programs").data)
        assert "Fat Loss (FL)" in data["programs"]

    def test_unknown_program_404(self, client):
        assert client.get("/programs/xyz").status_code == 404

# ── Calories ───────────────────────────────────────────────
class TestCalories:
    def test_fat_loss_calc(self):
        assert calculate_calories(70.0, "Fat Loss (FL)") == 1540

    def test_muscle_gain_calc(self):
        assert calculate_calories(80.0, "Muscle Gain (MG)") == 2800

    def test_beginner_calc(self):
        assert calculate_calories(60.0, "Beginner (BG)") == 1560

    def test_returns_int(self):
        assert isinstance(calculate_calories(72.5, "Beginner (BG)"), int)

    def test_api_calories(self, client):
        r = client.get("/calories?weight=70&program=Muscle Gain (MG)")
        assert r.status_code == 200
        assert json.loads(r.data)["calories"] == 2450

    def test_api_missing_params(self, client):
        assert client.get("/calories?weight=70").status_code == 400

    def test_api_invalid_program(self, client):
        assert client.get(
            "/calories?weight=70&program=Invalid").status_code == 400

# ── Clients ────────────────────────────────────────────────
class TestClients:
    def test_empty_clients(self, client):
        data = json.loads(client.get("/clients").data)
        assert data["clients"] == []

    def test_add_client_201(self, client, sample):
        r = client.post("/clients",
                        data=json.dumps(sample),
                        content_type="application/json")
        assert r.status_code == 201

    def test_add_client_calories(self, client, sample):
        r = client.post("/clients",
                        data=json.dumps(sample),
                        content_type="application/json")
        assert json.loads(r.data)["calories"] == 2625

    def test_missing_name_400(self, client):
        r = client.post("/clients",
                        data=json.dumps({"weight":70,
                                         "program":"Beginner (BG)"}),
                        content_type="application/json")
        assert r.status_code == 400

    def test_invalid_program_400(self, client):
        r = client.post("/clients",
                        data=json.dumps({"name":"X","weight":70,
                                         "program":"Invalid"}),
                        content_type="application/json")
        assert r.status_code == 400

    def test_zero_weight_400(self, client):
        r = client.post("/clients",
                        data=json.dumps({"name":"X","weight":0,
                                         "program":"Beginner (BG)"}),
                        content_type="application/json")
        assert r.status_code == 400

# ── Progress ───────────────────────────────────────────────
class TestProgress:
    def _add(self, client):
        client.post("/clients",
                    data=json.dumps({"name":"Arjun","age":25,
                                     "weight":75.0,
                                     "program":"Muscle Gain (MG)"}),
                    content_type="application/json")

    def test_log_progress_201(self, client):
        self._add(client)
        r = client.post("/clients/Arjun/progress",
                        data=json.dumps({"adherence":80}),
                        content_type="application/json")
        assert r.status_code == 201

    def test_empty_progress(self, client):
        self._add(client)
        data = json.loads(
            client.get("/clients/Arjun/progress").data)
        assert data["progress"] == []

    def test_progress_after_log(self, client):
        self._add(client)
        client.post("/clients/Arjun/progress",
                    data=json.dumps({"adherence":90}),
                    content_type="application/json")
        data = json.loads(
            client.get("/clients/Arjun/progress").data)
        assert len(data["progress"]) == 1
        assert data["progress"][0]["adherence"] == 90