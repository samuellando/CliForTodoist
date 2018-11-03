import requests, time

def genArgs(urlPath, data=None, headers=None):
    """
    THis method generates the arguments for any required request.
    """
    with open("~/.todoistApiToken", "r") as f:
        TOKEN = f.readline()

    args =  {"url":"https://beta.todoist.com/API/v8/"+urlPath, 
            "headers":{"Authorization": "Bearer %s" % TOKEN}}
    
    if data:
        args["data"] = data
    
    if headers:
        args["headers"] = {**args["headers"], **headers}
    
    return args

def doRequest(tries, code, f, args):
    """
        Higher order function that runs f as a request tries times until 
        code is returned. args is the function arguments in dictionary form.
    """
    statusCode = 404 # Default status code, will change depending on return.
    i = 1 # Start at try 1.
    while (i <= tries and statusCode != code):
        # Run the function with args.
        response = f(**args)
        # Extract the status code.
        statusCode = response.status_code 
        i += 1
        time.sleep(1)
    if (i > tries):
        # Show error message and exit.
        print("Failed to connect to todoist!")
        exit()
    else:
        # If all is good, return the responce.
        return response 

def getData():
    projects = doRequest(10, 200, requests.get, 
                genArgs("projects")).json()

    tasks = doRequest(10, 200, requests.get, 
                genArgs("tasks")).json()
    # Add date data to tasks.
    for task in tasks:
            task["date"] = doRequest(10, 200, requests.get, 
                            genArgs("tasks/"+str(task["id"]))
                                        ).json()["due"]["date"] # Extract date.
    # Simplify the ids.
    ids = []
    for project in projects:
        ids.append(project["id"])
        for task in tasks:
            if (task["project_id"] == project["id"]):
                ids.append(task["id"])
    
    return projects, tasks, ids

def addTask(content, projectId, dueString):
    doRequest(10, 200, requests.post, 
                        genArgs("tasks", data = json.dumps(
                                                    {"content": content,
                                                    "project_id": projectId, 
                                                    "due_string": dueString}
                                                    ), 
                            headers = {"Content-Type": "application/json",
                                        "X-Request-Id": str(uuid.uuid4())}))

def closeTask(taskId, token):
    doRequest(10, 204, requests.post, 
                        genArgs("tasks/%s/close" % taskId))