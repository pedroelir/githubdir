# import os

# from github import Github
from repo import Repo

# replace with your GitHub access token
# ACCESS_TOKEN = os.environ.get("GH_TOKEN")

# specify the repository and the directory to download
# rep = Repo("https://github.com/pedroelir/dir/tree/system")
# rep = Repo("https://github.com/pedroelir/dir/tree/system/system")
# rep = Repo("https://github.com/pedroelir/dir/tree/system/system/")
rep = Repo("https://github.com/pedroelir/dir/blob/system/system/")  # not existing (blob instead of tree)
# rep = Repo("https://github.com/pedroelir/dir/fejk/system/system/")  # suppsed not existence (fejk instad of tree)
# rep = Repo("https://github.com/pedroelir/dir/tree/fake/url/not/exist")  # not existing
# rep = Repo("https://github.com/pedroelir/dir")
# rep = Repo("https://github.com/pedroelir/dir/")
# rep = Repo("https://github.com/pedroelir/dir/blob/other/user/system/user/src/file.txt")
# rep = Repo("https://github.com/pedroelir/dir/blob/main/.gitignore")
rep.download_contents()

# REPO_NAME = rep.repo_name
# # REPO_NAME = "pedroelir/dir"
# DIRECTORY_PATH = rep.path
# # DIRECTORY_PATH = ""

# # create a PyGithub instance with the access token
# gith = Github(ACCESS_TOKEN)

# # get the repository object
# repo = gith.get_repo(REPO_NAME)
# branch = rep.branch
# # branch = "system"

# # get the GitTree object for the specified directory
# tree = repo.get_git_tree(sha=branch, recursive=True).tree
# for item in tree:
#     if item.path.startswith(DIRECTORY_PATH):
#         # download the file or directory
#         if item.type == "blob":
#             content = repo.get_contents(item.path, ref=branch).decoded_content
#             with open(item.path.replace(DIRECTORY_PATH, ""), "wb") as f:
#                 f.write(content)
#         elif item.type == "tree" and item.path != DIRECTORY_PATH:
#             os.makedirs(item.path.replace(DIRECTORY_PATH, ""), exist_ok=True)
