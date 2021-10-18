import requests
import csv

url = "http://10.9.8.3:8080"

login = "admin"
password = "admin"
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
}


def add_component(component_name, description, lead_name, assigneeType, isAssigneeTypeValid, project_key):
    payload = "{\n\"name\": \"" + component_name + \
              "\",\n\"description\": \"" + description + \
              "\",\n\"leadUserName\": \"" + lead_name + \
              "\",\n\"assigneeType\": \"" + assigneeType + \
              "\",\n\"isAssigneeTypeValid\": " + isAssigneeTypeValid + \
              ",\n\"project\": \"" + project_key + \
              "\"\n}"

    response = requests.request("POST",
                                url + "/rest/api/2/component",
                                auth=(login, password),
                                data=payload,
                                headers=headers)
    if response.status_code == 201:
        print("Component: '" + component_name + "' has been added to project: " + project_key)
    elif response.status_code == 400:
        print("Component: '" + component_name + "' already exist in project: " + project_key)
    return True


with open('list_of_components.csv', 'r') as csvfile:
    next(csvfile)
    data_reader = csv.reader(csvfile)
    for row in data_reader:
        add_component(row[0], row[1], row[2], row[3], row[4], row[5])
