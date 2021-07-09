/*
James Sandford, copyright BBC 2020

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

@Library("rd-apmm-groovy-ci-library@v1.x") _

/*
 Runs the following steps in parallel and reports results to GitHub:
 - Lint using flake8 and mypy
 - Run Python 3 unit tests in tox
 - Build Debian packages for supported Ubuntu versions

 If these steps succeed and the master branch is being built, wheels and debs are uploaded to Artifactory and the
 R&D Debian mirrors.

 Optionally you can set FORCE_PYUPLOAD to force upload to Artifactory, and FORCE_DEBUPLOAD to force Debian package
 upload on non-master branches.
*/

pipeline {
    agent {
        label "apmm-slave"
    }
    options {
        ansiColor('xterm') // Add support for coloured output
        buildDiscarder(logRotator(numToKeepStr: '10')) // Discard old builds
        timeout(time: 30, unit: 'MINUTES')
    }
    parameters {
        booleanParam(name: "FORCE_PYUPLOAD", defaultValue: false, description: "Force Python artifact upload")
        booleanParam(name: "FORCE_DEBUPLOAD", defaultValue: false, description: "Force Debian package upload")
        booleanParam(name: "RUN_UNIT_TESTS", defaultValue: true, description: "Run unit tests")
    }
    environment {
        http_proxy = "${ANSIBLE_PROXY}"
        https_proxy = "${ANSIBLE_PROXY}"
        FORGE_CERT = "/etc/pki/tls/private/client_crt_key.pem"
        PATH = "$HOME/.pyenv/bin:$PATH"
    }
    stages {
        stage ("Prepare Environment") {
            stages{
                stage ("Clean Environment") {
                    steps {
                        sh 'git clean -df'
                        sh 'rm -rf /tmp/$(basename ${WORKSPACE})/'
                        sh 'make clean'
                    }
                }
                stage ("Update pyenv") {
                    steps {
                        sh "cd $HOME/.pyenv; git pull"
                    }
                }
                stage ("Configure pyenv") {
                    steps {
                        sh "pyenv install -s 3.7.5"
                        sh "pyenv local 3.7.5"
                    }
                }
            }
        }
        stage ("Tests") {
            parallel {
                stage ("Linting Check") {
                    steps {
                        script {
                            env.lint_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "tests/lint", status: "PENDING")
                        // Use a workdirectory in /tmp to avoid shebang length limitation
                        sh 'tox -e lint --recreate --workdir /tmp/$(basename ${WORKSPACE})/tox-lint'
                        script {
                            env.lint_result = "SUCCESS" // This will only run if the sh above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "tests/lint", status: env.lint_result)
                        }
                    }
                }
                stage ("Type Check") {
                    steps {
                        script {
                            env.type_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "tests/type", status: "PENDING")
                        // Use a workdirectory in /tmp to avoid shebang length limitation
                        sh 'tox -e typecheck --recreate --workdir /tmp/$(basename ${WORKSPACE})/tox-type'
                        script {
                            env.type_result = "SUCCESS" // This will only run if the sh above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "tests/type", status: env.type_result)
                        }
                    }
                }
                stage ("Unit Tests") {
                    steps {
                        script {
                            env.unittest_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "tests/unittest", status: "PENDING")
                        // Use a workdirectory in /tmp to avoid shebang length limitation
                        sh 'tox -e unittest --recreate --workdir /tmp/$(basename ${WORKSPACE})/tox-unittest'
                        script {
                            env.unittest_result = "SUCCESS" // This will only run if the sh above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "tests/unittest", status: env.unittest_result)
                        }
                    }
                }
            }
        }
        stage ("Build") {
            parallel {
                stage ("Build Debian Source") {
                    steps {
                        script {
                            env.debSourceBuild_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "deb/sourceBuild", status: "PENDING")

                        sh 'python3 ./setup.py sdist'
                        sh 'make dsc'
                        bbcPrepareDsc()
                        stash(name: "deb_dist", includes: "deb_dist/*")
                        script {
                            env.debSourceBuild_result = "SUCCESS" // This will only run if the steps above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "deb/sourceBuild", status: env.debSourceBuild_result)
                        }
                    }
                }
            }
        }
        stage ("Package") {
            parallel{
                stage ("Build py3 wheel") {
                    steps {
                        script {
                            env.py3wheel_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "wheelBuild/py3", status: "PENDING")
                        bbcMakeGlobalWheel("py3.7")
                        script {
                            env.py3wheel_result = "SUCCESS" // This will only run if the steps above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "wheelBuild/py3", status: env.py3wheel_result)
                        }
                    }
                }
                stage ("Build Deb with pbuilder") {
                    steps {
                        script {
                            env.pbuilder_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "deb/packageBuild", status: "PENDING")
                        // Build for all supported platforms and extract results into workspace
                        bbcParallelPbuild(
                            stashname: "deb_dist",
                            dists: bbcGetSupportedUbuntuVersions(
                                exclude: ["trusty"]
                                ),
                            arch: "amd64")
                        script {
                            env.pbuilder_result = "SUCCESS" // This will only run if the steps above succeeded
                        }
                    }
                    post {
                        success {
                            archiveArtifacts artifacts: "_result/**"
                        }
                        always {
                            bbcGithubNotify(context: "deb/packageBuild", status: env.pbuilder_result)
                        }
                    }
                }
            }
        }
        stage ("Upload Packages") {
            // Duplicates the when clause of each upload so blue ocean can nicely display when stage skipped
            when {
                anyOf {
                    expression { return params.FORCE_PYUPLOAD }
                    expression { return params.FORCE_DEBUPLOAD }
                    expression {
                        bbcShouldUploadArtifacts(branches: ["master"])
                    }
                }
            }
            stages {
                stage ("Upload to PyPi") {
                    when {
                        anyOf {
                            expression { return params.FORCE_PYUPLOAD }
                            expression {
                                bbcShouldUploadArtifacts(branches: ["master"])
                            }
                        }
                    }
                    steps {
                        script {
                            env.pypiUpload_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "pypi/upload", status: "PENDING")
                        bbcTwineUpload(toxenv: "py3.7", pypi: true)
                        script {
                            env.pypiUpload_result = "SUCCESS" // This will only run if the steps above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "pypi/upload", status: env.pypiUpload_result)
                        }
                    }
                }
                stage ("Upload to Artifactory") {
                    when {
                        anyOf {
                            expression { return params.FORCE_PYUPLOAD }
                            expression {
                                bbcShouldUploadArtifacts(branches: ["master"])
                            }
                        }
                    }
                    steps {
                        script {
                            env.artifactoryUpload_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "artifactory/upload", status: "PENDING")
                        bbcTwineUpload(toxenv: "py3.7")
                        script {
                            env.artifactoryUpload_result = "SUCCESS" // This will only run if the steps above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "artifactory/upload", status: env.artifactoryUpload_result)
                        }
                    }
                }
                stage ("Upload deb") {
                    when {
                        anyOf {
                            expression { return params.FORCE_DEBUPLOAD }
                            expression {
                                bbcShouldUploadArtifacts(branches: ["master"])
                            }
                        }
                    }
                    steps {
                        script {
                            env.debUpload_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "deb/upload", status: "PENDING")
                        script {
                            for (def dist in bbcGetSupportedUbuntuVersions()) {
                                bbcDebUpload(sourceFiles: "_result/${dist}-amd64/*",
                                             removePrefix: "_result/${dist}-amd64",
                                             dist: "${dist}",
                                             apt_repo: "ap/python")
                            }
                        }
                        script {
                            env.debUpload_result = "SUCCESS" // This will only run if the steps above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "deb/upload", status: env.debUpload_result)
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            bbcSlackNotify()
        }
    }
}