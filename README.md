# ACEest Fitness & Gym — DevOps CI/CD Pipeline (Assignment 2)

**Course:** CSIZG514/SEZG514 — Introduction to DevOps (S1-25)  
**Student:** M Varshitha | **ID:** 2024TM93603  
**GitHub:** https://github.com/2024tm93603-MVarshitha/ACEest-Fitness-DevOps  
**Docker Hub:** https://hub.docker.com/r/2024tm93603mvarshitha/aceest-fitness  
**Cluster Endpoint:** http://192.168.49.2:30275  

---

## 📋 Overview

ACEest Fitness & Gym is a Flask-based web application for managing fitness programs, client profiles, and workout plans. This repository demonstrates a complete end-to-end DevOps CI/CD pipeline including automated testing, code quality analysis, containerization, and Kubernetes deployment with multiple deployment strategies.

---

## 🏗️ CI/CD Architecture

```
GitHub Push → Jenkins Pipeline → SonarQube Analysis → Docker Build → Docker Hub → Kubernetes Deploy
                    ↓
              Pytest Tests
                    ↓
           Quality Gate Check
                    ↓
            Docker Build & Push
                    ↓
         Kubernetes Deployment
        (5 Deployment Strategies)
```

### Tools Used

| Tool | Purpose |
|---|---|
| Git + GitHub | Version control & source code management |
| Jenkins | CI/CD build automation server |
| Pytest | Automated unit testing framework |
| SonarQube | Static code analysis & quality gate |
| Docker | Containerization of Flask application |
| Docker Hub | Container image registry |
| Minikube | Local Kubernetes cluster |
| GitHub Actions | Cloud-based CI/CD (backup pipeline) |

---

## 📁 Repository Structure

```
ACEest-Fitness-DevOps/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container image definition
├── Jenkinsfile                     # Jenkins CI/CD pipeline
├── sonar-project.properties        # SonarQube configuration
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # GitHub Actions workflow
├── tests/
│   ├── __init__.py
│   └── test_app.py                # Pytest test cases
├── k8s/
│   ├── rolling/deployment.yaml    # Rolling Update strategy
│   ├── blue-green/deployment.yaml # Blue-Green strategy
│   ├── canary/deployment.yaml     # Canary Release strategy
│   ├── shadow/deployment.yaml     # Shadow Deployment strategy
│   └── ab-testing/deployment.yaml # A/B Testing strategy
└── versions/
    ├── Aceestver-1.0.py           # Version 1.0 — Basic UI
    ├── Aceestver-1.1.py           # Version 1.1 — Calorie calculator
    ├── Aceestver1.1.2.py          # Version 1.1.2 — CSV export
    ├── Aceestver2.0.1.py          # Version 2.0 — SQLite DB
    ├── Aceestver-2.1.2.py         # Version 2.1.2 — Progress tracking
    ├── Aceestver-2.2.1.py         # Version 2.2.1 — Charts
    ├── Aceestver-2.2.4.py         # Version 2.2.4 — Enhanced
    ├── Aceestver-3.0.1.py         # Version 3.0 — Login system
    ├── Aceestver-3.1.2.py         # Version 3.1.2 — Workouts
    └── Aceestver-3.2.4.py         # Version 3.2.4 — Full featured
```

---

## 🚀 Local Setup and Execution

### Prerequisites
- Python 3.11+
- Docker
- Minikube
- kubectl

### 1. Clone the Repository
```bash
git clone https://github.com/2024tm93603-MVarshitha/ACEest-Fitness-DevOps.git
cd ACEest-Fitness-DevOps
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```
Application runs at: `http://localhost:5000`

### 4. API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | App info and programs list |
| `/health` | GET | Health check |
| `/programs` | GET | List all programs |
| `/clients` | GET/POST | Manage clients |
| `/clients/<name>/progress` | GET/POST | Track progress |
| `/calories` | GET | Calculate calories |

---

## 🧪 Running Tests Manually

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=html

# Run specific test
pytest tests/test_app.py::TestHealthAndRoot -v
```

### Test Coverage
- Health & Root endpoints
- Program listing and details
- Client CRUD operations
- Progress tracking
- Calorie calculation
- Helper function unit tests

---

## 🔧 Jenkins CI/CD Pipeline

Jenkins is configured at `http://localhost:8080`

