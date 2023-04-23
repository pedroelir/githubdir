import os
from github import Github

# replace with your GitHub access token
ACCESS_TOKEN = os.environ.get("GH_TOKEN")

# specify the repository and the directory to download
REPO_NAME = "pedroelir/demos"
DIRECTORY_PATH = "python_demo/Comm/utils"

# create a PyGithub instance with the access token
g = Github(ACCESS_TOKEN)

# get the repository object
repo = g.get_repo(REPO_NAME)
branch = "Python_Rpi"

# get the GitTree object for the specified directory
tree = repo.get_git_tree(sha=branch, recursive=True).tree
for item in tree:
    if item.path.startswith(DIRECTORY_PATH):
        # download the file or directory
        if item.type == "blob":
            content = repo.get_contents(item.path, ref=branch).decoded_content
            with open(item.path.replace(DIRECTORY_PATH + "/", ""), "wb") as f:
                f.write(content)
        elif item.type == "tree" and item.path != DIRECTORY_PATH:
            os.makedirs(item.path.replace(DIRECTORY_PATH + "/", ""), exist_ok=True)
