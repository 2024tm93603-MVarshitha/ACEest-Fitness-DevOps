pipeline {
    agent any
    environment {
        APP_NAME       = "aceest-fitness"
        FLASK_PORT     = "5000"
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
        stage('Docker Verify') {
            steps {
                echo 'Docker image build is validated via GitHub Actions CI/CD pipeline.'
                echo 'Docker Desktop restricted on this build machine - verified in GitHub Actions.'
                bat 'docker --version'
            }
        }
    }
    post {
        success {
            echo "BUILD #${BUILD_NUMBER} SUCCEEDED - All stages passed!"
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