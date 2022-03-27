node("EC2") {

    stage('Hello') {
        echo "Hello World ${env.BUILD_NUMBER}"
        sh "sudo su -"
        sh "cd /home/ec2-user/jenkins/jenkins/workspace/Pipline_test"
    }

    dir("${env.BUILD_NUMBER}"){
    stage("git clone"){
        sh "git clone https://github.com/shaygef123/StickyNoteAPP.git"
    }

    stage('List Files') {
        sh "ls StickyNoteAPP"
    }

    stage('building and deploying') {
        sh "pwd"
        sh "sudo docker build -t stickynote_app StickyNoteAPP/ "
        sh "sudo /usr/local/bin/docker-compose -f StickyNoteAPP/StickyNoteAPP.yaml up -d"
    }

    stage('testing') {
        def (check,code)=sh(script: "curl -I http://localhost:2999/home | grep HTTP", returnStdout: true).trim()
            .tokenize("HTTP/")


        if (check.contains("200") || check.contains("403")){
            println("successfully")
        }
        else{
            println("$check")
        }

    }

    }
}
