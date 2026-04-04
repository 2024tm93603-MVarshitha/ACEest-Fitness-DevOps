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
pytest tests/test_app.py -v
```

## Docker
```bash
docker build -t aceest-fitness .
docker run -p 5000:5000 aceest-fitness
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

## CI/CD
- **GitHub Actions** — auto runs on every push
- **Jenkins** — local BUILD server with rollback