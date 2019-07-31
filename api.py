import requests

USER = ""
PASSWD = ""
DOMAIN = ""
BASE = DOMAIN+"/api"

sid = ""

def login():
    global sid
    data = {"principal": USER, "password": PASSWD}
    r = requests.post(DOMAIN + "/c/login", data=data)
    sid = r.cookies["sid"]
    if sid == "":
        raise Exception("Failed to login")

def get(endpoint, p=None):
    url = BASE + endpoint
    r = requests.get(url, params=p)
    if r.status_code >= 300:
        raise Exception("can't {} {}: {} {}".format(method, r.url,
            r.status_code, r.text))
    return r.json()

def projs():
    return get("/projects")

def repos(proj_id):
    params = {
            "page": 1,
            "page_size": 1024,
            "project_id": proj_id
    }
    return get("/repositories", params)

def tag(repo):
    endpoint = "/repositories/{}/tags".format(repo["name"])
    return get(endpoint, {"detail": 1})

def delete(repo_name, tag):
    endpoint = "/repositories/{}/tags/{}".format(repo_name, tag)
    r = requests.delete(BASE + endpoint, cookies={"sid": sid})
    if r.status_code >= 300:
        raise Exception("failed to delete {}:{}", repo_name, tag)
    print("deleted {}:{}".format(repo_name, tag))

