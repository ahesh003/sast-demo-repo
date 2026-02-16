pipeline {
    agent any

    environment {
        RABBITMQ_HOST = "host.docker.internal"
        RABBITMQ_PORT = "5672"
        
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare SAST Job') {
            steps {
                script {
                    def jobId = UUID.randomUUID().toString()
                    def repoUrl = env.GIT_URL
                    def branch = env.GIT_BRANCH.replace("origin/", "")

                    writeFile file: 'scan_job.json', text: """
                    {
                        "job_id": "${jobId}",
                        "scan_type": "sast",
                        "repo": {
                            "type": "git",
                            "url": "${repoUrl}",
                            "branch": "${branch}"
                        },
                        "rules_path": "/rules/semgrep-rules"
                    }
                    """

                    env.SAST_JOB_ID = jobId
                }
            }
        }

        stage('Publish To RabbitMQ') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'rabbitmq-creds',
                    usernameVariable: 'RABBITMQ_USER',
                    passwordVariable: 'RABBITMQ_PASS'
                )]) {
                    sh """
                    python3 ci/publish_to_rabbitmq.py scan_job.json
                    """
                }
            }
        }
    }

    post {
        success {
            echo "SAST Job ${env.SAST_JOB_ID} successfully queued"
        }
        failure {
            echo "SAST Job failed to queue"
        }
    }
}
