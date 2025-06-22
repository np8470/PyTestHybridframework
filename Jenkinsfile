pipeline {
    agent any

    environment {
        VENV = ".venv"
        REPORT_DIR = "Reports"
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-creds', url: 'https://github.com/np8470/PyTestHybridframework.git'
            }
        }

        stage('Set up Python Env') {
            steps {
                bat "python -m venv %VENV%"
                bat ".venv\\Scripts\\activate && pip install --upgrade pip && pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                bat ".venv\\Scripts\\activate && pytest -s -v -m regression --html=%REPORT_DIR%\\report.html testCases/"
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML([
                    reportDir: "${env.REPORT_DIR}",
                    reportFiles: 'report.html',
                    reportName: 'PyTest HTML Report',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: false
                ])
            }
        }
    }

    post {
        always {
            emailext(
                subject: "PyTest Framework Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: """
                    <p>Build Result: <b>${currentBuild.currentResult}</b></p>
                    <p>Job: ${env.JOB_NAME}</p>
                    <p>Report: <a href="${env.BUILD_URL}PyTest%20HTML%20Report">View Report</a></p>
                """,
                mimeType: 'text/html',
                to: 'nirajpatel8470@gmail.com',
                attachmentsPattern: 'Reports/report.html'
            )
        }
    }
}
