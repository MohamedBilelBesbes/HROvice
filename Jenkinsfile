pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhubtoken')
    }
    stages {
        stage('Ansible Stage') {
            steps {
                sshUserPrivateKey(credentialsId : ['ansible-ssh-conncetion'], keyFileVariable: '~') {
                    sh 'ansible-playbook -i /opt/kubernetes/hosts /opt/kubernetes/deploy-playbook.yml'
                    sh 'ansible-playbook -i /opt/kubernetes/hosts /opt/kubernetes/service-playbook.yml'
                }
            }
        }
        stage('Dockerization') {
            steps {
                sh 'ls -l'
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker-compose build'
                sh 'docker tag hrovice_newdockerization2_web:latest mohamedbilelbesbes/hrovice_trial2'
                sh 'docker push mohamedbilelbesbes/hrovice_trial2'
            }
        }
    }
}
