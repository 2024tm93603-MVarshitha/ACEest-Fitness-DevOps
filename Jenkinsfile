pipeline {
    agent any
    environment {
        APP_NAME       = "aceest-fitness"
        IMAGE_TAG      = "${APP_NAME}:${BUILD_NUMBER}"
        FLASK_PORT     = "5000"
        CONTAINER_NAME = "aceest-live"
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        timeout(time: 15, unit: 'MINUTES')
        timestamps()
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
                sh 'git log --oneline -5'
            }
        }
        stage('Setup Python') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip --quiet
                    pip install -r requirements.txt --quiet
                    pip install flake8 --quiet
                '''
            }
        }
        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 app.py --max-line-length=120 --count
                    echo "Lint passed!"
                '''
            }
        }
        stage('Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/test_app.py -v \
                        --cov=app \
                        --cov-report=term-missing \
                        --junitxml=test-results.xml
                '''
            }
            post {
                always { junit 'test-results.xml' }
            }
        }
        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t ${IMAGE_TAG} .
                    docker tag ${IMAGE_TAG} ${APP_NAME}:latest
                    echo "Docker image built: ${IMAGE_TAG}"
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm   ${CONTAINER_NAME} 2>/dev/null || true
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${FLASK_PORT}:5000 \
                        --restart unless-stopped \
                        ${IMAGE_TAG}
                    sleep 5
                    curl --fail http://localhost:${FLASK_PORT}/health
                    echo "Deployment successful!"
                '''
            }
        }
        stage('Smoke Test') {
            steps {
                sh '''
                    curl --fail http://localhost:${FLASK_PORT}/ \
                      | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'ACEest' in d['app']"
                    echo "Smoke test passed!"
                '''
            }
        }
    }
    post {
        success {
            echo "BUILD #${BUILD_NUMBER} SUCCEEDED - App at http://localhost:${FLASK_PORT}"
        }
        failure {
            echo "BUILD #${BUILD_NUMBER} FAILED - Starting rollback..."
            sh '''
                PREV=$((BUILD_NUMBER - 1))
                PREV_IMAGE="${APP_NAME}:${PREV}"
                if docker image inspect ${PREV_IMAGE} > /dev/null 2>&1; then
                    docker stop ${CONTAINER_NAME} 2>/dev/null || true
                    docker rm   ${CONTAINER_NAME} 2>/dev/null || true
                    docker run -d --name ${CONTAINER_NAME} \
                        -p ${FLASK_PORT}:5000 \
                        --restart unless-stopped ${PREV_IMAGE}
                    echo "Rolled back to Build #${PREV}"
                else
                    echo "No previous image found. No rollback performed."
                fi
            '''
        }
        always {
            sh 'rm -f test-results.xml .coverage 2>/dev/null || true'
            sh 'rm -rf venv 2>/dev/null || true'
        }
    }
}