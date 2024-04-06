# import os

# from github import Github
import json
from repo import Repo

# replace with your GitHub access token
# ACCESS_TOKEN = os.environ.get("GH_TOKEN")

# specify the repository and the directory to download
# rep = Repo("https://github.com/pedroelir/dir/tree/system")
# rep = Repo("https://github.com/pedroelir/dir/tree/system/system")
# rep = Repo("https://github.com/pedroelir/dir/system/system")  # Mising tree or blob keyword (not exissting)
# rep = Repo("https://github.com/pedroelir/dir/tree/system/system/")
# rep = Repo("https://github.com/pedroelir/dir/blob/system/system/")  # wrong existing (blob instead of tree)
# rep = Repo("https://github.com/pedroelir/dir/fejk/system/system/")  # suppsed not existence (fejk instad of tree)
# rep = Repo("https://github.com/pedroelir/dir/tree/fake/url/not/exist")  # not existing
# rep = Repo("https://github.com/pedroelir/dir")
# rep = Repo("https://github.com/pedroelir/dir/")
# rep = Repo("https://github.com/pedroelir/dir/blob/other/user/system/user/src/file.txt")
# rep = Repo("https://github.com/pedroelir/dir/blob/main/.gitignore")
# rep.download_contents("example2\example")

if __name__ == "__main__":
    with open("repos.json",encoding="UTF-8") as fp:
        repos: list[str] = json.load(fp=fp)

    for repo in repos:
        # folder_name = repo.split("/")[-1]
        rep = Repo(repo)
        rep.download_contents("test_folder")
