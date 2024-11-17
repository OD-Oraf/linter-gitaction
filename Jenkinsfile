pipeline {
    agent {
        node {
            label "agent1"
        }
    }

    environment {
        // Define environment variables
        IMAGE_NAME = 'my-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                // sh "printenv"
                // Checkout code from version control
                git branch: 'main', url: 'https://github.com/OD-Oraf/mygitactions.git'
                sh "echo 'hello world' > example.txt"
                echo "checking out code"
                greet filePath: "categories.json",
                 name: 'od',
                 orgId:"a541ecba-4afe-4ce2-a4bb-7c8849912c7f",
                 assetId: "deom"
            }
        }


    }

    post {
        always {
            // Clean up workspace
            cleanWs()
        }
    }
}
