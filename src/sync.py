import todoistRequests, os, json, random

def sync():
    home = os.getenv("HOME")
    with open(home+"/.todoistCache", "r") as f:
        for line in f:
            line = line.replace("\n", "")
            command = line.split("////")[0]
            if (command == "add"):
                todoistRequests.addTask(line.split("////")[1], 
                                    int(line.split("////")[2]), 
                                    line.split("////")[3])
            elif (command == "close"):
                todoistRequests.closeTask(int(line.split("////")[1]))
    
    open(home+"/.todoistCache", "w").close()
    
    with open(home+"/.todoist.json", "w") as f:
        projects, tasks = todoistRequests.getData()
        data = structure(projects, tasks)
        json.dump(data, f)

def structure(projects, tasks):
    data = {}
    data["projects"] = projects
    data["tasks"] = tasks
    ids = []
    for project in projects:
        ids.append(project)
        for task in tasks:
            if task["project_id"] == project["id"]:
                ids.append(task)
    data["ids"] = ids
    return data
        
def cache(string):
    home = os.getenv("HOME")
    with open(home+"/.todoistCache", "a") as f:
        f.write("\n"+string)

def addTask(content, projectId, dueString):
    home = os.getenv("HOME")
    tempId = ''.join(
        random.choice('qwertyuiopasdfghjklzxcvbnm1234567890') for _ in range(10))
    cache("add////{}////{}////{}////{}".format(content, str(projectId), dueString, tempId))
    with open(home+"/.todoist.json", "r") as f:
        data = json.load(f)
    task = {
            "id": tempId,
            "project_id": projectId,
            "content": content,
            "completed": False,
            "label_ids": [],
            "order": 1,
            "indent": 1,
            "priority": 1,
            "comment_count": 0,
            "due": {
                "recurring": False,
                "string": dueString,
                "date": dueString
            },
            "url": "https://todoist.com/showTask?id=2806531187",
            "date": "2018-10-22"
        }
    data["tasks"].append(task)
    data = structure(data["projects"], data["tasks"])
    with open(home+"/.todoist.json", "w") as f:
        json.dump(data, f)

def closeTask(taskId):
    home = os.getenv("HOME")
    if isinstance(taskId, str):
        editedCache = ""
        with open(home+"/.todoistCache", "r") as f:
            for line in f:
                line = line.replace("\n", "")
                command = line.split("////")[0]
                if (command == "add" and line.split("////")[4] == taskId):
                    pass
                else:
                    editedCache += line+"\n"
        with open(home+"/.todoistCache", "w") as f:
            f.write(editedCache)                        
    else:
        cache("close////"+str(taskId))
    with open(home+"/.todoist.json", "r") as f:
        data = json.load(f)
    i = 0
    for task in data["tasks"]:
        if task["id"] == taskId:
            del data["tasks"][i]
            break
        i += 1
    data = structure(data["projects"], data["tasks"])
    with open(home+"/.todoist.json", "w") as f:
        json.dump(data, f)

def getData():
    home = os.getenv("HOME")
    with open(home+"/.todoist.json", "r") as f:
        try:
            data = json.load(f)
        except:
            sync()
            data = getData()
    return data