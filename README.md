# ACEest Fitness & Gym — DevOps CI/CD Pipeline
### Assignment 2 | CSIZG514/SEZG514/SEUSZG514 | S2-25

[![CI](https://github.com/2024tm93603-MVarshitha/ACEest-Fitness-DevOps/actions/workflows/main.yml/badge.svg)](https://github.com/2024tm93603-MVarshitha/ACEest-Fitness-DevOps/actions/workflows/main.yml)

---

## Project Overview
ACEest Fitness & Gym is a Flask-based REST API for fitness management.
This project demonstrates a complete DevOps lifecycle including version
control, automated testing, containerisation, and CI/CD pipelines.

---

## Local Setup & Execution

### Prerequisites
- Python 3.11
- pip
- Git
- Docker Desktop
- Java 17 + Jenkins

### Installation
```bash
# Clone the repository
git clone https://github.com/2024tm93603-MVarshitha/ACEest-Fitness-DevOps.git
cd ACEest-Fitness-DevOps

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
# Visit: http://localhost:5000
```

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | App info and status |
| GET | /health | Health check |
| GET | /programs | List all programs |
| POST | /clients | Add a client |
| GET | /clients | List all clients |
| POST | /clients/<name>/progress | Log weekly progress |
| GET | /calories?weight=X&program=Y | Estimate calories |

---

## Running Tests Manually
```bash
# Run all tests with verbose output
pytest tests/test_app.py -v

# Run with coverage report
pytest tests/test_app.py -v --cov=app --cov-report=term-missing
```

### Test Results
- **24 tests** across 5 test classes
- **88% code coverage**
- All tests pass on Python 3.11

### Test Classes
| Class | Tests | What Is Covered |
|-------|-------|----------------|
| TestHealth | 4 | Health endpoint, home endpoint |
| TestPrograms | 4 | Program listing, 404 handling |
| TestCalories | 7 | Calorie calculations, API errors |
| TestClients | 6 | Client CRUD, validation errors |
| TestProgress | 3 | Progress logging and retrieval |

---

## Docker
```bash
# Build the image
docker build -t aceest-fitness:latest .

# Run the container
docker run -d --name aceest-app -p 5000:5000 aceest-fitness:latest

# Verify it is running
curl http://localhost:5000/health
# {"status": "healthy"}

# Stop the container
docker stop aceest-app
```

---

## Jenkins CI/CD Integration

### What Jenkins Does
Jenkins is a local BUILD server installed on the development machine.
It pulls code from GitHub, runs the full pipeline, and automatically
rolls back if any stage fails.

### Pipeline Stages
### Setup
1. Install Jenkins from https://www.jenkins.io/download/
2. Open http://localhost:8080
3. Create new Pipeline job → Pipeline script from SCM
4. Repository URL: https://github.com/2024tm93603-MVarshitha/ACEest-Fitness-DevOps.git
5. Branch: */main | Script Path: Jenkinsfile
6. Click Build Now

### Rollback Strategy
Every build is tagged with BUILD_NUMBER (e.g. aceest-fitness:5).
If any stage fails, Jenkins automatically redeploys the previous
working image (BUILD_NUMBER - 1). This ensures zero downtime.

---

## GitHub Actions CI/CD Integration

### What GitHub Actions Does
GitHub Actions is a cloud-based CI/CD pipeline that runs automatically
on every push to main or version/* branches. No setup required —
it uses GitHub's free Ubuntu runners.

### Pipeline Jobs
### Setup
1. Install Jenkins from https://www.jenkins.io/download/
2. Open http://localhost:8080
3. Create new Pipeline job → Pipeline script from SCM
4. Repository URL: https://github.com/2024tm93603-MVarshitha/ACEest-Fitness-DevOps.git
5. Branch: */main | Script Path: Jenkinsfile
6. Click Build Now

### Rollback Strategy
Every build is tagged with BUILD_NUMBER (e.g. aceest-fitness:5).
If any stage fails, Jenkins automatically redeploys the previous
working image (BUILD_NUMBER - 1). This ensures zero downtime.

---

## GitHub Actions CI/CD Integration

### What GitHub Actions Does
GitHub Actions is a cloud-based CI/CD pipeline that runs automatically
on every push to main or version/* branches. No setup required —
it uses GitHub's free Ubuntu runners.

### Pipeline Jobs
### Trigger
- Every push to `main` branch
- Every push to `version/*` branches
- Every Pull Request to `main`

### View Results
Go to: https://github.com/2024tm93603-MVarshitha/ACEest-Fitness-DevOps/actions

---

## Version History

| Branch | Description |
|--------|-------------|
| main | Flask Web API — complete DevOps pipeline |
| version/1.0 | Basic Tkinter GUI with program selection |
| version/1.1 | Client profile form and calorie estimator |
| version/1.1.2 | CSV export and progress chart |
| version/2.0.1 | SQLite database integration |
| version/2.1.2 | Database bug fixes |
| version/2.2.1 | Progress chart from database |
| version/2.2.4 | Enhanced progress tracking |
| version/3.0.1 | Role-based login and PDF reports |
| version/3.1.2 | Workout tracking and membership billing |
| version/3.2.4 | Final Tkinter version before Flask conversion |