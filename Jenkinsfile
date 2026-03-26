pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt || true'
            }
        }

        stage('Run Project') {
            steps {
                sh 'python main.py || true'
            }
        }
    }
}
