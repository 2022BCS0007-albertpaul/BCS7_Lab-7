pipeline {
    agent any

    environment {
        IMAGE_NAME = "albertpaulbcs7/lab6-model:latest"
        CONTAINER_NAME = "lab7-test-container"
        PORT = "5000"
    }

    stages {

        stage('Stage 1: Pull Image') {
            steps {
                sh '''
                docker pull $IMAGE_NAME
                docker images | grep lab6-model
                '''
            }
        }

        stage('Stage 2: Run Container') {
            steps {
                sh '''
                docker run -d -p $PORT:5000 --name $CONTAINER_NAME $IMAGE_NAME
                docker ps | grep $CONTAINER_NAME
                '''
            }
        }

        stage('Stage 3: Wait for Service Readiness') {
            steps {
                script {
                    timeout(time: 60, unit: 'SECONDS') {
                        waitUntil {
                            def status = sh(
                                script: "curl -s -o /dev/null -w \"%{http_code}\" http://localhost:$PORT/health || true",
                                returnStdout: true
                            ).trim()
                            return (status == "200")
                        }
                    }
                }
            }
        }

        stage('Stage 4: Send Valid Inference Request') {
            steps {
                script {
                    def response = sh(
                        script: '''
                        curl -s -X POST http://localhost:$PORT/predict \
                        -H "Content-Type: application/json" \
                        -d '{
                          "fixed acidity": 7.4,
                          "volatile acidity": 0.70,
                          "citric acid": 0.00,
                          "residual sugar": 1.9,
                          "chlorides": 0.076,
                          "free sulfur dioxide": 11.0,
                          "total sulfur dioxide": 34.0,
                          "density": 0.9978,
                          "pH": 3.51,
                          "sulphates": 0.56,
                          "alcohol": 9.4
                        }'
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "Valid Response: ${response}"

                    if (!response.contains("prediction")) {
                        error("Prediction field missing in valid response")
                    }
                }
            }
        }

        stage('Stage 5: Send Invalid Request') {
            steps {
                script {
                    def response = sh(
                        script: '''
                        curl -s -X POST http://localhost:$PORT/predict \
                        -H "Content-Type: application/json" \
                        -d '{"invalid":"data"}'
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "Invalid Response: ${response}"

                    if (!response.toLowerCase().contains("error")) {
                        error("Invalid request did not return error")
                    }
                }
            }
        }

        stage('Stage 6: Stop Container') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                '''
            }
        }

        stage('Stage 7: Pipeline Result') {
            steps {
                echo "All validation tests passed successfully!"
            }
        }
    }

    post {
        always {
            sh '''
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true
            '''
        }
    }
}