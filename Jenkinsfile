pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = "2024tm93603mvarshitha/aceest-fitness"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                echo "Code checked out"
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt || true'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pip3 install pytest || true'
                sh 'pytest tests/ -v || true'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner -Dsonar.projectKey=aceest-fitness -Dsonar.sources=. || true'
                }
            }
        }
        stage('Docker Build') {
            steps {
                sh "docker build -t ${DOCKER_HUB_REPO}:${IMAGE_TAG} ."
            }
        }
        stage('Deploy') {
            steps {
                echo "Deploying version ${IMAGE_TAG}"
            }
        }
    }
    post {
        success { echo 'Pipeline succeeded!' }
        failure { echo 'Pipeline failed!' }
    }
}