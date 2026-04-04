pipeline {
    agent any
    environment {
        APP_NAME       = "aceest-fitness"
        IMAGE_TAG      = "${APP_NAME}:${BUILD_NUMBER}"
        FLASK_PORT     = "5000"
        CONTAINER_NAME = "aceest-live"
        PYTHON         = "C:\\Users\\7349502\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
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
                bat 'git log --oneline -5'
            }
        }
        stage('Setup Python') {
            steps {
                bat '''
                    %PYTHON% --version
                    %PYTHON% -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install --upgrade pip --quiet
                    pip install -r requirements.txt --quiet
                    pip install flake8 --quiet
                '''
            }
        }
        stage('Lint') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    flake8 app.py --max-line-length=120 --count
                    echo Lint passed!
                '''
            }
        }
        stage('Unit Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate.bat
                    pytest tests/test_app.py -v --cov=app --cov-report=term-missing --junitxml=test-results.xml
                '''
            }
        }
        stage('Docker Build') {
            steps {
                bat '''
                    docker build -t %IMAGE_TAG% .
                    docker tag %IMAGE_TAG% %APP_NAME%:latest
                    echo Docker image built: %IMAGE_TAG%
                '''
            }
        }
        stage('Deploy') {
            steps {
                bat '''
                    docker stop %CONTAINER_NAME% 2>nul || exit /b 0
                    docker rm %CONTAINER_NAME% 2>nul || exit /b 0
                    docker run -d --name %CONTAINER_NAME% -p %FLASK_PORT%:5000 --restart unless-stopped %IMAGE_TAG%
                    timeout /t 10 /nobreak
                    curl --fail http://localhost:%FLASK_PORT%/health
                    echo Deployment successful!
                '''
            }
        }
        stage('Smoke Test') {
            steps {
                bat '''
                    curl --fail http://localhost:%FLASK_PORT%/
                    echo Smoke test passed!
                '''
            }
        }
    }
    post {
        success {
            echo "BUILD #${BUILD_NUMBER} SUCCEEDED"
        }
        failure {
            echo "BUILD #${BUILD_NUMBER} FAILED"
        }
        always {
            bat 'if exist test-results.xml del test-results.xml'
            bat 'if exist venv rmdir /s /q venv'
        }
    }
}