### Pipeline Stages
1. **Checkout SCM** — Pull code from GitHub
2. **Install Dependencies** — pip install requirements
3. **Run Tests** — pytest with coverage
4. **SonarQube Analysis** — Static code analysis
5. **Docker Build** — Build container image
6. **Docker Push** — Push to Docker Hub
7. **Deploy** — Deploy to Kubernetes

### Trigger
Jenkins polls GitHub every 5 minutes for changes and automatically triggers a build on new commits.

---

## 📊 SonarQube Analysis

SonarQube runs at `http://localhost:9002`

- **Project Key:** aceest-fitness
- **Quality Gate Status:** ✅ PASSED
- **Lines of Code:** 173
- **Language:** Python, Docker

---

## 🐳 Docker

### Build Image
```bash
docker build -t 2024tm93603mvarshitha/aceest-fitness:v1 .
```

### Run Container
```bash
docker run -p 5000:5000 2024tm93603mvarshitha/aceest-fitness:latest
```

### Docker Hub Tags

| Tag | Version | Description |
|---|---|---|
| `v1` | 1.0 | Basic Flask app |
| `v2` | 2.0 | SQLite DB added |
| `v3` | 3.0 | Full featured |
| `v4` | 3.2.4 | Latest build |
| `latest` | 3.2.4 | Most recent |

---

## ☸️ Kubernetes Deployment (Minikube)

### Start Minikube
```bash
minikube start --driver=docker
```

### Deploy Application
```bash
minikube kubectl -- create deployment aceest \
  --image=2024tm93603mvarshitha/aceest-fitness:latest
minikube kubectl -- expose deployment aceest --port=5000 --type=NodePort
minikube service aceest --url
```

### Cluster Endpoint
```
http://192.168.49.2:30275
```

---

## 🎯 Deployment Strategies

### 1. Rolling Update
```bash
minikube kubectl -- set image deployment/aceest \
  aceest-fitness=2024tm93603mvarshitha/aceest-fitness:v2
minikube kubectl -- rollout status deployment/aceest
```

### 2. Blue-Green Deployment
```bash
minikube kubectl -- apply -f k8s/blue-green/deployment.yaml
# Switch traffic from blue to green
minikube kubectl -- patch service aceest \
  -p '{"spec":{"selector":{"slot":"green"}}}'
```

### 3. Canary Release
```bash
minikube kubectl -- apply -f k8s/canary/deployment.yaml
# 20% traffic goes to canary (1 canary + 4 stable pods)
```

### 4. Shadow Deployment
```bash
minikube kubectl -- apply -f k8s/shadow/deployment.yaml
# Mirror traffic to shadow without affecting users
```

### 5. A/B Testing
```bash
minikube kubectl -- apply -f k8s/ab-testing/deployment.yaml
# Route specific users to version B
```

### Rollback
```bash
minikube kubectl -- rollout undo deployment/aceest
minikube kubectl -- rollout history deployment/aceest
```

---

## 🔄 GitHub Actions

GitHub Actions workflow runs automatically on every push to `main` branch.

Workflow file: `.github/workflows/ci-cd.yml`

### Stages
1. Run Pytest tests
2. SonarQube analysis
3. Docker build & push
4. Deploy to Minikube

---

## 📈 Key Outcomes

- ✅ Fully automated CI/CD pipeline
- ✅ 35+ Pytest test cases
- ✅ SonarQube Quality Gate PASSED
- ✅ Docker images versioned and pushed to Hub
- ✅ 5 Kubernetes deployment strategies implemented
- ✅ Automated rollback mechanism
- ✅ Zero-downtime deployments

---

## 🔗 Links

- **GitHub Repository:** https://github.com/2024tm93603-MVarshitha/ACEest-Fitness-DevOps
- **Docker Hub:** https://hub.docker.com/r/2024tm93603mvarshitha/aceest-fitness
- **Cluster Endpoint:** http://192.168.49.2:30275
- **Jenkins:** http://localhost:8080
- **SonarQube:** http://localhost:9002
