def namespace = '**************'
def context = '*******'
def project = 'HELMDEPL'
String jobFolder = "${namespace}/helm"
String jobName = "deploy-iapi-supporting-chart-prs-dev"

pipelineJob(jobFolder + '/' + jobName) {
	displayName(jobName)
	description('Executed at 8:10am every weekday - This job deploys all selected charts and their chart versions into your selected environment and displays the results in #prs-notifications -' + jobName)

	triggers {
		cron('10 8 * * 1-5')
	}

	parameters {
        choiceParam('CONTEXT', [context])
		choiceParam('NAMESPACE', [namespace])
		choiceParam('GIT_PROJECT', [project])
		choiceParam('GIT_REPO', ['ida-supporting-charts-cw'])
		choiceParam('SLACK_URL', ['https://hooks.slack.com/services/************************'])
		choiceParam('SLACK_FAILURE_MESSAGE')
		stringParam('HELM_CHART_BRANCH', 'develop', 'This is the branch of the ida-supporting-charts repo to deploy from')
		textParam {
			name('CHARTS')
			defaultValue('identity-api-simulator')
			description('Charts to deploy')
		}
		textParam {
			name('DOCKER_IMAGE_TAG')
			defaultValue('ida-pcdp-stub:latest\n' +
					'ida-dependency-stub:latest\n' +
					'')
			description('Images to deploy. These override the chart\'s Chart.yaml appVersion. Specify <chart-name>:<image> where image can be [ latest | ida-xxxxx | x.y.z | r-x.y ]) eg. pcu-chart:1.2.3 or pcu-chart:latest')
		}
	}

	definition {
		cpsScm {
			scm {
				git {
					remote {
						url('ssh://git@bitbucket.ipttools.info/iptdeploy/ipt-jenkins-pipeline-shared-resources.git')
						credentials('************************')
					}
					branch('ida-devops/v4.0')
				}
			}

			scriptPath('src/uk/gov/ipt/ida/devops/jenkins/deploy/Jenkinsfile-deploy-from-repo')
		}
	}
}