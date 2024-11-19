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
//                 sh "echo 'hello world' > example.txt"

                upload apiSpecFilePath: "api-spec/openapi---1.0.7.yaml",
                 categoriesFilePath: "categories.json",
                 orgId: "a541ecba-4afe-4ce2-a4bb-7c8849912c7f",
                 assetId: "od-demo",
                 clientId: "9d86c5d7bcb6405bab5f66db454fb7d",
                 clientSecret: "0620101761de45ff87837B4D7068bd56"
            }
        }


    }

    post {
        always {
//             Clean up workspace
            cleanWs()
        }
    }
}
