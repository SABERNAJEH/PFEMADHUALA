pipeline {
    agent any

    environment {
      
        // Email recipients for notifications
        EMAIL_RECIPIENTS = 'saber.fraj@etudiant-isi.utm.tn, najah.wchem@etudiant-isi.utm.tn'
    }

    triggers {
        // Poll SCM to check for changes (e.g., merged pull requests)
        pollSCM('H/5 * * * *') // Poll every 5 minutes
    }

    stages {
        stage('Check for Merged Pull Requests') {
            steps {
                script {
                    // Fetch the latest changes from the repository
                    sh 'git fetch origin'

                    // Check for merged pull requests
                    def mergedPRs = sh(script: 'git log --merges --pretty=format:"%h - %an, %ar : %s"', returnStdout: true).trim()

                    if (mergedPRs) {
                        echo "Merged Pull Requests:\n${mergedPRs}"

                        // Send Slack notification
                        slackSend(
                            channel: '#dev-team',
                            message: "🚀 New Pull Request Merged!\n${mergedPRs}",
                            color: 'good'
                        )

                        // Send email notification
                        emailext(
                            subject: '🚀 New Pull Request Merged!',
                            body: "The following pull requests have been merged:\n\n${mergedPRs}",
                            to: "${EMAIL_RECIPIENTS}"
                        )
                    } else {
                        echo "No new pull requests merged."
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded. Notifications sent if any PRs were merged."
        }
        failure {
            echo "Pipeline failed. Check the logs for details."
        }
    }
}
