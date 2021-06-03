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
                sh "docker build -t global_touch/base ."
            }
        }

        stage('Deploying staging') {
            when {
                expression { env.GIT_BRANCH == 'origin/master' }
            }

            stages {
                stage('Copying the .env file') {
                    steps {
                        sh "cp ./environments/.env.staging ./.env"
                        sh "cp ./environments/.env.staging ./src/.env"
                    }
                }

                stage('Running the staging service') {
                    steps {
                        sh "docker-compose -p staging up -d --no-deps app"
                        sh "docker-compose -p staging up -d --no-deps beat"
                        sh "docker-compose -p staging up -d --no-deps worker"
                    }
                }
            }
        }

        stage('Deploying production') {
            when {
                expression { env.GIT_BRANCH == 'origin/production' }
            }

            stages {
                stage('Copying the .env file') {
                    steps {
                        sh "cp ./environments/.env.production ./.env"
                        sh "cp ./environments/.env.production ./src/.env"
                    }
                }

                stage('Running the production service') {
                    steps {
                        sh "docker-compose -p production up -d --no-deps app"
                        sh "docker-compose -p production up -d --no-deps beat"
                        sh "docker-compose -p production up -d --no-deps worker"
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