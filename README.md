# ACEest Fitness & Gym — DevOps CI/CD Pipeline
### Assignment 1 | CSIZG514/SEZG514/SEUSZG514 | S2-25
 
## Quick Start
```bash
pip install -r requirements.txt
python app.py
# Visit: http://localhost:5000
```
 
## Run Tests
```bash
pytest tests/test_app.py -v --cov=app --cov-report=term-missing
```
 
## Docker
```bash
docker build -t aceest-fitness .
docker run -d -p 5000:5000 aceest-fitness
# Visit: http://localhost:5000/health
```
 
## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | App info |
| GET | /health | Health check |
| GET | /programs | List programs |
| POST | /clients | Add client |
| GET | /clients | List clients |
| POST | /clients/<name>/progress | Log progress |
| GET | /calories?weight=X&program=Y | Estimate calories |
 
## CI/CD Pipeline Overview
 
### GitHub Actions (`.github/workflows/main.yml`)
Automatically triggered on every push or pull request to `main`:
- **Lint** — Flake8 checks `app.py` for code quality
- **Test** — Runs 24 Pytest cases with coverage report
- **Docker Build** — Builds Docker image and runs smoke test on port 5000
 
### Jenkins (Local BUILD Server)
Jenkins runs locally at `http://localhost:8080` using Java 17 (Eclipse Temurin).
 
**Pipeline Stages:**
1. `Checkout` — Pulls latest code from GitHub
2. `Setup Python` — Creates virtual environment and installs dependencies
3. `Lint` — Flake8 validation
4. `Unit Tests` — 24 Pytest cases with coverage
5. `Docker Verify` — Confirms Docker availability
6. `Post Actions` — Cleanup workspace
 
**Rollback:** Configured in `Jenkinsfile` — on failure, automatically rolls back to previous Docker image build.
 
**Requirements:**
- Java 17 (Eclipse Temurin)
- Jenkins 2.541.3 LTS
- Python 3.11
- Docker
 
## OSHA VM Deployment
App is deployed on AWS Virtual Lab instance via Docker:
```bash
git clone https://github.com/2024tm93603-MVarshitha/ACEest-Fitness-DevOps.git
cd ACEest-Fitness-DevOps
docker build -t aceest-fitness .
docker run -d --name aceest-app -p 5000:5000 aceest-fitness
curl http://localhost:5000/health
# {"status": "healthy"}
```
 
## Version History
| Branch | Version | Features |
|--------|---------|----------|
| version/1.0 | v1.0 | Basic Tkinter GUI |
| version/1.1 | v1.1 | Client profile form |
| version/1.1.2 | v1.1.2 | CSV export + charts |
| version/2.0.1 | v2.0.1 | SQLite integration |
| version/2.1.2 | v2.1.2 | DB bug fixes |
| version/2.2.1 | v2.2.1 | Progress charts |
| version/2.2.4 | v2.2.4 | Enhanced tracking |
| version/3.0.1 | v3.0.1 | Role-based login + PDF |
| version/3.1.2 | v3.1.2 | Workout tracking |
| version/3.2.4 | v3.2.4 | Flask REST API (current) |
| main | latest | DevOps CI/CD Pipeline |
