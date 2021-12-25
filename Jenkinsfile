pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhubtoken')
    }
    stages {
        stage('pre Ansible Stage') {
            sh 'sshpass -p \'ansadmin\' ssh ansadmin@172.31.91.173 ansible-playbook -i /opt/kubernetes/hosts /opt/kubernetes/deploy-playbook.yml'
        }
        stage('Ansible Stage') {
            steps {
                sshagent(credentials : ['ansible-ssh-connection']) {
                    sh 'sshpass -p \'ansadmin\' ssh ansadmin@172.31.91.173 ansible-playbook -i /opt/kubernetes/hosts /opt/kubernetes/deploy-playbook.yml'
                    sh 'sshpass -p \'ansadmin\' ssh ansadmin@172.31.91.173 ansible-playbook -i /opt/kubernetes/hosts /opt/kubernetes/service-playbook.yml'
                }
            }
        }
        stage('Dockerization') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker-compose build'
                sh 'docker tag hrovice_newdockerization2_web:latest mohamedbilelbesbes/hrovice_trial2'
                sh 'docker push mohamedbilelbesbes/hrovice_trial2'
            }
        }
    }
}
