pipeline {
    agent any

    environment {
        // Destinataires des e-mails de notification
        EMAIL_RECIPIENTS = 'saber.fraj@etudiant-isi.utm.tn, najah.wchem@etudiant-isi.utm.tn'
    }

    triggers {
        // Poll SCM pour vérifier les modifications (toutes les 5 minutes)
        pollSCM('H/5 * * * *') // Vérifie toutes les 5 minutes
        // Déclencheur GitHub webhook
        githubPush()
    }

    stages {
        stage('Vérifier les modifications récentes') {
            steps {
                script {
                    try {
                        // Récupérer les dernières modifications du repository
                        sh 'git fetch origin'
                        echo "Dernières modifications récupérées avec succès."

                        // Récupérer les derniers commits (non merges)
                        def recentCommits = sh(script: 'git log --pretty=format:"%h - %an, %ar : %s" -n 5', returnStdout: true).trim()

                        if (recentCommits) {
                            echo "Derniers commits détectés :\n${recentCommits}"

                            // Envoyer un e-mail de notification
                            emailext(
                                subject: '🚀 Nouvelle modification détectée sur le repository',
                                body: """<html>
                                            <body>
                                                <h2>Nouvelle modification détectée !</h2>
                                                <p>Les derniers commits sur le repository sont :</p>
                                                <pre>${recentCommits}</pre>
                                            </body>
                                        </html>""",
                                to: "${EMAIL_RECIPIENTS}",
                                mimeType: 'text/html'
                            )
                        } else {
                            echo "Aucun nouveau commit détecté."
                        }
                    } catch (Exception e) {
                        echo "Une erreur s'est produite : ${e.message}"
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline exécuté avec succès. Les notifications ont été envoyées si des modifications ont été détectées."
        }
        failure {
            echo "Échec du pipeline. Consultez les logs pour plus de détails."
            emailext(
                subject: '🚨 Échec du pipeline !',
                body: "Le pipeline a échoué. Veuillez consulter les logs pour plus de détails.",
                to: "${EMAIL_RECIPIENTS}"
            )
        }
    }
}
