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
                script {
                    // Use the 'Secret File' ID you created in Jenkins
                    withCredentials([file(credentialsId: 'k3s-config', variable: 'KUBECONFIG')]) {
                        // We pass the file directly to the kubectl command
                        sh "kubectl --kubeconfig=${KUBECONFIG} apply -f deployment.yaml"
                        
                        // This ensures K3s pulls the newest image even if the tag is 'latest'
                        sh "kubectl --kubeconfig=${KUBECONFIG} rollout restart deployment/flask-app"
                    }
                }
            }
        }
