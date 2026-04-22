pipeline {
    agent any

    environment {
        REGISTRY = "192.168.1.27:8082"
        IMAGE = "${REGISTRY}/flask-test:${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                sh "docker build -t ${IMAGE} ."
            }
        }

        stage('Push to Nexus') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'nexus-docker-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh "echo ${PASS} | docker login ${REGISTRY} -u ${USER} --password-stdin"
                    sh "docker push ${IMAGE}"
                }
            }
        }

        stage('Deploy to K3s') {
            steps {
                withCredentials([file(credentialsId: 'k3s-config', variable: 'KUBECONFIG')]) {

                    // Update image dynamically in deployment
                    sh """
                    kubectl --kubeconfig=${KUBECONFIG} set image deployment/flask-app \
                    flask-container=${IMAGE}
                    """

                    // Ensure rollout
                    sh "kubectl --kubeconfig=${KUBECONFIG} rollout status deployment/flask-app"
                }
            }
        }
    }
}
