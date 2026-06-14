pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest tests/test_model.py'
            }
        }

        stage('Retrain Model') {
            steps {
                sh 'python3 src/retrain.py'
            }
        }
    }
}