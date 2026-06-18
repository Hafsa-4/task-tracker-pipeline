pipeline {
  agent any
  stages {
    stage("Build") {
      steps {
        script { env.TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim() }
        sh "docker build -t task-tracker:${env.TAG} ./app"
      }
    }
    stage("Approve") {
      steps { input "Deploy ${env.TAG}?" }
    }
    stage("Deploy") {
      steps {
        sh "docker rm -f task-tracker || true"
        sh "docker run -d --name task-tracker -p 5000:5000 -e DYNAMODB_TABLE=tasks -e AWS_REGION=us-east-1 -e AWS_ACCESS_KEY_ID=${env.AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${env.AWS_SECRET_ACCESS_KEY} task-tracker:${env.TAG}"
      }
    }
  }
}
