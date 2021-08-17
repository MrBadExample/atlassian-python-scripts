import os
import requests


url1 = "http://10.9.8.3:8080"
url2 = "http://10.9.8.4:8080"
login = "admin"
password = "admin"
headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
    }

project_key = "TEST"


# Find all issues in the project that contain attachments
def list_issues_with_attachements(project_key, url):
    payload = "{\n\t\"jql\": \"Project=" + project_key + " and attachments is not EMPTY\"\n}"
    respone = requests.request("POST", 
    url+"/rest/api/2/search",
    auth=(login, password), 
    data=payload, 
    headers=headers)
    issue_list = []
    for issue in respone.json()["issues"]:
        issue_list.append(issue["key"])
    return issue_list

# Create a list with all attachements
def list_all_attachments(source_jira_url, issue_key):
    issue_response = requests.request("GET",
        source_jira_url + "/rest/api/2/issue/" + issue_key,
        auth=(login, password),
        headers=headers
    )
    return issue_response.json()["fields"]["attachment"]

# Upload attachments from my device
def upload_attachment(url, issue_key, file_name):
    headers = {
    'X-Atlassian-Token': 'no-check',
    }
    files = {
    'file': (file_name, open(file_name, 'rb')),
    }
    upload_response = requests.post(
        url + '/rest/api/2/issue/' + issue_key + '/attachments',
        headers=headers,
        files=files, 
        auth=(login, password))
    if(upload_response.status_code == 200):
        print("'" + file_name + "' uploaded to " + issue_key)



def copy_attachements(source_jira_url, target_jira_url, issue_key):
    attachments = list_all_attachments(source_jira_url, issue_key)
    for attachment in attachments:
        file_url = attachment["content"]
        file_name = attachment["filename"]
        download_response = requests.get(file_url, 
            auth=(login, password), 
            stream=True)
        
        # Save the attchment on the device
        with open(file_name, "wb") as f: 
            f.write(download_response.content)
        f.close()

        # Upload attchment
        upload_attachment(target_jira_url, issue_key, file_name)

        # Remove attachments from device
        os.remove(file_name)




for issue_key in list_issues_with_attachements(project_key, url1):
   copy_attachements(url1, url2, issue_key)
