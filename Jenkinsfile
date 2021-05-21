pipeline {
    agent any

    stages {
        stage('Starting the Pipeline') {
            steps {
                slackSend (color: "#DF6B00", message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
            }
        }

        stage('Building the base image') {
            steps {
                sh "docker build -t global_touch/base -f ./deploy/Dockerfile ."
            }
        }

        stage('Deploying production') {
            when {
                expression { env.GIT_BRANCH == 'origin/production' }
            }

            stages {
                stage('Building production image') {
                    steps {
                        sh "docker-compose build -f ./deploy/docker-compose.yml --build-arg BUILD_NUMBER=${env.BUILD_NUMBER} prod_app"
                        sh "docker-compose build -f ./deploy/docker-compose.yml --build-arg BUILD_NUMBER=${env.BUILD_NUMBER} prod_celery"
                    }
                }

                stage('Running the production service') {
                    steps {
                        sh "docker-compose up -d -f ./deploy/docker-compose.yml --no-deps prod_app"
                        sh "docker-compose up -d -f ./deploy/docker-compose.yml --no-deps prod_celery"
                    }
                }
            }
        }
    }

    post {
        success {
            slackSend (color: "#2EB886", message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }

        failure {
            slackSend (color: "#B82E2E", message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
    }
}