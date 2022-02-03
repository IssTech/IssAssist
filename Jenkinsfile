pipeline {
 agent {
  kubernetes {
    label "issassist-${UUID.randomUUID().toString()}"
    yaml '''
      apiVersion: v1
      kind: Pod
      metadata:
      labels:
        component: ci
      spec:
        containers:
        - name: jnlp
          image: jenkins/inbound-agent:4.11-1
        - name: python
          image: python:3
          imagePullPolicy: IfNotPresent
          command:
          - cat
          tty: true
          volumeMounts:
          - name: workspace-volume
            mountPath: /home/jenkins/python
            readOnly: false
        - name: kaniko
          image: gcr.io/kaniko-project/executor:debug
          imagePullPolicy: IfNotPresent
          command:
          - sleep
          args:
          - 999999
          volumeMounts:
          - name: kaniko-secret
            mountPath: /kaniko/.docker
          - name: workspace-volume
            mountPath: /home/jenkins/kaniko
            readOnly: false
        restartPolicy: Never
        dnsConfig:
          options:
          - name: ndots
            value: "1"
        volumes:
        - name: kaniko-secret
          secret:
              secretName: dockercred
              items:
              - key: .dockerconfigjson
                path: config.json
        - emptyDir:
            medium: ""
          name: "workspace-volume"
      '''
    }
  }

 environment {
    DOCKER_ORGANIZATION_NAME = "isstech"
    SERVICE_NAME = "issassist"
    GIT_ORGANIZATION_NAME = "IssTech"
    DOCKER_REGISTRY = "$DOCKER_ORGANIZATION_NAME/$SERVICE_NAME"
    PROD_NAMESPACE = "issassist-prod"
    PROD_URL = "issassist.isstech.local"
    TEST_NAMESPACE = "issassist-test"
    TEST_URL = "issassist-test.isstech.local"
    ANNOTATIONS = "kubernetes.io/ingress.class: traefik"
 }

 stages {
  stage('Get our Django Project going') {
    steps {
      container('jnlp') {
      sh 'echo "##### DOWNLOADING GITHUB REPO $GIT_BRANCH #####"'
      git url: GIT_URL, branch: GIT_BRANCH
      }
    }
  }

  stage('Test and Build $DOCKER_SERVICE_NAME'){
    steps {
      container('python') {
        sh 'chmod +x ./jenkins/test.sh && ./jenkins/test.sh'
        sh 'chmod +x ./jenkins/helm.sh && ./jenkins/helm.sh'
        sh 'chmod +x ./jenkins/kube.sh && ./jenkins/kube.sh'
      }
    }
  }

  stage('Build and Push main image to Docker Hub') {
    when { branch 'main' }
      steps {
        container('kaniko') {
          sh '''
            /kaniko/executor --context git://github.com/$DOCKER_REGISTRY.git#refs/heads/$GIT_BRANCH --destination $DOCKER_REGISTRY:$GIT_TAG --destination $DOCKER_REGISTRY:latest
          '''
        }
      }
  }

  stage('Build and Push image to Docker Hub') {
    when { not { branch 'main' } }
      steps {
        container('kaniko') {
          sh '''
            /kaniko/executor --context git://github.com/$DOCKER_REGISTRY.git#refs/heads/$GIT_BRANCH --destination $DOCKER_REGISTRY:$GIT_BRANCH
          '''
        }
      }
  }

  stage('Deploy Code to Prod Environment') {
    when { branch 'main' }
    steps {
      container('python') {
        withKubeConfig([credentialsId: 'k3s-jenkins-sa', serverUrl: 'https://192.168.55.21:6443']) {
        sh '''
           helm upgrade $SERVICE_NAME ./deployment/helm/ \
           --set ingress.enabled=True \
           --set ingress.hosts[0].host=$PROD_URL \
           --set ingress.hosts[0].paths[0].path=/ \
           --set ingress.hosts[0].paths[0].pathType=ImplementationSpecific  \
           --set nginx.hosts=$PROD_URL \
           --set ingress.metadata.annotations="$ANNOTATIONS" \
           --set issassist.backend.image.tag=$GIT_BRANCH \
           --set issassist.backend.image.pullPolicy=Always \
           --namespace=$PROD_NAMESPACE \
           --create-namespace \
           --wait
         '''
        }
      }
    }
  }

  stage('Deploy Code to Test Environment') {
    when { not { branch 'main' } }
    steps {
      container('python') {
        withKubeConfig([credentialsId: 'k3s-jenkins-sa', serverUrl: 'https://192.168.55.21:6443']) {
        sh 'helm uninstall $SERVICE_NAME --namespace $TEST_NAMESPACE --wait || true'
        sh '''
           helm install $SERVICE_NAME ./deployment/helm/ \
           --set ingress.enabled=True \
           --set ingress.hosts[0].host=$TEST_URL \
           --set ingress.hosts[0].paths[0].path=/ \
           --set ingress.hosts[0].paths[0].pathType=ImplementationSpecific  \
           --set ingress.metadata.annotations="$ANNOTATIONS" \
           --set issassist.backend.image.tag=$GIT_BRANCH \
           --set issassist.backend.image.pullPolicy=Always \
           --namespace=$TEST_NAMESPACE \
           --create-namespace \
           --wait
         '''
        }
      }
    }
  }

  stage('Test and Main Deployment ') {
    when { branch 'main' }
      steps {
        container('python') {
          sh ' curl $PROD_URL '
      }
    }
  }

  stage('Test and Decommission our deployment ') {
    when { not { branch 'main' } }
      steps {
        container('python') {
          withKubeConfig([credentialsId: 'k3s-jenkins-sa', serverUrl: 'https://192.168.55.21:6443']) {
            sh '''
              curl $TEST_URL
              helm uninstall $SERVICE_NAME --namespace=$TEST_NAMESPACE --wait
              ./kubectl delete namespace $TEST_NAMESPACE

            '''
          }
        }
      }
  }
 }
}
