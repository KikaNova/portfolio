def trigger_rerun_job(input_contents, payload_dict, slack_token):   
    trigger_slack_id = payload_dict['event']['user']
    message = f"<@{trigger_slack_id}>"
    extracted_namespace = input_contents.split()[-1]
    namespace_data = utils.get_jenkinsjob_data(extracted_namespace)
    slack_channel = utils.get_channel_id(extracted_namespace)
    print( slack_channel)
    ts = payload_dict["event"]["event_ts"]
    if 'thread_ts' in payload_dict['event']:
        thread_ts = payload_dict['event']['thread_ts']
    else :
        thread_ts=ts
    print("thread_ts: "+ thread_ts)
    jenkins_url = namespace_data[0]["jenkins_instance"]
    print("jenkins_url: "+ jenkins_url)
    items = input_contents.split()
    tags = [item for item in items[2:-1]]
    
    if slack_channel == payload_dict["event"]["channel"]:
        for tag in tags:
            print(tag)
            typed_tag = tag
            first_part = re.split(r"[._]", tag)[0]
            if len(re.split(r"[._]", tag)) == 1:
                tag = find_testTags(tag, extracted_namespace)
                print("post")
                print (tag)
            try:
                job_data= (list(filter(lambda y:y["name"]==first_part,namespace_data[0]["test_list"])))
                print(job_data)
                full_job_url =jenkins_url + job_data[0]["url"]
                print(full_job_url)
                test_tag = job_data[0]['param1']
                print( test_tag) 
                jenkins_message = jenkinsProcesser.trigger_job(full_job_url,True, {'SLACK_CHANNEL': slack_channel, test_tag: tag, 'THREAD_TS': thread_ts})
                print(message)
                message += "\n - Jenkins trigger: " + tag +":"+jenkins_message["message"]
            except Exception as e:
                print(e)
                print ("NoMatch")
                message += "\n - :warning: " + typed_tag + " is not configured in robby. Please use the first part of the test tag exactly."
        audit_message = f"<@{trigger_slack_id}> has run reruntest on " + extracted_namespace
        request_payload = {'token': slack_token, 'channel': utils.getAuditChannel(),'text': audit_message}
        url = "	https://slack.com/api/chat.postMessage"
        r = requests.post(url, data=request_payload)
        
        return message
    else:
        slack_channel = utils.get_channel_id(extracted_namespace)
        message = f"<@{trigger_slack_id}> Please run this command from the channel <#"+ slack_channel +">"


def get_pipelinestatus(input_contents):
    tag = input_contents.split()[2]
    title, finalString= release_note.create_release.getTestResults(tag)
    #print(title) 
    #print(finalString)

    message = title + "\n" + finalString

    return message

def deploy_autosit2_pipeline (input_contents, payload_dict, slack_token):
    trigger_slack_id = payload_dict['event']['user']
    message = f"<@{trigger_slack_id}>"
    #slack_token = 'autosit2'
    url = 'https://************/job/my_test_job'
    branch_param = input_contents.split()[-1]
    tag = input_contents.split()[2]
    jenkins_message = jenkinsProcesser.trigger_job(url,True, {'BRANCH': branch_param, 'TEST_TAGS': tag, 'BROWSERSTACK' : True})
    print(message)
    message += "\n - Jenkins trigger: " + tag +":"+jenkins_message["message"]

    
    audit_message = f"<@{trigger_slack_id}> has run deploysit2 on {branch_param}"
    request_payload = {'token': slack_token, 'channel': utils.getAuditChannel(),'text': audit_message}
    url = "	https://slack.com/api/chat.postMessage"
    r = requests.post(url, data=request_payload)

    return message