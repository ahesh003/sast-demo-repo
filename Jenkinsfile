// pipeline {
//     agent any

//     environment {
//         RABBITMQ_HOST = "host.docker.internal"
//         RABBITMQ_PORT = "5672"
        
//     }

//     stages {

//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Prepare SAST Job') {
//             steps {
//                 script {
//                     def jobId = UUID.randomUUID().toString()
//                     def repoUrl = env.GIT_URL
//                     def branch = env.GIT_BRANCH.replace("origin/", "")

//                     writeFile file: 'scan_job.json', text: """
//                     {
//                         "job_id": "${jobId}",
//                         "scan_type": "sast",
//                         "repo": {
//                             "type": "git",
//                             "url": "${repoUrl}",
//                             "branch": "${branch}"
//                         },
//                         "rules_path": "/rules/semgrep-rules"
//                     }
//                     """

//                     env.SAST_JOB_ID = jobId
//                 }
//             }
//         }

//         stage('Publish To RabbitMQ') {
//             steps {
//                 withCredentials([usernamePassword(
//                     credentialsId: 'rabbitmq-creds',
//                     usernameVariable: 'RABBITMQ_USER',
//                     passwordVariable: 'RABBITMQ_PASS'
//                 )]) {
//                     sh """
//                     python3 publish_job.py scan_job.json
//                     """
//                 }
//             }
//         }
//     }

//     post {
//         success {
//             echo "SAST Job ${env.SAST_JOB_ID} successfully queued"
//         }
//         failure {
//             echo "SAST Job failed to queue"
//         }
//     }
// }
// -----------------------------------------------------------------------------------------------------------

// pipeline {
//     agent {
//         docker {
//             image 'python:3.11'
//             args '-u root'
//         }
//     }

//     environment {
//         RABBITMQ_HOST = "host.docker.internal"
//         RABBITMQ_PORT = "5672"
//     }

//     stages {

//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Install Dependencies') {
//             steps {
//                 sh 'pip install --no-cache-dir -r requirements.txt'
//             }
//         }

//         stage('Prepare SAST Job') {
//             steps {
//                 script {
//                     def jobId = UUID.randomUUID().toString()
//                     def repoUrl = env.GIT_URL
//                     def branch = env.GIT_BRANCH.replace("origin/", "")

//                     writeFile file: 'scan_job.json', text: """
//                     {
//                         "job_id": "${jobId}",
//                         "scan_type": "sast",
//                         "repo": {
//                             "type": "git",
//                             "url": "${repoUrl}",
//                             "branch": "${branch}"
//                         },
//                         "rules_path": "/rules/semgrep-rules"
//                     }
//                     """

//                     env.SAST_JOB_ID = jobId
//                 }
//             }
//         }

//         stage('Publish To RabbitMQ') {
//             steps {
//                 withCredentials([usernamePassword(
//                     credentialsId: 'rabbitmq-creds',
//                     usernameVariable: 'RABBITMQ_USER',
//                     passwordVariable: 'RABBITMQ_PASS'
//                 )]) {
//                     sh 'python publish_job.py scan_job.json'
//                 }
//             }
//         }
//     }

//     post {
//         success {
//             echo "SAST Job ${env.SAST_JOB_ID} successfully queued"
//         }
//         failure {
//             echo "SAST Job failed to queue"
//         }
//     }
// }
// ---------------------------------------------------------------------------------------Jenkins-> ARMOR-> RabbitMQ -----------------------------------------
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Trigger SAST via ARMOR API') {
            steps {
                script {
                    def repoUrl = env.GIT_URL
                    def branch = env.GIT_BRANCH.replace("origin/", "")

                    sh """
                    curl -X POST http://host.docker.internal:8000/api/v2/sast/trigger \
                    -H "Content-Type: application/json" \
                    -d '{
                        "repo_url": "${repoUrl}",
                        "branch": "${branch}"
                    }'
                    """
                }
            }
        }
    }

    post {
        success {
            echo "SAST trigger request sent to ARMOR"
        }
        failure {
            echo "Failed to trigger SAST via ARMOR"
        }
    }
}

