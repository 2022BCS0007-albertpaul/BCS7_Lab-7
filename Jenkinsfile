pipeline {
    agent any

    environment {
        IMAGE = "albertpaulbcs7/lab6-model:latest"
        CONTAINER = "lab7-test-container"
        PORT = "5000"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh 'docker pull $IMAGE'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f $CONTAINER || true
                docker run -d -p $PORT:5000 --name $CONTAINER $IMAGE
                '''
            }
        }

        stage('Wait for API Readiness') {
            steps {
                sh '''
                timeout=30
                until curl -s -o /dev/null -w "%{http_code}" http://host.docker.internal:$PORT/health | grep -q 200
                do
                    if [ $timeout -le 0 ]; then
                        echo "API did not start"
                        exit 1
                    fi
                    sleep 2
                    timeout=$((timeout-2))
                done
                echo "API is ready"
                '''
            }
        }

        stage('Valid Inference Test') {
            steps {
                sh '''
                response=$(curl -s -X POST http://host.docker.internal:$PORT/predict \
                -H "Content-Type: application/json" \
                -d @tests/valid_input.json)

                echo "Valid Response: $response"

                echo "$response" | grep -q "prediction" || exit 1
                echo "Valid input test passed"
                '''
            }
        }

        stage('Invalid Input Test') {
            steps {
                sh '''
                status=$(curl -s -o /dev/null -w "%{http_code}" \
                -X POST http://host.docker.internal:$PORT/predict \
                -H "Content-Type: application/json" \
                -d @tests/invalid_input.json)

                if [ "$status" -eq 200 ]; then
                    echo "Invalid input should not return 200"
                    exit 1
                fi

                echo "Invalid input correctly rejected"
                '''
            }
        }

        stage('Stop Container') {
            steps {
                sh '''
                docker stop $CONTAINER || true
                docker rm $CONTAINER || true
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f $CONTAINER || true'
        }
    }
}