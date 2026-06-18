pipeline {
  agent any
  stages {
    stage("Build") {
      steps {
        script { env.TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim() }
        sh "docker build -t task-tracker:${env.TAG} ./app"
        sh "docker save task-tracker:${env.TAG} -o /tmp/task-tracker-${env.TAG}.tar"
      }
    }
    stage("Approve") {
      steps { input "Deploy ${env.TAG}?" }
    }
    stage("Deploy") {
      steps {
        sh """
          ansible-playbook ansible/deploy.yml \
            -i ansible/inventory.ini \
            --extra-vars "image_tag=${env.TAG}"
        """
      }
    }
  }
}
