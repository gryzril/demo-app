pipeline {
  agent any

  environment {
      AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
      AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
      DOCKER_IMAGE_TAG = "myapp:${env.BUILD_NUMBER}"
  }

  stages {
      stage('Checkout') {
        steps {
          git 'https://github.com/yourusername/yourrepo.git'
        }
      }

      stage('Install Dependencies') {
          steps {
              script {
                  // Install dependencies for backend, frontend, and testing
                  sh 'pip install -r backend/requirements.txt'  // Install Python dependencies (including pytest)
                  sh 'npm install --prefix frontend'  // Install Node dependencies (for Playwright and frontend)
              }
          }
      }

      stage('Run Unit Tests') {
          steps {
              script {
                  // Run unit tests for the backend (using pytest)
                  sh 'pytest backend/tests --maxfail=1 --disable-warnings -q'
              }
          }
      }

      stage('Run Playwright Tests') {
          steps {
              script {
                  // Run Playwright tests for the frontend
                  sh 'npx playwright test frontend/tests'  // Assuming you have a Playwright test setup in frontend/tests
              }
          }
      }

      stage('Build Backend') {
          steps {
              dir('backend') {
                  script {
                      docker.build("backend:${DOCKER_IMAGE_TAG}")
                  }
              }
          }
      }

      stage('Build Frontend') {
          steps {
              dir('frontend') {
                  script {
                      docker.build("frontend:${DOCKER_IMAGE_TAG}")
                  }
              }
          }
      }

      stage('Terraform Apply') {
          steps {
              script {
                  sh '''
                      cd terraform
                      terraform init
                      terraform apply -auto-approve
                  '''
              }
          }
      }

      stage('Push to Docker Hub') {
          steps {
              script {
                  // Docker login (replace with your Docker Hub credentials)
                  sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                  sh 'docker push backend:${DOCKER_IMAGE_TAG}'
                  sh 'docker push frontend:${DOCKER_IMAGE_TAG}'
              }
          }
      }
  }
  post {
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
