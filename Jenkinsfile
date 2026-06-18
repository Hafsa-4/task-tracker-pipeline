pipeline {
  agent any
  environment {
    ECR = "<account-id>.dkr.ecr.us-east-1.amazonaws.com"
  }
  stages {
    stage("Build & Push") {
      steps {
        script { env.TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim() }
        sh "docker build -t ${ECR}/task-tracker:${TAG} ./app"
        sh "docker push ${ECR}/task-tracker:${TAG}"
      }
    }
    stage("Approve") {
      steps { input "Deploy ${env.TAG}?" }
    }
    stage("Deploy") {
      steps {
        sh "ansible-playbook -i ansible/inventory.ini ansible/deploy.yml -e image_tag=${env.TAG} -e ecr_registry=${ECR}"
      }
    }
  }
}
