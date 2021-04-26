pipeline {
    agent any

    stages {
        stage('Starting the Pipeline') {
            steps {
                slackSend (color: '#DF6B00', message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
            }
        }
        
        stage('Deploying production') {
            when {
                expression { env.GIT_BRANCH == 'origin/production' }
            }
            
            stages {
                stage('Building production image') {
                    steps {
                        sh "docker-compose build --build-arg BUILD_NUMBER=${env.BUILD_NUMBER} prod_app"
                    }
                }
                
                stage('Running the production service') {
                    steps {
                        sh 'docker-compose up -d --no-deps prod_app'
                    }
                }
            }
        }
        
        stage('Deploying staging') {
            when { 
                expression { env.GIT_BRANCH == 'origin/production' }
            }
            
            stages {
                stage('Building the staging image') {
                    steps {
                        sh "docker-compose build --build-arg BUILD_NUMBER=${env.BUILD_NUMBER} stag_app"
                    }
                }
                
                stage('Running the staging service') {
                    steps {
                        sh 'docker-compose up -d --no-deps stag_app'
                    }
                }
            }
        }
    }
    
    post {
        success {
            slackSend (color: '#2EB886', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }

        failure {
            slackSend (color: '#B82E2E', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
    }
}