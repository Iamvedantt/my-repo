pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build Image') {
            steps {
                sh "docker build -t 192.168.1.27:8082/flask-test:latest ."
            }
        }
        stage('Push to Nexus') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'nexus-docker-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "docker login -u ${USER} -p ${PASS} 192.168.1.27:8082"
                    sh "docker push 192.168.1.27:8082/flask-test:latest"
                }
            }
        }
        stage('Deploy to K3s') {
            steps {
                withKubeConfig([credentialsId: 'k3s-config']) {
                    sh "kubectl apply -f deployment.yaml"
                }
            }
        }
    }
}
