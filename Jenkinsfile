pipeline {
  agent any
  
  environment {
      PYTHON_VERSION = '3.13'
      PROJECT_NAME = 'finance'
  }
  
  stages {
    stage('Checkout') {
      steps {
          checkout scm
      }
    }
    
    stage('Setup') {
        steps {
            sh '''
                pyenv install ${PYTHON_VERSION}
                pyenv global ${PYTHON_VERSION}
                
                curl -LsSf https://astral.sh/uv/install.sh | sh
                source ~/.cargo/env
            '''
        }
    }
    
    stage('Dependencies') {
        steps {
            sh '''
                source ~/.cargo/env
                uv venv .venv
                source .venv/bin/activate
                uv sync --no-dev
            '''
        }
    }
    
    stage('Test') {
        steps {
            sh '''
                source .venv/bin/activate
                python -m pytest tests/ -v --tb=short
            '''
        }
    }
    
    stage('Build') {
        steps {
            sh '''
                source .venv/bin/activate
                uv pip install --no-deps -e .
            '''
        }
    }
    
    stage('Docker Build') {
        steps {
            sh '''
                docker build -t ${PROJECT_NAME}:latest .
            '''
        }
    }
  }
  
  post {
    always {
        sh '''
            if [ -f .venv/bin/activate ]; then
                . .venv/bin/activate
                echo "Test results:"
                python -m pytest tests/ -v --tb=short --junitxml=test-results.xml
                mkdir -p test-reports
                cp test-results.xml test-reports/
            fi
        '''
        archiveArtifacts artifacts: 'test-reports/*.xml', allowEmptyArchive: true
    }
    
    success {
        echo 'Pipeline succeeded!'
    }
    
    failure {
        echo 'Pipeline failed!'
    }
  }
}
