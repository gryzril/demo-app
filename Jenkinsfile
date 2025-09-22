pipeline {
  agent any

  environment {
      AWS_REGION  = 'us-east-1'
      DOCKER_HOST = 'tcp://dind:2375'
      ECR_BACKEND   = "demo-app-backend"
      ECR_FRONTEND  = "demo-app-frontend"
  }

  options { skipDefaultCheckout(false) }

  stages {
      stage('Checkout') {
        steps { git 'https://github.com/gryzril/demo-app.git' }
      }

      stage('Set Image Tag') {
          agent any
          steps {
              script {
                env.GIT_SHA = sh(script: 'git rev-parse --short=7 HEAD', returnStdout: true).trim()
                env.IMAGE_TAG = "b${env.BUILD_NUMBER}-${env.GIT_SHA}"
              }
          }
      }

      stage('Backend unit tests') {
        steps {
            sh '''
              docker run --rm -v "$PWD:/w" -w /w python:3.12 bash -lc "
                pip install -U pip &&
                pip install -r backend/requirements.txt &&
                pytest backend/tests -q
              "
            '''
        }
      }

      stage('Run Playwright Tests') {
          steps {
            sh '''
              docker run --rm -v "$PWD/frontend:/app" -w /app mcr.microsoft.com/playwright:v1.47.2-jammy bash -lc "
                npm ci &&
                npx playwright install --with-deps &&
                npx playwright test
              "
            '''
          }
      }

      stage('Build Docker images') {
          steps {
            sh '''
              docker build -t backend:${IMAGE_TAG}  backend
              docker build -t frontend:${IMAGE_TAG} frontend
            '''
          }
      }

      stage('Terraform Apply') {
          steps {
             withCredentials([usernamePassword(credentialsId: 'aws', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                  dir('terraform') {
                    sh '''
                      terraform init -input=false
                      terraform apply -auto-approve -input=false \
                        -var="backend_image_tag=${IMAGE_TAG}" \
                        -var="db_image_tag=latest"
                    '''
                  }
              }
          }
      }

      stage('Push to ECR') {
      agent any
      environment { AWS_DEFAULT_REGION = "${AWS_REGION}" }
      steps {
        withCredentials([usernamePassword(credentialsId: 'aws', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
          script {
            // Need to add some setup

            sh """
              docker tag backend:${IMAGE_TAG}  ${registry}/${ECR_BACKEND}:${IMAGE_TAG}
              docker tag frontend:${IMAGE_TAG} ${registry}/${ECR_FRONTEND}:${IMAGE_TAG}
              docker push ${registry}/${ECR_BACKEND}:${IMAGE_TAG}
              docker push ${registry}/${ECR_FRONTEND}:${IMAGE_TAG}
            """
          }
        }
      }
    }
  }
  post {
      always  { 
          echo "Tag: ${env.IMAGE_TAG}" 
      }
      success {
          echo "Build and deploy completed successfully."
          // Send a success email?
      }
      failure {
          echo "Build or deployment failed."
          // Send a failure email?
      }
  }
}
