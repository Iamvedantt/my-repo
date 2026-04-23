pipeline {
    agent any

    environment {
        // Using your Stack VM Nexus IP and the Build Number for unique tagging
        DOCKER_REGISTRY = '192.168.1.27:8082'
        IMAGE_NAME = 'flask-test'
    }

    stages {
        stage('Checkout') {
            steps {
                // Pulls the code from your GitHub repo
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                script {
                    // Building with a unique tag (Build Number) and 'latest'
                    sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${env.BUILD_ID} ."
                    sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Push to Nexus') {
            steps {
                // Using the credentials you already verified are working
                withCredentials([usernamePassword(credentialsId: 'nexus-docker-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "echo ${PASS} | docker login ${DOCKER_REGISTRY} -u ${USER} --password-stdin"
                    sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${env.BUILD_ID}"
                    sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy to K3s') {
            steps {
                script {
                    // Using the Secret File credential for the Kuber VM (192.168.1.25)
                    withCredentials([file(credentialsId: 'k3s-config', variable: 'KUBECONFIG')]) {
                        
                        // 1. Apply the manifest (Creates the 'flask-app' if it doesn't exist)
                        sh "kubectl --kubeconfig=${KUBECONFIG} apply -f deployment.yaml"
                        
                        // 2. Update the image to the specific version we just pushed
                        // NOTE: This assumes your container name in deployment.yaml is 'flask'
                        sh "kubectl --kubeconfig=${KUBECONFIG} set image deployment/flask-app flask=${DOCKER_REGISTRY}/${IMAGE_NAME}:${env.BUILD_ID}"
                        
                        // 3. Verify the rollout
                        sh "kubectl --kubeconfig=${KUBECONFIG} rollout status deployment/flask-app"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Successfully deployed version ${env.BUILD_ID} to K3s!"
        }
        failure {
            echo "Pipeline failed. Check Console Output for specific errors."
        }
    }
}
